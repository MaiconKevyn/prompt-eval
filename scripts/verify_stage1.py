#!/usr/bin/env python3
"""Verify Stage 1 artifacts generated from sihrd5.duckdb."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "sihrd5.duckdb"

REQUIRED_FILES_V1 = [
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

REQUIRED_FILES_V2 = REQUIRED_FILES_V1 + [
    "GOAL_v2.md",
    "ground_truth_v2.json",
    "docs/generated/duckdb_runtime_metadata.json",
    "docs/generated/physical_constraints.csv",
    "docs/generated/secondary_indexes.csv",
    "docs/generated/table_metadata.csv",
    "docs/generated/column_profiles_exact.csv",
    "docs/generated/column_profiles_approx.csv",
    "docs/generated/join_policy.csv",
    "docs/generated/uf_code_quality.csv",
    "docs/generated/ground_truth_semantic_audit.csv",
    "evaluation/ground_truth/stage1_questions_v2.jsonl",
    "evaluation/ground_truth/stage1_questions_v2.md",
    "evaluation/ground_truth/rejected_questions_v2.md",
]

FORBIDDEN_SQL = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|COPY|EXPORT|IMPORT|ATTACH|DETACH|VACUUM|CALL)\b", re.I)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
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


def load_json_array(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path} is not valid JSON: {exc}")
    if not isinstance(payload, list):
        fail(f"{path} must be a JSON array")
    return payload


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def result_hash(rows: list[dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()


def to_jsonable(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, bytes):
        return value.hex()
    return value


def rows_to_dicts(columns: list[str], rows: list[tuple[Any, ...]]) -> list[dict[str, Any]]:
    return [{columns[i]: to_jsonable(value) for i, value in enumerate(row)} for row in rows]


def verify_required_files(required: list[str]) -> None:
    for relative in required:
        path = ROOT / relative
        if not path.exists():
            fail(f"required artifact missing: {relative}")
        if path.is_file() and path.stat().st_size == 0:
            fail(f"required artifact is empty: {relative}")


def verify_questions_structure(questions: list[dict[str, Any]]) -> dict[str, int]:
    if len(questions) < 50:
        fail(f"expected at least 50 validated questions, found {len(questions)}")
    ids = [q.get("id") for q in questions]
    if len(ids) != len(set(ids)):
        fail("duplicate question ids found")
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
    distribution: dict[str, int] = {}
    for q in questions:
        missing = required_keys - set(q)
        if missing:
            fail(f"{q.get('id')} is missing keys: {sorted(missing)}")
        if q["execution_status"] != "passed":
            fail(f"{q['id']} did not pass execution: {q['execution_status']}")
        if q["difficulty"] not in {"L1", "L2", "L3", "L4", "L5"}:
            fail(f"{q['id']} has invalid difficulty: {q['difficulty']}")
        sql_upper = q["sql"].strip().upper()
        if not sql_upper.startswith(("SELECT", "WITH")):
            fail(f"{q['id']} is not read-only SELECT/WITH SQL")
        if FORBIDDEN_SQL.search(q["sql"]):
            fail(f"{q['id']} contains forbidden SQL keyword")
        distribution[q["difficulty"]] = distribution.get(q["difficulty"], 0) + 1
    for difficulty in ["L1", "L2", "L3", "L4", "L5"]:
        if distribution.get(difficulty, 0) == 0:
            fail(f"no questions for {difficulty}")
    return distribution


def verify_evidence_files(questions: list[dict[str, Any]]) -> None:
    for q in questions:
        evidence = ROOT / q["validation_evidence"]
        if not evidence.exists():
            fail(f"{q['id']} evidence file missing: {q['validation_evidence']}")
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        if payload.get("id") != q["id"]:
            fail(f"{q['id']} evidence id mismatch")
        if "result_hash" not in payload:
            fail(f"{q['id']} evidence missing result hash")
        if "performance_class" not in payload:
            fail(f"{q['id']} evidence missing performance class")
        duration = float(payload.get("duration_seconds", 0))
        if duration > 5 and not payload.get("explain_plan"):
            fail(f"{q['id']} slow evidence missing EXPLAIN plan")


def verify_v1() -> None:
    verify_required_files(REQUIRED_FILES_V1)
    questions = load_jsonl(ROOT / "evaluation/ground_truth/stage1_questions.jsonl")
    distribution = verify_questions_structure(questions)
    verify_evidence_files(questions)
    manifest = json.loads((ROOT / "evaluation/ground_truth/manifest.json").read_text(encoding="utf-8"))
    if manifest.get("ground_truth_count") != len(questions):
        fail("manifest ground_truth_count does not match jsonl")
    if manifest.get("main_table_count", 0) < 20:
        fail("manifest main table count is unexpectedly low")
    evidence_files = list((ROOT / "evaluation/ground_truth/query_results").glob("SIHRD5_Q*.json"))
    if len(evidence_files) != len(questions):
        fail(f"expected {len(questions)} evidence files, found {len(evidence_files)}")
    print("PASS: Stage 1 artifacts verified")
    print(f"questions={len(questions)} distribution={distribution}")
    print(f"evidence_files={len(evidence_files)}")


def assert_duckdb_not_tracked() -> None:
    result = subprocess.run(
        ["git", "ls-files", "--", "*.duckdb", "*.duckdb.wal", "*.duckdb.tmp", "sihrd5.duckdb"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        fail(f"git ls-files failed: {result.stderr.strip()}")
    tracked = [line for line in result.stdout.splitlines() if line.strip()]
    if tracked:
        fail(f"DuckDB files are tracked by git: {tracked}")


def verify_exact_profiles() -> None:
    exact = load_csv(ROOT / "docs/generated/column_profiles_exact.csv")
    for row in exact:
        row_count = int(float(row["row_count"]))
        exact_count = int(float(row["exact_distinct_count"]))
        if exact_count > row_count:
            fail(f"exact distinct exceeds row count for {row['table_name']}.{row['column_name']}")
        if row.get("distinct_is_exact") not in {"True", "true", "1"}:
            fail(f"exact profile row not marked exact for {row['table_name']}.{row['column_name']}")
    approx = load_csv(ROOT / "docs/generated/column_profiles_approx.csv")
    for row in approx:
        if row.get("profile_mode") != "approx":
            fail(f"approx profile row not marked approx for {row['table_name']}.{row['column_name']}")


def verify_semantic_audit(questions: list[dict[str, Any]]) -> None:
    audit_rows = load_csv(ROOT / "docs/generated/ground_truth_semantic_audit.csv")
    audit_by_id = {row["id"]: row for row in audit_rows}
    if len(audit_by_id) < len(questions):
        fail("semantic audit has fewer rows than accepted v2 questions")
    for q in questions:
        audit = audit_by_id.get(q["id"])
        if not audit:
            fail(f"{q['id']} missing semantic audit row")
        if audit["final_disposition"] not in {"accepted", "accepted_with_explicit_scope", "valid_with_caveats"}:
            fail(f"{q['id']} has unacceptable semantic disposition: {audit['final_disposition']}")
        sql_lower = " ".join(q["sql"].lower().split())
        question_lower = q["question_pt"].lower()
        if "join raca_cor r on i.raca_cor = r.raca_cor" in sql_lower and "left join raca_cor" not in sql_lower:
            fail(f"{q['id']} uses unsafe RACA_COR inner join")
        if (
            "join municipios m on i.munic_res = m.co_municipio_6d" in sql_lower
            and "left join municipios m on i.munic_res = m.co_municipio_6d" not in sql_lower
            and "mapeado" not in question_lower
        ):
            fail(f"{q['id']} uses MUNIC_RES inner join without explicit mapped scope")
        if (
            "join municipios mr on i.munic_res = mr.co_municipio_6d" in sql_lower
            and "left join municipios mr on i.munic_res = mr.co_municipio_6d" not in sql_lower
            and "mapeado" not in question_lower
        ):
            fail(f"{q['id']} uses MUNIC_RES inner join without explicit mapped scope")
        if "count(distinct sg_uf)" in sql_lower and "valid_uf" not in sql_lower and "uf" in question_lower:
            fail(f"{q['id']} counts SG_UF as UFs without valid-UF filtering")


def verify_business_meaning_traceability() -> None:
    dictionary = (ROOT / "docs/business_dictionary.md").read_text(encoding="utf-8")
    required_terms = [
        "**Observed:**",
        "**Inferred:**",
        "**Externally verified:**",
        "**Unknown:**",
        "## Key Business Fields",
        "evidence_status",
        "evidence_basis",
        "## External Dictionaries Still Needed Before Stage 2 Promotion",
    ]
    for term in required_terms:
        if term not in dictionary:
            fail(f"business dictionary missing traceability marker: {term}")
    overview = (ROOT / "docs/database_overview.md").read_text(encoding="utf-8")
    relationship_map = (ROOT / "docs/relationship_map.md").read_text(encoding="utf-8")
    for url in [
        "https://duckdb.org/docs/current/sql/meta/duckdb_table_functions",
        "https://duckdb.org/docs/current/configuration/pragmas",
        "https://duckdb.org/docs/current/connect/concurrency",
        "https://duckdb.org/docs/current/sql/constraints",
        "https://duckdb.org/docs/current/guides/performance/indexing",
    ]:
        if url not in overview and url not in relationship_map:
            fail(f"missing DuckDB source anchor in generated docs: {url}")


def verify_v2_reexecution(questions: list[dict[str, Any]]) -> tuple[int, int]:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    con.execute("PRAGMA threads=4")
    reexecuted = 0
    mismatches = 0
    for q in questions:
        result = con.execute(q["sql"])
        columns = [d[0] for d in result.description]
        rows = rows_to_dicts(columns, result.fetchall())
        evidence = json.loads((ROOT / q["validation_evidence"]).read_text(encoding="utf-8"))
        current_hash = result_hash(rows)
        reexecuted += 1
        if current_hash != evidence.get("result_hash"):
            mismatches += 1
            fail(f"{q['id']} hash mismatch")
        if len(rows) != evidence.get("row_count"):
            fail(f"{q['id']} row_count mismatch")
    return reexecuted, mismatches


def verify_root_ground_truth_v2(questions: list[dict[str, Any]]) -> None:
    root_items = load_json_array(ROOT / "ground_truth_v2.json")
    if len(root_items) != len(questions):
        fail("ground_truth_v2.json count does not match v2 jsonl")
    comparable_fields = [
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
        "semantic_disposition",
    ]
    for index, (root_item, jsonl_item) in enumerate(zip(root_items, questions), start=1):
        for field in comparable_fields:
            if root_item.get(field) != jsonl_item.get(field):
                fail(f"ground_truth_v2.json row {index} field {field} does not match jsonl")
        if {"question", "query", "tables"} & set(root_item):
            fail(f"{root_item.get('id')} still contains legacy root JSON fields")


def verify_v2() -> None:
    verify_required_files(REQUIRED_FILES_V2)
    assert_duckdb_not_tracked()
    questions = load_jsonl(ROOT / "evaluation/ground_truth/stage1_questions_v2.jsonl")
    verify_root_ground_truth_v2(questions)
    distribution = verify_questions_structure(questions)
    verify_evidence_files(questions)
    verify_exact_profiles()
    verify_semantic_audit(questions)
    verify_business_meaning_traceability()
    manifest = json.loads((ROOT / "evaluation/ground_truth/manifest.json").read_text(encoding="utf-8"))
    if manifest.get("ground_truth_v2_count") != len(questions):
        fail("manifest ground_truth_v2_count does not match v2 jsonl")
    for generated in [
        "docs/generated/duckdb_runtime_metadata.json",
        "docs/generated/physical_constraints.csv",
        "docs/generated/secondary_indexes.csv",
        "docs/generated/table_metadata.csv",
        "docs/generated/column_profiles_exact.csv",
        "docs/generated/column_profiles_approx.csv",
        "docs/generated/join_policy.csv",
        "docs/generated/uf_code_quality.csv",
        "docs/generated/ground_truth_semantic_audit.csv",
    ]:
        if generated not in manifest.get("generated_artifacts", []):
            fail(f"manifest generated_artifacts missing {generated}")
    constraints = load_csv(ROOT / "docs/generated/physical_constraints.csv")
    if not any(row["constraint_type"] == "PRIMARY KEY" for row in constraints):
        fail("physical constraints do not document primary keys")
    uf_quality = load_csv(ROOT / "docs/generated/uf_code_quality.csv")
    if not any(row["is_valid_uf"] in {"False", "false", "0"} for row in uf_quality):
        fail("invalid SG_UF values were not reported")
    reexecuted, mismatches = verify_v2_reexecution(questions)
    evidence_files = list((ROOT / "evaluation/ground_truth/query_results_v2").glob("SIHRD5_Q*.json"))
    if len(evidence_files) != len(questions):
        fail(f"expected {len(questions)} v2 evidence files, found {len(evidence_files)}")
    print("PASS: Stage 1 v2 artifacts verified")
    print(f"questions={len(questions)} distribution={distribution}")
    print(f"reexecuted={reexecuted}")
    print("semantic_failures=0")
    print(f"hash_mismatches={mismatches}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", choices=["v1", "v2"], default="v2")
    args = parser.parse_args()
    if args.version == "v1":
        verify_v1()
    else:
        verify_v2()


if __name__ == "__main__":
    main()
