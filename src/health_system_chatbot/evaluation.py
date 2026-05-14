from __future__ import annotations

import json
import statistics
import time
from pathlib import Path
from typing import Any

from .artifacts import load_stage1_context
from .config import ChatbotConfig, load_config
from .duckdb_executor import execute_validated_sql
from .intent import classify_question
from .models import EvaluationRecord, GroundTruthItem
from .schema_context import retrieve_context
from .sql_generator import generate_sql_plan
from .sql_validator import validate_sql


def _load_dataset(path: Path) -> list[GroundTruthItem]:
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            items.append(GroundTruthItem.model_validate(json.loads(line)))
    return items


def _load_evidence(root: Path, item: GroundTruthItem) -> dict[str, Any] | None:
    if not item.validation_evidence:
        return None
    path = root / item.validation_evidence
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _rows_match(actual: list[dict[str, Any]], expected: list[dict[str, Any]]) -> bool:
    if len(actual) < len(expected):
        return False
    return actual[: len(expected)] == expected


def evaluate_item(
    item: GroundTruthItem,
    *,
    config: ChatbotConfig,
    ctx=None,
    allow_llm: bool = True,
) -> EvaluationRecord:
    ctx = ctx or load_stage1_context(config.project_root)
    start = time.perf_counter()
    errors: list[str] = []
    warnings: list[str] = []
    result_match: bool | None = None
    executed = False
    sql_valid = False

    intent = classify_question(item.question_pt, ctx)
    if intent.status != "answerable":
        return EvaluationRecord(
            id=item.id,
            question_pt=item.question_pt,
            difficulty=item.difficulty,
            status="clarified" if intent.status == "needs_clarification" else "refused",
            intent_status=intent.status,
            sql_valid=False,
            executed=False,
            result_match=False,
            latency_seconds=time.perf_counter() - start,
            errors=[intent.reason],
        )

    try:
        retrieved = retrieve_context(item.question_pt, ctx, config=config)
        plan = generate_sql_plan(
            item.question_pt,
            retrieved,
            ctx,
            config,
            allow_llm=allow_llm,
        )
        validation = validate_sql(plan.sql, ctx, question=item.question_pt, plan=plan)
        sql_valid = validation.is_valid
        warnings.extend(validation.warnings)
        if not validation.is_valid:
            errors.extend(validation.errors)
        else:
            execution = execute_validated_sql(validation, db_path=config.db_path, max_rows=config.max_rows)
            executed = True
            evidence = _load_evidence(config.project_root, item)
            if evidence:
                result_match = (
                    execution.columns == evidence.get("columns", [])
                    and _rows_match(execution.rows, evidence.get("preview_rows", []))
                )
            else:
                result_match = None
    except Exception as exc:
        errors.append(str(exc))

    return EvaluationRecord(
        id=item.id,
        question_pt=item.question_pt,
        difficulty=item.difficulty,
        status="answered" if executed else "failed",
        intent_status=intent.status,
        sql_valid=sql_valid,
        executed=executed,
        result_match=result_match,
        latency_seconds=time.perf_counter() - start,
        errors=errors,
        warnings=warnings,
    )


def summarize_records(records: list[EvaluationRecord]) -> dict[str, Any]:
    total = len(records)
    latencies = [r.latency_seconds for r in records]
    failures_by_difficulty: dict[str, int] = {}
    for record in records:
        if record.errors:
            key = record.difficulty or "unknown"
            failures_by_difficulty[key] = failures_by_difficulty.get(key, 0) + 1
    return {
        "total": total,
        "intent_accuracy": sum(r.intent_status == "answerable" for r in records) / total if total else 0,
        "sql_valid_rate": sum(r.sql_valid for r in records) / total if total else 0,
        "sql_execution_rate": sum(r.executed for r in records) / total if total else 0,
        "result_match_rate": (
            sum(r.result_match is True for r in records) / sum(r.result_match is not None for r in records)
            if any(r.result_match is not None for r in records)
            else None
        ),
        "caveat_recall": sum(not r.errors for r in records) / total if total else 0,
        "latency_p50": statistics.median(latencies) if latencies else 0,
        "latency_p95": sorted(latencies)[int(0.95 * (len(latencies) - 1))] if latencies else 0,
        "cost_estimate": {"usd": None, "method": "not_tracked_yet"},
        "failure_by_difficulty": failures_by_difficulty,
        "failures": [r.model_dump() for r in records if r.errors],
    }


def evaluate_dataset(
    *,
    dataset: Path,
    output: Path,
    limit: int | None = None,
    allow_llm: bool = True,
    config: ChatbotConfig | None = None,
) -> dict[str, Any]:
    cfg = config or load_config()
    items = _load_dataset(dataset)
    if limit is not None:
        items = items[:limit]
    ctx = load_stage1_context(cfg.project_root)
    records = [evaluate_item(item, config=cfg, ctx=ctx, allow_llm=allow_llm) for item in items]
    payload = {
        "dataset": str(dataset),
        "limit": limit,
        "allow_llm": allow_llm,
        "summary": summarize_records(records),
        "records": [record.model_dump() for record in records],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=True, default=str), encoding="utf-8")
    return payload
