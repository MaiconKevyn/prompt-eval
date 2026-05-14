from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .config import find_project_root
from .models import (
    GroundTruthItem,
    JoinPolicy,
    Stage1Context,
    TableContext,
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _to_int(value: str | None) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def _to_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _load_join_policies(root: Path) -> list[JoinPolicy]:
    rows = _read_csv(root / "docs/generated/join_policy.csv")
    policies: list[JoinPolicy] = []
    for row in rows:
        policies.append(
            JoinPolicy(
                left=row.get("left", ""),
                right=row.get("right", ""),
                business_meaning=row.get("business_meaning", ""),
                left_rows=_to_int(row.get("left_rows")),
                matched_rows=_to_int(row.get("matched_rows")),
                unmatched_rows=_to_int(row.get("unmatched_rows")),
                match_rate_non_null=_to_float(row.get("match_rate_non_null")),
                confidence=row.get("confidence", ""),
                accepted_usage_policy=row.get("accepted_usage_policy", ""),
            )
        )
    return policies


def _load_ground_truth(root: Path) -> list[GroundTruthItem]:
    path = root / "evaluation/ground_truth/stage1_questions_v2.jsonl"
    if not path.exists():
        path = root / "evaluation/ground_truth/stage1_questions.jsonl"
    items: list[GroundTruthItem] = []
    if not path.exists():
        return items
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            items.append(GroundTruthItem.model_validate(json.loads(line)))
    return items


def _table_name_from_qualified(value: str) -> str:
    parts = value.split(".")
    return parts[0] if len(parts) == 2 else value


def _load_tables(root: Path, join_policies: Iterable[JoinPolicy]) -> dict[str, TableContext]:
    tables: dict[str, TableContext] = {}

    for row in _read_csv(root / "docs/generated/table_metadata.csv"):
        name = row.get("table_name", "")
        if not name:
            continue
        tables[name] = TableContext(
            table_name=name,
            schema_name=row.get("schema_name", "main") or "main",
            column_count=_to_int(row.get("column_count")),
            estimated_size=_to_int(row.get("estimated_size")),
            notes=[],
        )

    for row in _read_csv(root / "docs/generated/column_catalog.csv"):
        table = row.get("table_name", "")
        column = row.get("column_name", "")
        data_type = row.get("data_type", "")
        if table and column and data_type:
            tables.setdefault(table, TableContext(table_name=table)).column_types[column] = data_type

    for row in _read_csv(root / "docs/generated/column_profiles_exact.csv"):
        table = row.get("table_name", "")
        column = row.get("column_name", "")
        if not table or not column:
            continue
        ctx = tables.setdefault(table, TableContext(table_name=table))
        ctx.columns.append(column)
        if row.get("data_type"):
            ctx.column_types[column] = row["data_type"]

    for row in _read_csv(root / "docs/generated/column_profiles_approx.csv"):
        table = row.get("table_name", "")
        column = row.get("column_name", "")
        if not table or not column:
            continue
        ctx = tables.setdefault(table, TableContext(table_name=table))
        if column not in ctx.columns:
            ctx.columns.append(column)
        if row.get("data_type"):
            ctx.column_types[column] = row["data_type"]

    for policy in join_policies:
        left_table = _table_name_from_qualified(policy.left)
        right_table = _table_name_from_qualified(policy.right)
        for table in (left_table, right_table):
            if table:
                tables.setdefault(table, TableContext(table_name=table))
        note = (
            f"join {policy.left} -> {policy.right}: "
            f"{policy.confidence}/{policy.accepted_usage_policy}"
        )
        if left_table:
            tables[left_table].notes.append(note)
        if right_table and right_table != left_table:
            tables[right_table].notes.append(note)

    return tables


def load_stage1_context(project_root: Path | None = None) -> Stage1Context:
    root = find_project_root(project_root)
    join_policies = _load_join_policies(root)
    return Stage1Context(
        project_root=str(root),
        tables=_load_tables(root, join_policies),
        join_policies=join_policies,
        ground_truth=_load_ground_truth(root),
        readiness_notes=_read_text(root / "docs/stage2_readiness.md"),
        business_dictionary=_read_text(root / "docs/business_dictionary.md"),
        schema_catalog=_read_text(root / "docs/schema_catalog.md"),
        relationship_map=_read_text(root / "docs/relationship_map.md"),
        data_quality_report=_read_text(root / "docs/data_quality_report.md"),
    )


def ground_truth_by_normalized_question(ctx: Stage1Context) -> dict[str, GroundTruthItem]:
    from .text import normalize_text

    return {normalize_text(item.question_pt): item for item in ctx.ground_truth}
