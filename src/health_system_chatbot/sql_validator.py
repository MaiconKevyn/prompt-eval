from __future__ import annotations

import re

import sqlglot
from sqlglot import expressions as exp

from .models import SqlPlan, Stage1Context, ValidationResult
from .text import normalize_text


BLOCKED_KEYWORDS = {
    "ALTER",
    "ATTACH",
    "CHECKPOINT",
    "COPY",
    "CREATE",
    "DELETE",
    "DROP",
    "EXPORT",
    "INSERT",
    "INSTALL",
    "LOAD",
    "PRAGMA",
    "TRUNCATE",
    "UPDATE",
    "VACUUM",
}

FILE_ACCESS_PATTERNS = (
    "read_csv",
    "read_json",
    "read_parquet",
    "httpfs",
    "secret",
)

NUMERIC_TYPES = {
    "TINYINT",
    "SMALLINT",
    "INTEGER",
    "BIGINT",
    "UBIGINT",
    "UTINYINT",
    "USMALLINT",
    "UINTEGER",
    "UHUGEINT",
    "HUGEINT",
    "FLOAT",
    "DOUBLE",
    "REAL",
    "DECIMAL",
    "NUMERIC",
}

VALID_UFS = {
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


def _strip_sql(sql: str) -> str:
    return sql.strip().rstrip(";").strip()


def _keyword_errors(sql: str) -> list[str]:
    upper = sql.upper()
    errors = []
    for keyword in sorted(BLOCKED_KEYWORDS):
        if re.search(rf"\b{keyword}\b", upper):
            errors.append(f"Blocked SQL keyword: {keyword}")
    lower = sql.lower()
    for pattern in FILE_ACCESS_PATTERNS:
        if pattern in lower:
            errors.append(f"Blocked file/extension access pattern: {pattern}")
    return errors


def _cte_names(parsed: exp.Expression) -> set[str]:
    names = set()
    for cte in parsed.find_all(exp.CTE):
        if cte.alias:
            names.add(cte.alias)
    return names


def _referenced_tables(parsed: exp.Expression) -> set[str]:
    ctes = _cte_names(parsed)
    tables = set()
    for table in parsed.find_all(exp.Table):
        name = table.name
        if name and name not in ctes:
            tables.add(name)
    return tables


def _table_aliases(parsed: exp.Expression) -> dict[str, str]:
    aliases: dict[str, str] = {}
    ctes = _cte_names(parsed)
    for table in parsed.find_all(exp.Table):
        if not table.name or table.name in ctes:
            continue
        aliases[table.name] = table.name
        if table.alias:
            aliases[table.alias] = table.name
    return aliases


def _column_type(ctx: Stage1Context, table_name: str, column_name: str) -> tuple[str, str] | None:
    table = ctx.tables.get(table_name)
    if not table:
        return None
    for candidate, data_type in table.column_types.items():
        if candidate.upper() == column_name.upper():
            return candidate, data_type
    return None


def _resolve_column(
    column: exp.Column,
    ctx: Stage1Context,
    aliases: dict[str, str],
    tables: set[str],
) -> tuple[str, str, str] | None:
    qualifier = column.table
    if qualifier:
        table_name = aliases.get(qualifier, qualifier)
        typed_column = _column_type(ctx, table_name, column.name)
        if typed_column:
            return table_name, typed_column[0], typed_column[1]
        return None

    matches = []
    for table_name in tables:
        typed_column = _column_type(ctx, table_name, column.name)
        if typed_column:
            matches.append((table_name, typed_column[0], typed_column[1]))
    return matches[0] if len(matches) == 1 else None


def _is_numeric_type(data_type: str) -> bool:
    upper = data_type.upper()
    return upper in NUMERIC_TYPES or upper.startswith("DECIMAL(") or upper.startswith("NUMERIC(")


def _literal_preview(literal: exp.Literal) -> str:
    value = str(literal.this)
    if len(value) > 40:
        value = value[:37] + "..."
    return value


def _text_literal_numeric_type_errors(
    parsed: exp.Expression,
    ctx: Stage1Context,
    tables: set[str],
) -> list[str]:
    aliases = _table_aliases(parsed)
    errors: list[str] = []
    seen: set[str] = set()

    def add_error(column: exp.Column, literal: exp.Literal) -> None:
        resolved = _resolve_column(column, ctx, aliases, tables)
        if not resolved:
            return
        table_name, column_name, data_type = resolved
        if not _is_numeric_type(data_type):
            return
        key = f"{table_name}.{column_name}:{literal.this}"
        if key in seen:
            return
        seen.add(key)
        errors.append(
            f"Column {table_name}.{column_name} has {data_type} type and cannot be "
            f"compared to text literal '{_literal_preview(literal)}'. "
            "For city names, join municipios and filter municipios.NO_MUNICIPIO/SG_UF."
        )

    comparison_types = (exp.EQ, exp.NEQ, exp.GT, exp.GTE, exp.LT, exp.LTE)
    for comparison_type in comparison_types:
        for comparison in parsed.find_all(comparison_type):
            left = comparison.left
            right = comparison.right
            if isinstance(left, exp.Column) and isinstance(right, exp.Literal) and right.is_string:
                add_error(left, right)
            if isinstance(right, exp.Column) and isinstance(left, exp.Literal) and left.is_string:
                add_error(right, left)

    for in_expression in parsed.find_all(exp.In):
        target = in_expression.this
        if not isinstance(target, exp.Column):
            continue
        for expression in in_expression.expressions:
            if isinstance(expression, exp.Literal) and expression.is_string:
                add_error(target, expression)

    return errors


def _has_left_join_for(sql: str, table_name: str) -> bool:
    return bool(re.search(rf"\bLEFT\s+(?:OUTER\s+)?JOIN\s+{re.escape(table_name)}\b", sql, re.I))


def _has_explicit_mapped_scope(question: str, plan: SqlPlan | None) -> bool:
    chunks = [question]
    if plan:
        chunks.extend(plan.caveats)
        chunks.extend(plan.join_assumptions)
        chunks.append(plan.question)
    text = normalize_text(" ".join(chunks))
    return any(token in text for token in ("mapeado", "mapeada", "mapped", "restrito", "universo mapeado"))


def validate_sql(
    sql: str,
    ctx: Stage1Context,
    *,
    question: str = "",
    plan: SqlPlan | None = None,
) -> ValidationResult:
    safe_sql = _strip_sql(sql)
    errors = []
    warnings = []

    if not safe_sql:
        return ValidationResult(is_valid=False, severity="error", errors=["SQL is empty"])

    errors.extend(_keyword_errors(safe_sql))
    if ";" in safe_sql:
        errors.append("Multiple SQL statements are not allowed")

    try:
        parsed_statements = sqlglot.parse(safe_sql, read="duckdb")
    except sqlglot.errors.ParseError as exc:
        return ValidationResult(is_valid=False, severity="error", errors=[f"SQL parse error: {exc}"])

    if len(parsed_statements) != 1:
        errors.append("Exactly one SQL statement is required")
        parsed = parsed_statements[0] if parsed_statements else None
    else:
        parsed = parsed_statements[0]

    if parsed is not None and not isinstance(parsed, exp.Select):
        errors.append(f"Only SELECT/WITH statements are allowed, got {parsed.key}")

    tables: set[str] = set()
    if parsed is not None:
        tables = _referenced_tables(parsed)
        unknown = sorted(table for table in tables if table not in ctx.table_names)
        if unknown:
            errors.append(f"Unknown or unsupported table(s): {', '.join(unknown)}")
        else:
            errors.extend(_text_literal_numeric_type_errors(parsed, ctx, tables))

    for table in tables:
        if table.startswith("main_dbt_test__audit") or table.startswith("dbt_"):
            errors.append(f"Audit table is not allowed for business answers: {table}")

    question_text = normalize_text(question)
    is_audit_question = any(
        token in question_text
        for token in (
            "auditoria",
            "qualidade",
            "inconsistencia",
            "inconsistencias",
            "sem correspondencia",
            "nao mapeado",
            "orfaos",
        )
    )

    for policy in ctx.join_policies:
        left_table = policy.left.split(".")[0]
        right_table = policy.right.split(".")[0]
        if left_table not in tables or right_table not in tables:
            continue

        left_col = policy.left.split(".")[-1]
        right_col = policy.right.split(".")[-1]
        uses_policy_columns = left_col.upper() in safe_sql.upper() and right_col.upper() in safe_sql.upper()

        if policy.confidence == "rejected" and uses_policy_columns and not is_audit_question:
            has_unmapped_bucket = (
                _has_left_join_for(safe_sql, right_table)
                and (
                    "SEM CORRESPONDENCIA" in safe_sql.upper()
                    or "SEM CORRESPONDENCIA" in question.upper()
                    or "QUANDO HOUVER CORRESPONDENCIA" in question.upper()
                )
            )
            if has_unmapped_bucket:
                warnings.append(
                    f"Rejected relationship used only with LEFT JOIN/unmapped bucket: {policy.left} -> {policy.right}"
                )
            else:
                errors.append(
                    f"Rejected relationship cannot be used for business answers: {policy.left} -> {policy.right}"
                )

        if policy.accepted_usage_policy == "left_join_or_explicit_mapped_scope_required":
            has_left_join = _has_left_join_for(safe_sql, right_table)
            if uses_policy_columns and not has_left_join and not _has_explicit_mapped_scope(question, plan):
                errors.append(
                    f"Join requires LEFT JOIN or explicit mapped scope: {policy.left} -> {policy.right}"
                )

    upper = safe_sql.upper()
    if "INTERNACAO_PROCEDIMENTO" in upper and "INTERNACOES" in upper and "COUNT(*)" in upper:
        warnings.append(
            "Query joins procedures and admissions; confirm whether the unit is procedure occurrence or hospitalization."
        )

    if "SG_UF" in upper and "VALID_UF" not in upper and not all(f"'{uf}'" in upper for uf in list(VALID_UFS)[:3]):
        warnings.append("Query references SG_UF; ensure invalid numeric SG_UF codes are excluded when counting UFs.")

    if "LIMIT" not in upper and not re.search(r"\b(COUNT|SUM|AVG|MIN|MAX|QUANTILE|ROUND)\s*\(", upper):
        warnings.append("Exploratory row-returning query has no LIMIT.")

    if errors:
        return ValidationResult(
            is_valid=False,
            severity="error",
            errors=errors,
            warnings=warnings,
            required_clarification="A consulta precisa ser corrigida antes de executar.",
        )

    return ValidationResult(
        is_valid=True,
        severity="warning" if warnings else "info",
        errors=[],
        warnings=warnings,
        safe_sql=safe_sql,
    )
