from __future__ import annotations

import hashlib
import json
import time
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb

from .models import ExecutionResult, ValidationResult


def _json_default(value: Any) -> str | float | int | None:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value)


def _normalize_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def _hash_rows(columns: list[str], rows: list[dict[str, Any]]) -> str:
    payload = {"columns": columns, "rows": rows}
    data = json.dumps(payload, ensure_ascii=True, sort_keys=True, default=_json_default)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def execute_validated_sql(
    validation: ValidationResult,
    *,
    db_path: Path,
    max_rows: int = 200,
) -> ExecutionResult:
    if not validation.is_valid or not validation.safe_sql:
        raise ValueError("Only validated SQL can be executed")
    if not db_path.exists():
        raise FileNotFoundError(f"DuckDB file not found: {db_path}")

    start = time.perf_counter()
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        cursor = con.execute(validation.safe_sql)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        raw_rows = cursor.fetchmany(max_rows + 1)
    finally:
        con.close()

    elapsed = time.perf_counter() - start
    truncated = len(raw_rows) > max_rows
    raw_rows = raw_rows[:max_rows]
    rows = [
        {columns[idx]: _normalize_value(value) for idx, value in enumerate(row)}
        for row in raw_rows
    ]
    return ExecutionResult(
        sql=validation.safe_sql,
        columns=columns,
        rows=rows,
        row_count=len(rows),
        elapsed_seconds=elapsed,
        result_hash=_hash_rows(columns, rows),
        truncated=truncated,
    )

