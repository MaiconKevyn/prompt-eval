#!/usr/bin/env python3
"""Validate the canonical root ground_truth_v2.json artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "ground_truth_v2.json"
DEFAULT_DB = ROOT / "sihrd5.duckdb"

REQUIRED_FIELDS = {
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
}

ALLOWED_DIFFICULTIES = {"L1", "L2", "L3", "L4", "L5"}
ALLOWED_RESULT_TYPES = {
    "scalar",
    "distribution",
    "ranking",
    "time_series",
    "comparison",
    "data_quality_finding",
}
ALLOWED_DISPOSITIONS = {
    "accepted",
    "accepted_with_explicit_scope",
    "valid_with_caveats",
}
FORBIDDEN_SQL = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|COPY|EXPORT|IMPORT|ATTACH|DETACH|VACUUM|CALL)\b",
    re.I,
)
LEGACY_PATTERNS = [
    " atendimentos ",
    "codigo_6d",
    ".nome",
    ".estado",
    "cd_descricao",
    " metrica ",
    " valor ",
    "bolsa_familia",
    "idhm",
    "esgotamento_sanitario",
]
VALID_UF_CODES = {
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
}


class ValidationFailure(Exception):
    """Raised when the ground-truth artifact is invalid."""


def normalize_sql(sql: str) -> str:
    return " " + re.sub(r"\s+", " ", sql.strip().lower()) + " "


def collect_static_sql_errors(sql: str) -> list[str]:
    """Return SQL guardrail errors for tests and CLI validation."""
    normalized = normalize_sql(sql)
    errors: list[str] = []
    if not normalized.strip().upper().startswith(("SELECT", "WITH")):
        errors.append("read_only_start")
    if FORBIDDEN_SQL.search(sql):
        errors.append("forbidden_sql")
    for pattern in LEGACY_PATTERNS:
        lowered = pattern.lower()
        if lowered in {".nome", ".estado"}:
            alias_matches = re.findall(r"\b[a-z_][\w]*" + re.escape(lowered) + r"[\w]*", normalized)
            errors.extend(sorted(set(alias_matches)))
        elif lowered in normalized:
            errors.append(pattern.strip().lower())
    return errors


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, bytes):
        return value.hex()
    return value


def _rows_to_dicts(columns: list[str], rows: list[tuple[Any, ...]]) -> list[dict[str, Any]]:
    return [{columns[i]: _to_jsonable(value) for i, value in enumerate(row)} for row in rows]


def result_hash(rows: list[dict[str, Any]]) -> str:
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, default=str).encode()
    return hashlib.sha256(payload).hexdigest()


def performance_class(duration_seconds: float) -> str:
    if duration_seconds <= 1:
        return "fast"
    if duration_seconds <= 5:
        return "moderate"
    if duration_seconds <= 15:
        return "slow"
    return "too_slow_for_default_eval"


def load_items(path: Path = DEFAULT_DATASET) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValidationFailure(f"{path} must be a JSON array")
    return payload


def validate_item_format(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    item_id = item.get("id", "<missing>")
    missing = sorted(REQUIRED_FIELDS - set(item))
    if missing:
        errors.append(f"{item_id}: missing fields {missing}")
    legacy = {"question", "query", "tables"} & set(item)
    if legacy:
        errors.append(f"{item_id}: legacy fields still present {sorted(legacy)}")
    if item.get("difficulty") not in ALLOWED_DIFFICULTIES:
        errors.append(f"{item_id}: invalid difficulty {item.get('difficulty')!r}")
    if item.get("expected_result_type") not in ALLOWED_RESULT_TYPES:
        errors.append(f"{item_id}: invalid expected_result_type {item.get('expected_result_type')!r}")
    if item.get("semantic_disposition") not in ALLOWED_DISPOSITIONS:
        errors.append(f"{item_id}: invalid semantic_disposition {item.get('semantic_disposition')!r}")
    for field in ["tables_used", "columns_used"]:
        if field in item and not isinstance(item[field], list):
            errors.append(f"{item_id}: {field} must be a list")
    for error in collect_static_sql_errors(str(item.get("sql", ""))):
        errors.append(f"{item_id}: static_sql:{error}")
    return errors


def validate_format(items: list[dict[str, Any]]) -> None:
    errors: list[str] = []
    ids: list[str] = []
    for item in items:
        ids.append(str(item.get("id", "")))
        errors.extend(validate_item_format(item))
    if len(ids) != len(set(ids)):
        errors.append("duplicate ids found")
    if len(items) < 50:
        errors.append(f"expected at least 50 items, found {len(items)}")
    if errors:
        raise ValidationFailure("\n".join(errors))


def _contains_mapped_scope(item: dict[str, Any]) -> bool:
    text = " ".join(
        str(item.get(field, ""))
        for field in ["question_pt", "assumptions", "data_quality_notes", "semantic_disposition"]
    ).lower()
    return "mapead" in text or "sem correspondencia" in text or "left join" in text


def validate_semantics(items: list[dict[str, Any]]) -> None:
    validate_format(items)
    errors: list[str] = []
    for item in items:
        item_id = item["id"]
        sql = normalize_sql(item["sql"])
        question = item["question_pt"].lower()
        notes = item.get("data_quality_notes", "").lower()
        if " pacientes " in f" {question} " and "internacoes de pacientes" not in question:
            errors.append(f"{item_id}: question uses patient grain without internacao wording")
        if " val_uti " in sql and "uti" in question:
            if not any(term in question for term in ["valor", "custo", "cobranca", "cobrança"]):
                errors.append(f"{item_id}: UTI question uses VAL_UTI without value/cost wording")
        if " dias_perm " in sql and "dias_perm diferente" not in question:
            if "dias_perm" not in question and "dias_perm" not in notes:
                errors.append(f"{item_id}: DIAS_PERM used without explicit caveat")
        if " join municipios " in sql and "i.munic_res = m.co_municipio_6d" in sql:
            if " left join municipios " not in sql and "mapead" not in question:
                errors.append(f"{item_id}: MUNIC_RES inner join without mapped-scope wording")
        if " join municipios mr " in sql and "i.munic_res = mr.co_municipio_6d" in sql:
            if " left join municipios mr " not in sql and "mapead" not in question:
                errors.append(f"{item_id}: MUNIC_RES inner join without mapped-scope wording")
        for table in ["raca_cor", "instrucao", "vincprev", "cbor", "etnia"]:
            if f" join {table} " in sql and f" left join {table} " not in sql and not _contains_mapped_scope(item):
                errors.append(f"{item_id}: unsafe inner join on {table}")
        if "count(distinct sg_uf)" in sql and "valid" not in sql and "uf" in question:
            errors.append(f"{item_id}: SG_UF count lacks valid UF filter")
        for uf in re.findall(r"'([A-Z]{2})'", item["sql"]):
            if uf not in VALID_UF_CODES:
                errors.append(f"{item_id}: invalid UF literal {uf}")
    if errors:
        raise ValidationFailure("\n".join(errors))


def execute_items(items: list[dict[str, Any]], db_path: Path, *, write_evidence: bool = True) -> None:
    validate_semantics(items)
    con = duckdb.connect(str(db_path), read_only=True)
    con.execute("PRAGMA threads=4")
    for item in items:
        start = time.perf_counter()
        result = con.execute(item["sql"])
        columns = [description[0] for description in result.description]
        rows = _rows_to_dicts(columns, result.fetchall())
        duration = time.perf_counter() - start
        evidence = {
            "id": item["id"],
            "question_pt": item["question_pt"],
            "executed_at": datetime.now(UTC).isoformat(),
            "database_file": str(db_path.name),
            "sql": item["sql"],
            "duration_seconds": round(duration, 6),
            "performance_class": performance_class(duration),
            "explain_plan": [],
            "row_count": len(rows),
            "columns": columns,
            "preview_rows": rows[:20],
            "result_hash": result_hash(rows),
            "semantic_disposition": item["semantic_disposition"],
        }
        if duration > 5:
            explain_result = con.execute(f"EXPLAIN {item['sql']}")
            explain_columns = [description[0] for description in explain_result.description]
            evidence["explain_plan"] = _rows_to_dicts(explain_columns, explain_result.fetchall())
        if len(rows) != item.get("row_count"):
            raise ValidationFailure(f"{item['id']}: row_count mismatch {len(rows)} != {item.get('row_count')}")
        evidence_path = ROOT / item["validation_evidence"]
        if write_evidence:
            evidence_path.parent.mkdir(parents=True, exist_ok=True)
            evidence_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
        elif evidence_path.exists():
            previous = json.loads(evidence_path.read_text(encoding="utf-8"))
            if previous.get("result_hash") != evidence["result_hash"]:
                raise ValidationFailure(f"{item['id']}: hash mismatch")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--static-only", action="store_true")
    parser.add_argument("--semantic-only", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    items = load_items(Path(args.dataset))
    try:
        if args.execute:
            execute_items(items, Path(args.db), write_evidence=True)
            print(f"PASS executed={len(items)}")
            print("errors=0")
            print("semantic_failures=0")
            print("hash_mismatches=0")
        elif args.semantic_only:
            validate_semantics(items)
            print("PASS semantic_policy")
        else:
            validate_format(items)
            print("PASS static_format")
            print("PASS static_sql_schema_names")
    except ValidationFailure as exc:
        raise SystemExit(f"FAIL: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
