#!/usr/bin/env python3
"""Verify Stage 1 artifacts generated from sihrd5.duckdb."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "GOAL.md",
    "docs/database_overview.md",
    "docs/schema_catalog.md",
    "docs/business_dictionary.md",
    "docs/relationship_map.md",
    "docs/data_quality_report.md",
    "docs/query_design_methodology.md",
    "docs/stage2_readiness.md",
    "docs/generated/table_inventory.csv",
    "docs/generated/table_storage_estimates.csv",
    "docs/generated/column_catalog.csv",
    "docs/generated/column_profiles.csv",
    "docs/generated/top_frequent_values.csv",
    "docs/generated/candidate_keys.csv",
    "docs/generated/relationship_coverage.csv",
    "docs/generated/data_quality_checks.json",
    "evaluation/ground_truth/manifest.json",
    "evaluation/ground_truth/stage1_questions.jsonl",
    "evaluation/ground_truth/stage1_questions.md",
    "evaluation/ground_truth/rejected_questions.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                fail(f"{path} line {line_no} is not valid JSON: {exc}")
    return rows


def main() -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.exists():
            fail(f"required artifact missing: {relative}")
        if path.is_file() and path.stat().st_size == 0:
            fail(f"required artifact is empty: {relative}")

    questions = load_jsonl(ROOT / "evaluation/ground_truth/stage1_questions.jsonl")
    if len(questions) < 50:
        fail(f"expected at least 50 validated questions, found {len(questions)}")

    ids = [q.get("id") for q in questions]
    if len(ids) != len(set(ids)):
        fail("duplicate question ids found")

    distribution: dict[str, int] = {}
    required_keys = {
        "id",
        "persona",
        "question_pt",
        "business_intent",
        "difficulty",
        "difficulty_rationale",
        "sql",
        "tables_used",
        "columns_used",
        "expected_result_type",
        "execution_status",
        "row_count",
        "result_summary",
        "validation_evidence",
        "assumptions",
        "data_quality_notes",
        "created_at",
    }
    for q in questions:
        missing = required_keys - set(q)
        if missing:
            fail(f"{q.get('id')} is missing keys: {sorted(missing)}")
        if q["execution_status"] != "passed":
            fail(f"{q['id']} did not pass execution: {q['execution_status']}")
        if q["difficulty"] not in {"L1", "L2", "L3", "L4", "L5"}:
            fail(f"{q['id']} has invalid difficulty: {q['difficulty']}")
        if not q["sql"].upper().startswith(("SELECT", "WITH")):
            fail(f"{q['id']} is not read-only SELECT/WITH SQL")
        evidence = ROOT / q["validation_evidence"]
        if not evidence.exists():
            fail(f"{q['id']} evidence file missing: {q['validation_evidence']}")
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        if payload.get("id") != q["id"]:
            fail(f"{q['id']} evidence id mismatch")
        if "result_hash" not in payload:
            fail(f"{q['id']} evidence missing result hash")
        distribution[q["difficulty"]] = distribution.get(q["difficulty"], 0) + 1

    for difficulty in ["L1", "L2", "L3", "L4", "L5"]:
        if distribution.get(difficulty, 0) == 0:
            fail(f"no questions for {difficulty}")

    manifest = json.loads((ROOT / "evaluation/ground_truth/manifest.json").read_text(encoding="utf-8"))
    if manifest.get("ground_truth_count") != len(questions):
        fail("manifest ground_truth_count does not match jsonl")
    if manifest.get("main_table_count", 0) < 20:
        fail("manifest main table count is unexpectedly low")

    for generated in [
        "docs/generated/table_storage_estimates.csv",
        "docs/generated/top_frequent_values.csv",
        "docs/generated/candidate_keys.csv",
    ]:
        if generated not in manifest.get("generated_artifacts", []):
            fail(f"manifest generated_artifacts missing {generated}")

    evidence_files = list((ROOT / "evaluation/ground_truth/query_results").glob("SIHRD5_Q*.json"))
    if len(evidence_files) != len(questions):
        fail(f"expected {len(questions)} evidence files, found {len(evidence_files)}")

    print("PASS: Stage 1 artifacts verified")
    print(f"questions={len(questions)} distribution={distribution}")
    print(f"evidence_files={len(evidence_files)}")


if __name__ == "__main__":
    main()
