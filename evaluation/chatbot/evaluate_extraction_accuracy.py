#!/usr/bin/env python3
"""Evaluate chatbot SQL extraction by comparing executed result values.

This evaluator intentionally compares database results, not generated SQL text.
Column names are retained for diagnostics, but aliases do not affect the primary
match decision.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Literal

import duckdb

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from health_system_chatbot.artifacts import load_stage1_context
from health_system_chatbot.config import ChatbotConfig, load_config
from health_system_chatbot.intent import classify_question
from health_system_chatbot.models import GroundTruthItem, Stage1Context
from health_system_chatbot.schema_context import retrieve_context
from health_system_chatbot.sql_generator import generate_sql_plan
from health_system_chatbot.sql_validator import validate_sql


ComparisonMode = Literal["ordered", "unordered", "scalar"]
ExecutionStatus = Literal["passed", "failed", "timeout", "skipped"]

DEFAULT_DATASET = "evaluation/ground_truth/stage1_questions_v2.jsonl"
DEFAULT_RESULTS_ROOT = "evaluation/chatbot/results"

RESULT_TYPE_TO_MODE: dict[str, ComparisonMode] = {
    "scalar": "scalar",
    "ranking": "ordered",
    "time_series": "ordered",
    "distribution": "unordered",
    "comparison": "unordered",
    "data_quality_finding": "unordered",
}


@dataclass
class SqlExecution:
    status: ExecutionStatus
    columns: list[str] = field(default_factory=list)
    rows: list[tuple[Any, ...]] = field(default_factory=list)
    row_count: int = 0
    duration_seconds: float = 0.0
    truncated: bool = False
    error_message: str | None = None


@dataclass
class ComparisonResult:
    result_match: bool
    alias_only_difference: bool
    type_only_difference: bool
    order_only_mismatch: bool
    shape_match: bool
    value_match: bool
    error_category: str | None = None
    error_message: str | None = None


@dataclass(frozen=True)
class RunPaths:
    run_id: str
    run_dir: Path
    output: Path
    analysis_output: Path
    trace_output: Path


def format_progress_start(index: int, total: int, item_id: str) -> str:
    return f"[{index}/{total}] {item_id} running..."


def format_progress_done(index: int, total: int, record: dict[str, Any]) -> str:
    error = record.get("error_category") or "none"
    elapsed = float(record.get("latency_seconds") or 0)
    return (
        f"[{index}/{total}] {record['id']} done "
        f"match={record['result_match']} "
        f"generated={record['generated_execution_status']} "
        f"ground_truth={record['ground_truth_execution_status']} "
        f"error={error} elapsed={elapsed:.2f}s"
    )


def print_progress(message: str, *, quiet: bool) -> None:
    if not quiet:
        print(message, flush=True)


def _json_default(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value)


def build_run_id(explicit_run_id: str | None = None) -> str:
    raw = explicit_run_id or f"extraction_{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%f')}"
    run_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", raw.strip()).strip("._-")
    if not run_id:
        raise ValueError("--run-id cannot be empty after normalization")
    return run_id


def resolve_run_paths(
    project_root: Path,
    *,
    results_root: str,
    run_id: str,
) -> RunPaths:
    root = project_root / Path(results_root)
    run_dir = root / run_id
    return RunPaths(
        run_id=run_id,
        run_dir=run_dir,
        output=run_dir / "results.json",
        analysis_output=run_dir / "analysis.md",
        trace_output=run_dir / "trace.jsonl",
    )


def load_dataset(path: Path) -> list[GroundTruthItem]:
    items: list[GroundTruthItem] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            items.append(GroundTruthItem.model_validate(json.loads(line)))
    return items


def select_items(
    items: list[GroundTruthItem],
    *,
    ids: str | None = None,
    limit: int | None = None,
) -> list[GroundTruthItem]:
    selected = items
    if ids:
        requested = [item_id.strip() for item_id in ids.split(",") if item_id.strip()]
        by_id = {item.id: item for item in items}
        missing = [item_id for item_id in requested if item_id not in by_id]
        if missing:
            raise ValueError(f"Unknown ground-truth id(s): {', '.join(missing)}")
        selected = [by_id[item_id] for item_id in requested]
    if limit is not None:
        selected = selected[:limit]
    return selected


def normalize_value(value: Any, *, numeric_tolerance: float = 1e-6) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"
        return round(value, _decimal_places_for_tolerance(numeric_tolerance))
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def _decimal_places_for_tolerance(tolerance: float) -> int:
    if tolerance <= 0:
        return 12
    return max(0, min(12, int(math.ceil(-math.log10(tolerance))) + 1))


def canonicalize_result(
    columns: list[str],
    rows: list[tuple[Any, ...]],
    *,
    numeric_tolerance: float = 1e-6,
) -> list[list[Any]]:
    _ = columns
    return [
        [normalize_value(value, numeric_tolerance=numeric_tolerance) for value in row]
        for row in rows
    ]


def _is_numeric(value: Any) -> bool:
    return isinstance(value, (int, float, Decimal)) and not isinstance(value, bool)


def _numeric_text_to_float(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return float(stripped)
    except ValueError:
        return None


def _values_equal(expected: Any, actual: Any, *, numeric_tolerance: float) -> bool:
    if _is_numeric(expected) and _is_numeric(actual):
        expected_float = float(expected)
        actual_float = float(actual)
        if math.isnan(expected_float) or math.isnan(actual_float):
            return math.isnan(expected_float) and math.isnan(actual_float)
        return math.isclose(
            expected_float,
            actual_float,
            rel_tol=numeric_tolerance,
            abs_tol=numeric_tolerance,
        )
    expected_text_number = _numeric_text_to_float(expected)
    actual_text_number = _numeric_text_to_float(actual)
    if _is_numeric(expected) and actual_text_number is not None:
        return math.isclose(
            float(expected),
            actual_text_number,
            rel_tol=numeric_tolerance,
            abs_tol=numeric_tolerance,
        )
    if expected_text_number is not None and _is_numeric(actual):
        return math.isclose(
            expected_text_number,
            float(actual),
            rel_tol=numeric_tolerance,
            abs_tol=numeric_tolerance,
        )
    if isinstance(expected, (date, datetime)):
        expected = expected.isoformat()
    if isinstance(actual, (date, datetime)):
        actual = actual.isoformat()
    return expected == actual


def _rows_equal(
    expected: tuple[Any, ...],
    actual: tuple[Any, ...],
    *,
    numeric_tolerance: float,
) -> bool:
    if len(expected) != len(actual):
        return False
    return all(
        _values_equal(left, right, numeric_tolerance=numeric_tolerance)
        for left, right in zip(expected, actual, strict=True)
    )


def _ordered_values_match(
    expected_rows: list[tuple[Any, ...]],
    actual_rows: list[tuple[Any, ...]],
    *,
    numeric_tolerance: float,
) -> bool:
    if len(expected_rows) != len(actual_rows):
        return False
    return all(
        _rows_equal(expected, actual, numeric_tolerance=numeric_tolerance)
        for expected, actual in zip(expected_rows, actual_rows, strict=True)
    )


def _unordered_values_match(
    expected_rows: list[tuple[Any, ...]],
    actual_rows: list[tuple[Any, ...]],
    *,
    numeric_tolerance: float,
) -> bool:
    if len(expected_rows) != len(actual_rows):
        return False
    unmatched = list(actual_rows)
    for expected in expected_rows:
        match_index = next(
            (
                index
                for index, actual in enumerate(unmatched)
                if _rows_equal(expected, actual, numeric_tolerance=numeric_tolerance)
            ),
            None,
        )
        if match_index is None:
            return False
        unmatched.pop(match_index)
    return True


def _strict_rows_equal(expected: tuple[Any, ...], actual: tuple[Any, ...]) -> bool:
    if len(expected) != len(actual):
        return False
    return all(left == right for left, right in zip(expected, actual, strict=True))


def _strict_ordered_values_match(
    expected_rows: list[tuple[Any, ...]],
    actual_rows: list[tuple[Any, ...]],
) -> bool:
    if len(expected_rows) != len(actual_rows):
        return False
    return all(
        _strict_rows_equal(expected, actual)
        for expected, actual in zip(expected_rows, actual_rows, strict=True)
    )


def _strict_unordered_values_match(
    expected_rows: list[tuple[Any, ...]],
    actual_rows: list[tuple[Any, ...]],
) -> bool:
    if len(expected_rows) != len(actual_rows):
        return False
    unmatched = list(actual_rows)
    for expected in expected_rows:
        match_index = next(
            (
                index
                for index, actual in enumerate(unmatched)
                if _strict_rows_equal(expected, actual)
            ),
            None,
        )
        if match_index is None:
            return False
        unmatched.pop(match_index)
    return True


def compare_results(
    expected_columns: list[str],
    expected_rows: list[tuple[Any, ...]],
    actual_columns: list[str],
    actual_rows: list[tuple[Any, ...]],
    *,
    mode: ComparisonMode,
    numeric_tolerance: float = 1e-6,
    expected_truncated: bool = False,
    actual_truncated: bool = False,
) -> ComparisonResult:
    column_count_match = len(expected_columns) == len(actual_columns)
    row_count_match = len(expected_rows) == len(actual_rows)
    shape_match = column_count_match and row_count_match
    if expected_truncated or actual_truncated:
        return ComparisonResult(
            result_match=False,
            alias_only_difference=False,
            type_only_difference=False,
            order_only_mismatch=False,
            shape_match=shape_match,
            value_match=False,
            error_category="shape_mismatch",
            error_message="Result was truncated before full comparison.",
        )
    if not shape_match:
        return ComparisonResult(
            result_match=False,
            alias_only_difference=False,
            type_only_difference=False,
            order_only_mismatch=False,
            shape_match=False,
            value_match=False,
            error_category="shape_mismatch",
            error_message=(
                "Result shape differs: "
                f"expected {len(expected_rows)}x{len(expected_columns)}, "
                f"actual {len(actual_rows)}x{len(actual_columns)}."
            ),
        )

    ordered_match = _ordered_values_match(
        expected_rows,
        actual_rows,
        numeric_tolerance=numeric_tolerance,
    )
    unordered_match = ordered_match or _unordered_values_match(
        expected_rows,
        actual_rows,
        numeric_tolerance=numeric_tolerance,
    )
    if mode == "unordered":
        value_match = unordered_match
        order_only_mismatch = False
    else:
        value_match = ordered_match
        order_only_mismatch = not ordered_match and unordered_match

    if not value_match:
        return ComparisonResult(
            result_match=False,
            alias_only_difference=False,
            type_only_difference=False,
            order_only_mismatch=order_only_mismatch,
            shape_match=True,
            value_match=False,
            error_category="order_only_mismatch" if order_only_mismatch else "value_mismatch",
            error_message=(
                "Rows contain the same values but in a different order."
                if order_only_mismatch
                else "Result values differ."
            ),
        )

    strict_ordered_match = _strict_ordered_values_match(expected_rows, actual_rows)
    strict_unordered_match = strict_ordered_match or _strict_unordered_values_match(
        expected_rows,
        actual_rows,
    )
    strict_match = strict_unordered_match if mode == "unordered" else strict_ordered_match
    return ComparisonResult(
        result_match=True,
        alias_only_difference=expected_columns != actual_columns,
        type_only_difference=not strict_match,
        order_only_mismatch=False,
        shape_match=True,
        value_match=True,
    )


def execute_sql(
    sql: str,
    *,
    db_path: Path,
    max_rows: int,
    timeout_seconds: int,
) -> SqlExecution:
    if not db_path.exists():
        return SqlExecution(
            status="failed",
            error_message=f"DuckDB file not found: {db_path}",
        )
    start = time.perf_counter()
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        con.execute(f"SET enable_progress_bar=false")
        con.execute(f"SET threads=4")
        cursor = con.execute(sql)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchmany(max_rows + 1)
    except Exception as exc:
        return SqlExecution(
            status="failed",
            duration_seconds=time.perf_counter() - start,
            error_message=str(exc),
        )
    finally:
        con.close()
    duration = time.perf_counter() - start
    if duration > timeout_seconds:
        return SqlExecution(
            status="timeout",
            columns=columns,
            rows=rows[:max_rows],
            row_count=min(len(rows), max_rows),
            duration_seconds=duration,
            truncated=len(rows) > max_rows,
            error_message=f"Query exceeded timeout_seconds={timeout_seconds}.",
        )
    truncated = len(rows) > max_rows
    rows = rows[:max_rows]
    return SqlExecution(
        status="passed",
        columns=columns,
        rows=rows,
        row_count=len(rows),
        duration_seconds=duration,
        truncated=truncated,
    )


def comparison_mode_for(item: GroundTruthItem) -> ComparisonMode:
    return RESULT_TYPE_TO_MODE.get(item.expected_result_type or "", "ordered")


def _preview_values(
    columns: list[str],
    rows: list[tuple[Any, ...]],
    *,
    numeric_tolerance: float,
    max_preview_rows: int = 10,
) -> list[list[Any]]:
    return canonicalize_result(
        columns,
        rows[:max_preview_rows],
        numeric_tolerance=numeric_tolerance,
    )


def evaluate_item(
    item: GroundTruthItem,
    *,
    config: ChatbotConfig,
    ctx: Stage1Context,
    allow_llm: bool,
    max_rows: int,
    timeout_seconds: int,
    numeric_tolerance: float,
) -> dict[str, Any]:
    start = time.perf_counter()
    record: dict[str, Any] = {
        "id": item.id,
        "difficulty": item.difficulty,
        "expected_result_type": item.expected_result_type,
        "question_pt": item.question_pt,
        "intent_status": None,
        "generated_sql": "",
        "ground_truth_sql": item.sql,
        "generated_sql_valid": False,
        "generated_sql_validation_errors": [],
        "generated_sql_validation_warnings": [],
        "generated_execution_status": "skipped",
        "ground_truth_execution_status": "skipped",
        "comparison_mode": comparison_mode_for(item),
        "result_match": False,
        "alias_only_difference": False,
        "type_only_difference": False,
        "order_only_mismatch": False,
        "shape_match": False,
        "expected_columns": [],
        "actual_columns": [],
        "expected_preview_values": [],
        "actual_preview_values": [],
        "expected_row_count": 0,
        "actual_row_count": 0,
        "expected_truncated": False,
        "actual_truncated": False,
        "error_category": None,
        "error_message": None,
        "latency_seconds": 0.0,
    }

    try:
        intent = classify_question(item.question_pt, ctx)
        record["intent_status"] = intent.status
        if intent.status != "answerable":
            record["error_category"] = "intent_not_answerable"
            record["error_message"] = intent.reason
            return record

        retrieved = retrieve_context(item.question_pt, ctx, config=config)
        try:
            plan = generate_sql_plan(
                item.question_pt,
                retrieved,
                ctx,
                config,
                allow_llm=allow_llm,
            )
        except Exception as exc:
            record["error_category"] = "sql_generation_error"
            record["error_message"] = str(exc)
            return record

        record["generated_sql"] = plan.sql
        validation = validate_sql(plan.sql, ctx, question=item.question_pt, plan=plan)
        record["generated_sql_valid"] = validation.is_valid
        record["generated_sql_validation_errors"] = validation.errors
        record["generated_sql_validation_warnings"] = validation.warnings
        if not validation.is_valid or not validation.safe_sql:
            record["error_category"] = "sql_validation_error"
            record["error_message"] = "; ".join(validation.errors)
            return record

        actual = execute_sql(
            validation.safe_sql,
            db_path=config.db_path,
            max_rows=max_rows,
            timeout_seconds=timeout_seconds,
        )
        record["generated_execution_status"] = actual.status
        record["actual_columns"] = actual.columns
        record["actual_row_count"] = actual.row_count
        record["actual_truncated"] = actual.truncated
        record["actual_preview_values"] = _preview_values(
            actual.columns,
            actual.rows,
            numeric_tolerance=numeric_tolerance,
        )
        if actual.status != "passed":
            record["error_category"] = (
                "timeout" if actual.status == "timeout" else "generated_sql_execution_error"
            )
            record["error_message"] = actual.error_message
            return record

        expected = execute_sql(
            item.sql,
            db_path=config.db_path,
            max_rows=max_rows,
            timeout_seconds=timeout_seconds,
        )
        record["ground_truth_execution_status"] = expected.status
        record["expected_columns"] = expected.columns
        record["expected_row_count"] = expected.row_count
        record["expected_truncated"] = expected.truncated
        record["expected_preview_values"] = _preview_values(
            expected.columns,
            expected.rows,
            numeric_tolerance=numeric_tolerance,
        )
        if expected.status != "passed":
            record["error_category"] = (
                "timeout" if expected.status == "timeout" else "ground_truth_sql_execution_error"
            )
            record["error_message"] = expected.error_message
            return record

        comparison = compare_results(
            expected.columns,
            expected.rows,
            actual.columns,
            actual.rows,
            mode=comparison_mode_for(item),
            numeric_tolerance=numeric_tolerance,
            expected_truncated=expected.truncated,
            actual_truncated=actual.truncated,
        )
        record["result_match"] = comparison.result_match
        record["alias_only_difference"] = comparison.alias_only_difference
        record["type_only_difference"] = comparison.type_only_difference
        record["order_only_mismatch"] = comparison.order_only_mismatch
        record["shape_match"] = comparison.shape_match
        record["error_category"] = comparison.error_category
        record["error_message"] = comparison.error_message
        return record
    except Exception as exc:
        record["error_category"] = "unknown_error"
        record["error_message"] = str(exc)
        return record
    finally:
        record["latency_seconds"] = time.perf_counter() - start


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(records)
    answerable = [record for record in records if record["intent_status"] == "answerable"]
    generated = [record for record in records if record["generated_sql"]]
    valid = [record for record in records if record["generated_sql_valid"]]
    executed = [
        record for record in records if record["generated_execution_status"] == "passed"
    ]
    comparable = [
        record
        for record in records
        if record["generated_execution_status"] == "passed"
        and record["ground_truth_execution_status"] == "passed"
        and not record["expected_truncated"]
        and not record["actual_truncated"]
    ]
    categories: dict[str, int] = {}
    for record in records:
        category = record.get("error_category")
        if category:
            categories[category] = categories.get(category, 0) + 1
    return {
        "total": total,
        "answerable_rate": len(answerable) / total if total else 0,
        "sql_generation_rate": len(generated) / total if total else 0,
        "sql_validation_rate": len(valid) / total if total else 0,
        "sql_execution_rate": len(executed) / total if total else 0,
        "result_value_match_rate": (
            sum(record["result_match"] for record in comparable) / len(comparable)
            if comparable
            else None
        ),
        "alias_only_difference_count": sum(
            record["alias_only_difference"] for record in records
        ),
        "type_only_difference_count": sum(
            record["type_only_difference"] for record in records
        ),
        "order_only_mismatch_count": sum(
            record["order_only_mismatch"] for record in records
        ),
        "shape_mismatch_count": categories.get("shape_mismatch", 0),
        "value_mismatch_count": categories.get("value_mismatch", 0),
        "error_category_counts": categories,
    }


def write_trace(records: list[dict[str, Any]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=True, default=_json_default))
            handle.write("\n")
    return path


def initialize_trace(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
    return path


def append_trace_record(record: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True, default=_json_default))
        handle.write("\n")
    return path


def write_json_payload(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=True, default=_json_default),
        encoding="utf-8",
    )


def write_analysis(payload: dict[str, Any], path: Path) -> None:
    summary = payload["summary"]
    lines = [
        "# Extraction Accuracy Evaluation",
        "",
        "## Summary",
        "",
        f"- Total: {summary['total']}",
        f"- Answerable rate: {summary['answerable_rate']:.4f}",
        f"- SQL generation rate: {summary['sql_generation_rate']:.4f}",
        f"- SQL validation rate: {summary['sql_validation_rate']:.4f}",
        f"- SQL execution rate: {summary['sql_execution_rate']:.4f}",
        f"- Result value match rate: {summary['result_value_match_rate']}",
        f"- Alias-only differences: {summary['alias_only_difference_count']}",
        f"- Type-only differences: {summary['type_only_difference_count']}",
        f"- Order-only mismatches: {summary['order_only_mismatch_count']}",
        f"- Shape mismatches: {summary['shape_mismatch_count']}",
        f"- Value mismatches: {summary['value_mismatch_count']}",
        "",
        "## Records",
        "",
        "| id | difficulty | mode | match | alias_only | type_only | order_only | error_category |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in payload["records"]:
        lines.append(
            "| {id} | {difficulty} | {mode} | {match} | {alias} | {type_only} | {order} | {category} |".format(
                id=record["id"],
                difficulty=record["difficulty"],
                mode=record["comparison_mode"],
                match=record["result_match"],
                alias=record["alias_only_difference"],
                type_only=record["type_only_difference"],
                order=record["order_only_mismatch"],
                category=record["error_category"] or "",
            )
        )
    failures = [record for record in payload["records"] if record["error_category"]]
    if failures:
        lines.extend(["", "## Failure Details", ""])
        for record in failures:
            lines.extend(
                [
                    f"### {record['id']}",
                    "",
                    f"- Category: `{record['error_category']}`",
                    f"- Message: {record['error_message']}",
                    f"- Question: {record['question_pt']}",
                    "",
                    "Generated SQL:",
                    "",
                    "```sql",
                    record["generated_sql"] or "<empty>",
                    "```",
                    "",
                    "Ground truth SQL:",
                    "",
                    "```sql",
                    record["ground_truth_sql"],
                    "```",
                    "",
                    f"- Expected preview values: `{record['expected_preview_values']}`",
                    f"- Actual preview values: `{record['actual_preview_values']}`",
                    "",
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--results-root", default=DEFAULT_RESULTS_ROOT)
    parser.add_argument("--run-id", default=None)
    parser.add_argument(
        "--output",
        default=None,
        help="Optional compatibility copy path. Canonical output is <results-root>/<run-id>/results.json.",
    )
    parser.add_argument(
        "--analysis-output",
        default=None,
        help="Optional compatibility copy path. Canonical analysis is <results-root>/<run-id>/analysis.md.",
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--ids", default=None)
    parser.add_argument("--numeric-tolerance", type=float, default=1e-6)
    parser.add_argument("--max-rows", type=int, default=10000)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable per-question progress logs. Final summary is still printed.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(ROOT)
    dataset = config.project_root / Path(args.dataset)
    run_id = build_run_id(args.run_id)
    run_paths = resolve_run_paths(
        config.project_root,
        results_root=args.results_root,
        run_id=run_id,
    )
    output_copy = config.project_root / Path(args.output) if args.output else None
    analysis_copy = (
        config.project_root / Path(args.analysis_output) if args.analysis_output else None
    )

    items = select_items(load_dataset(dataset), ids=args.ids, limit=args.limit)
    ctx = load_stage1_context(config.project_root)
    trace_path = initialize_trace(run_paths.trace_output)
    records = []
    total = len(items)
    for index, item in enumerate(items, start=1):
        print_progress(
            format_progress_start(index, total, item.id),
            quiet=args.quiet,
        )
        record = evaluate_item(
            item,
            config=config,
            ctx=ctx,
            allow_llm=not args.no_llm,
            max_rows=args.max_rows,
            timeout_seconds=args.timeout_seconds,
            numeric_tolerance=args.numeric_tolerance,
        )
        records.append(record)
        append_trace_record(record, trace_path)
        print_progress(
            format_progress_done(index, total, record),
            quiet=args.quiet,
        )
    payload = {
        "run_id": run_paths.run_id,
        "run_dir": str(run_paths.run_dir),
        "dataset": str(dataset),
        "db_path": str(config.db_path),
        "limit": args.limit,
        "ids": [item.id for item in items],
        "allow_llm": not args.no_llm,
        "numeric_tolerance": args.numeric_tolerance,
        "max_rows": args.max_rows,
        "timeout_seconds": args.timeout_seconds,
        "trace_path": str(trace_path),
        "summary": summarize(records),
        "records": records,
    }
    write_json_payload(payload, run_paths.output)
    write_analysis(payload, run_paths.analysis_output)
    if output_copy and output_copy != run_paths.output:
        write_json_payload(payload, output_copy)
    if analysis_copy and analysis_copy != run_paths.analysis_output:
        write_analysis(payload, analysis_copy)
    print(json.dumps(payload["summary"], indent=2, ensure_ascii=True, default=_json_default))
    print(f"run_id={run_paths.run_id}")
    print(f"run_dir={run_paths.run_dir}")
    print(f"output={run_paths.output}")
    print(f"analysis_output={run_paths.analysis_output}")
    print(f"trace_path={trace_path}")
    if output_copy and output_copy != run_paths.output:
        print(f"output_copy={output_copy}")
    if analysis_copy and analysis_copy != run_paths.analysis_output:
        print(f"analysis_output_copy={analysis_copy}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
