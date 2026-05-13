#!/usr/bin/env python3
"""Generate Stage 1 documentation and validated ground truth for sihrd5.duckdb."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "sihrd5.duckdb"
DOCS_DIR = ROOT / "docs"
GT_DIR = ROOT / "evaluation" / "ground_truth"
RESULTS_DIR = GT_DIR / "query_results"
MANIFEST_PATH = GT_DIR / "manifest.json"

MAIN_TABLES = [
    "car_int",
    "cbor",
    "cid",
    "complexidade",
    "contraceptivos",
    "especialidade",
    "etnia",
    "hospital",
    "instrucao",
    "internacao_procedimento",
    "internacoes",
    "marca_uti",
    "municipios",
    "nacionalidade",
    "procedimentos",
    "raca_cor",
    "sexo",
    "socioeconomico",
    "stg_hospital",
    "stg_internacoes",
    "stg_sexo",
    "tempo",
    "vincprev",
]

FACT_TABLES = {"internacoes", "internacao_procedimento", "stg_internacoes"}
DIMENSION_TABLES = {
    "car_int",
    "cbor",
    "cid",
    "complexidade",
    "contraceptivos",
    "especialidade",
    "etnia",
    "hospital",
    "instrucao",
    "marca_uti",
    "municipios",
    "nacionalidade",
    "procedimentos",
    "raca_cor",
    "sexo",
    "socioeconomico",
    "tempo",
    "vincprev",
}

PERSONAS = [
    "Gestor municipal do SUS",
    "Gestor estadual do SUS",
    "Analista DATASUS/SIH",
    "Auditor de contas hospitalares",
    "Coordenador hospitalar",
    "Epidemiologista",
    "Planejador de rede assistencial",
    "Pesquisador em saude publica",
    "Tecnico de regulacao",
    "Analista financeiro da saude",
]


@dataclass(frozen=True)
class QuestionSpec:
    persona: str
    question_pt: str
    business_intent: str
    difficulty: str
    difficulty_rationale: str
    sql: str
    expected_result_type: str
    assumptions: str = ""
    data_quality_notes: str = ""


def q(
    persona: str,
    question_pt: str,
    business_intent: str,
    difficulty: str,
    rationale: str,
    sql: str,
    result_type: str,
    assumptions: str = "",
    notes: str = "",
) -> QuestionSpec:
    return QuestionSpec(
        persona=persona,
        question_pt=question_pt,
        business_intent=business_intent,
        difficulty=difficulty,
        difficulty_rationale=rationale,
        sql=clean_sql(sql),
        expected_result_type=result_type,
        assumptions=assumptions or "Sem premissas adicionais alem do significado observado/inferido das colunas usadas.",
        data_quality_notes=notes or "Verificar caveats documentados no data quality report antes de interpretar o resultado.",
    )


def stabilize_financial_aggregates(sql: str) -> str:
    replacements = {
        "SUM(VAL_TOT)": "SUM(CAST(VAL_TOT AS DECIMAL(20,2)))",
        "SUM(i.VAL_TOT)": "SUM(CAST(i.VAL_TOT AS DECIMAL(20,2)))",
        "AVG(VAL_TOT)": "(SUM(CAST(VAL_TOT AS DECIMAL(20,2)))::DOUBLE / COUNT(VAL_TOT))",
        "AVG(i.VAL_TOT)": "(SUM(CAST(i.VAL_TOT AS DECIMAL(20,2)))::DOUBLE / COUNT(i.VAL_TOT))",
        "AVG(DIAS_PERM)": "(SUM(CAST(DIAS_PERM AS DECIMAL(20,2)))::DOUBLE / COUNT(DIAS_PERM))",
        "AVG(i.DIAS_PERM)": "(SUM(CAST(i.DIAS_PERM AS DECIMAL(20,2)))::DOUBLE / COUNT(i.DIAS_PERM))",
        "ORDER BY media_dias_permanencia DESC": "ORDER BY media_dias_permanencia DESC, SG_UF",
        "ORDER BY hosp.internacoes DESC": "ORDER BY hosp.internacoes DESC, hosp.CNES",
        "ORDER BY media_dias DESC LIMIT 20": "ORDER BY media_dias DESC, especialidade LIMIT 20",
    }
    for old, new in replacements.items():
        sql = sql.replace(old, new)
    return sql


def clean_sql(sql: str) -> str:
    return re.sub(r"\s+", " ", stabilize_financial_aggregates(sql).strip().rstrip(";"))


def quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def quote_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


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


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_dicts(con: duckdb.DuckDBPyConnection, sql: str) -> list[dict[str, Any]]:
    result = con.execute(clean_sql(sql))
    columns = [d[0] for d in result.description]
    return rows_to_dicts(columns, result.fetchall())


def markdown_table(rows: list[dict[str, Any]], max_rows: int | None = None) -> str:
    if not rows:
        return "_Nenhuma linha retornada._"
    selected = rows[:max_rows] if max_rows else rows
    columns = list(selected[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in selected:
        values = []
        for col in columns:
            value = row.get(col)
            text = "" if value is None else str(value)
            text = text.replace("|", "\\|").replace("\n", " ")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    if max_rows and len(rows) > max_rows:
        lines.append(f"\n_Mostrando {max_rows} de {len(rows)} linhas._")
    return "\n".join(lines)


def classify_table(table_schema: str, table_name: str) -> str:
    if table_schema == "main_dbt_test__audit":
        return "dbt audit"
    if table_name in FACT_TABLES:
        return "fato/staging"
    if table_name in DIMENSION_TABLES:
        return "dimensao/referencia"
    return "outro"


def get_catalog(con: duckdb.DuckDBPyConnection) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    tables = fetch_dicts(
        con,
        """
        SELECT table_schema, table_name, table_type
        FROM information_schema.tables
        ORDER BY table_schema, table_name
        """,
    )
    for table in tables:
        table["classificacao"] = classify_table(table["table_schema"], table["table_name"])
        table["row_count"] = con.execute(
            f"SELECT COUNT(*) FROM {quote_ident(table['table_schema'])}.{quote_ident(table['table_name'])}"
        ).fetchone()[0]

    columns = fetch_dicts(
        con,
        """
        SELECT table_schema, table_name, ordinal_position, column_name, data_type, is_nullable
        FROM information_schema.columns
        ORDER BY table_schema, table_name, ordinal_position
        """,
    )
    return tables, columns


def profile_columns(
    con: duckdb.DuckDBPyConnection, tables: list[dict[str, Any]], columns: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    columns_by_table: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for col in columns:
        columns_by_table.setdefault((col["table_schema"], col["table_name"]), []).append(col)

    profiles: list[dict[str, Any]] = []
    for table in tables:
        schema = table["table_schema"]
        name = table["table_name"]
        if schema != "main":
            continue
        row_count = table["row_count"]
        table_cols = columns_by_table[(schema, name)]
        base = f"{quote_ident(schema)}.{quote_ident(name)}"
        started = time.time()
        expressions: list[str] = []
        for col in table_cols:
            column = col["column_name"]
            data_type = col["data_type"]
            colref = quote_ident(column)
            expressions.append(f"COUNT(*) FILTER (WHERE {colref} IS NULL) AS {quote_ident(f'{column}__null_count')}")
            expressions.append(f"approx_count_distinct({colref}) AS {quote_ident(f'{column}__approx_distinct')}")
            if data_type.upper() not in {"BLOB"}:
                expressions.append(f"MIN({colref}) AS {quote_ident(f'{column}__min_value')}")
                expressions.append(f"MAX({colref}) AS {quote_ident(f'{column}__max_value')}")
            else:
                expressions.append(f"NULL AS {quote_ident(f'{column}__min_value')}")
                expressions.append(f"NULL AS {quote_ident(f'{column}__max_value')}")
        result = con.execute(f"SELECT {', '.join(expressions)} FROM {base}")
        row = rows_to_dicts([d[0] for d in result.description], result.fetchall())[0]
        duration = round(time.time() - started, 3)
        for col in table_cols:
            column = col["column_name"]
            data_type = col["data_type"]
            null_count = row[f"{column}__null_count"]
            approx_distinct = row[f"{column}__approx_distinct"]
            min_value = row[f"{column}__min_value"]
            max_value = row[f"{column}__max_value"]
            profiles.append(
                {
                    "table_schema": schema,
                    "table_name": name,
                    "column_name": column,
                    "data_type": data_type,
                    "row_count": row_count,
                    "null_count": null_count,
                    "null_rate": round(null_count / row_count, 6) if row_count else None,
                    "approx_distinct": approx_distinct,
                    "approx_distinct_rate": round(approx_distinct / row_count, 6) if row_count else None,
                    "min_value": to_jsonable(min_value),
                    "max_value": to_jsonable(max_value),
                    "profile_seconds": duration,
                }
            )
    return profiles


def top_value_queries(con: duckdb.DuckDBPyConnection) -> dict[str, list[dict[str, Any]]]:
    queries = {
        "internacoes_por_ano_inter": """
            SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes
            FROM internacoes
            GROUP BY 1
            ORDER BY 1
        """,
        "internacoes_por_uf_residencia": """
            SELECT m.SG_UF, COUNT(*) AS internacoes, ROUND(SUM(i.VAL_TOT), 2) AS valor_total
            FROM internacoes i
            JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D
            GROUP BY 1
            ORDER BY internacoes DESC
        """,
        "top_procedimentos": """
            SELECT p.PROC_REA, p.NOME_PROC, COUNT(*) AS ocorrencias
            FROM internacao_procedimento ip
            JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA
            GROUP BY 1, 2
            ORDER BY ocorrencias DESC
            LIMIT 20
        """,
        "top_cid_capitulo": """
            SELECT c.DS_CAPITULO, COUNT(*) AS internacoes
            FROM internacoes i
            JOIN cid c ON i.DIAG_PRINC = c.CID
            GROUP BY 1
            ORDER BY internacoes DESC
            LIMIT 20
        """,
        "top_hospitais": """
            SELECT i.CNES, h.NO_HOSPITAL, COUNT(*) AS internacoes, ROUND(SUM(i.VAL_TOT), 2) AS valor_total
            FROM internacoes i
            LEFT JOIN hospital h ON i.CNES = h.CNES
            GROUP BY 1, 2
            ORDER BY internacoes DESC
            LIMIT 20
        """,
    }
    return {name: fetch_dicts(con, sql) for name, sql in queries.items()}


RELATIONSHIPS = [
    ("internacoes", "CNES", "hospital", "CNES", "Hospital de atendimento pela chave CNES"),
    ("hospital", "MUNIC_MOV", "municipios", "CO_MUNICIPIO_6D", "Municipio de movimento/estabelecimento"),
    ("internacoes", "MUNIC_RES", "municipios", "CO_MUNICIPIO_6D", "Municipio de residencia do usuario"),
    ("internacoes", "SEXO", "sexo", "SEXO", "Sexo do usuario"),
    ("internacoes", "RACA_COR", "raca_cor", "RACA_COR", "Raca/cor informada"),
    ("internacoes", "ETNIA", "etnia", "ETNIA", "Etnia informada"),
    ("internacoes", "NACIONAL", "nacionalidade", "NACIONAL", "Nacionalidade"),
    ("internacoes", "INSTRU", "instrucao", "INSTRU", "Instrucao/escolaridade"),
    ("internacoes", "VINCPREV", "vincprev", "VINCPREV", "Vinculo previdenciario"),
    ("internacoes", "CAR_INT", "car_int", "CAR_INT", "Carater da internacao"),
    ("internacoes", "ESPEC", "especialidade", "ESPEC", "Especialidade/leito"),
    ("internacoes", "COMPLEX", "complexidade", "COMPLEX", "Complexidade do atendimento"),
    ("internacoes", "MARCA_UTI", "marca_uti", "MARCA_UTI", "Marcador/tipo de UTI"),
    ("internacoes", "CBOR", "cbor", "CBOR", "Ocupacao CBO-R"),
    ("internacoes", "DIAG_PRINC", "cid", "CID", "Diagnostico principal CID"),
    ("internacoes", "DIAG_SECUN", "cid", "CID", "Diagnostico secundario CID"),
    ("internacoes", "CID_MORTE", "cid", "CID", "CID da morte"),
    ("internacao_procedimento", "N_AIH", "internacoes", "N_AIH", "Procedimentos vinculados a AIH/internacao"),
    ("internacao_procedimento", "PROC_REA", "procedimentos", "PROC_REA", "Procedimento realizado"),
    ("socioeconomico", "CO_MUNICIPIO_6D", "municipios", "CO_MUNICIPIO_6D", "Indicadores socioeconomicos por municipio"),
]

CANDIDATE_KEY_SPECS = [
    ("car_int", ["CAR_INT"], "Codigo do carater de internacao"),
    ("cbor", ["CBOR"], "Codigo CBO-R"),
    ("cid", ["CID"], "Codigo CID"),
    ("complexidade", ["COMPLEX"], "Codigo de complexidade"),
    ("contraceptivos", ["CONTRACEPTIVO"], "Codigo de metodo contraceptivo"),
    ("especialidade", ["ESPEC"], "Codigo de especialidade"),
    ("etnia", ["ETNIA"], "Codigo de etnia"),
    ("hospital", ["CNES"], "Codigo nacional de estabelecimento de saude"),
    ("instrucao", ["INSTRU"], "Codigo de instrucao"),
    ("internacao_procedimento", ["id_atendimento"], "Identificador tecnico da linha de procedimento"),
    ("internacoes", ["N_AIH"], "Identificador AIH/internacao"),
    ("marca_uti", ["MARCA_UTI"], "Codigo do marcador de UTI"),
    ("municipios", ["CO_MUNICIPIO_6D"], "Codigo municipal de 6 digitos"),
    ("nacionalidade", ["NACIONAL"], "Codigo de nacionalidade"),
    ("procedimentos", ["PROC_REA"], "Codigo de procedimento realizado"),
    ("raca_cor", ["RACA_COR"], "Codigo de raca/cor"),
    ("sexo", ["SEXO"], "Codigo de sexo"),
    ("socioeconomico", ["CO_MUNICIPIO_6D", "NU_ANO"], "Indicador municipal anual"),
    ("stg_hospital", ["CNES"], "Codigo CNES na staging"),
    ("stg_internacoes", ["N_AIH"], "Identificador AIH/internacao na staging"),
    ("stg_sexo", ["SEXO"], "Codigo de sexo na staging"),
    ("tempo", ["data"], "Data calendario"),
    ("vincprev", ["VINCPREV"], "Codigo de vinculo previdenciario"),
]

TOP_VALUE_SPECS = [
    ("internacoes", "CAR_INT", "carater da internacao"),
    ("internacoes", "ESPEC", "especialidade"),
    ("internacoes", "COMPLEX", "complexidade"),
    ("internacoes", "MARCA_UTI", "marcador de UTI"),
    ("internacoes", "SEXO", "sexo"),
    ("internacoes", "RACA_COR", "raca/cor"),
    ("internacoes", "DIAG_PRINC", "diagnostico principal"),
    ("internacoes", "CNES", "hospital"),
    ("internacoes", "MUNIC_RES", "municipio de residencia"),
    ("internacao_procedimento", "PROC_REA", "procedimento realizado"),
    ("hospital", "GESTAO", "gestao hospitalar"),
    ("hospital", "NATUREZA", "natureza hospitalar"),
    ("hospital", "MUNIC_MOV", "municipio do estabelecimento"),
    ("municipios", "SG_UF", "UF"),
    ("socioeconomico", "NU_ANO", "ano socioeconomico"),
]


def relationship_coverage(con: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for left_table, left_key, right_table, right_key, meaning in RELATIONSHIPS:
        started = time.time()
        sql = f"""
            SELECT
              COUNT(*) AS left_rows,
              COUNT(l.{quote_ident(left_key)}) AS non_null_left_key,
              COUNT(r.{quote_ident(right_key)}) AS matched_rows,
              COUNT(*) - COUNT(r.{quote_ident(right_key)}) AS unmatched_rows,
              COUNT(r.{quote_ident(right_key)})::DOUBLE / NULLIF(COUNT(l.{quote_ident(left_key)}), 0) AS match_rate_non_null
            FROM {quote_ident(left_table)} l
            LEFT JOIN {quote_ident(right_table)} r
              ON l.{quote_ident(left_key)} = r.{quote_ident(right_key)}
            WHERE l.{quote_ident(left_key)} IS NOT NULL
        """
        result = fetch_dicts(con, sql)[0]
        match_rate = result["match_rate_non_null"]
        if match_rate is None:
            confidence = "rejected"
        elif match_rate >= 0.995:
            confidence = "confirmed"
        elif match_rate >= 0.95:
            confidence = "likely"
        elif match_rate >= 0.80:
            confidence = "weak"
        else:
            confidence = "rejected"
        rows.append(
            {
                "left_table": left_table,
                "left_key": left_key,
                "right_table": right_table,
                "right_key": right_key,
                "business_meaning": meaning,
                **{k: to_jsonable(v) for k, v in result.items()},
                "confidence": confidence,
                "sql": clean_sql(sql),
                "duration_seconds": round(time.time() - started, 3),
            }
        )
    return rows


def candidate_key_checks(con: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for table_name, key_columns, meaning in CANDIDATE_KEY_SPECS:
        started = time.time()
        base = quote_ident(table_name)
        key_exprs = [quote_ident(col) for col in key_columns]
        null_condition = " OR ".join(f"{expr} IS NULL" for expr in key_exprs)
        if len(key_columns) == 1:
            distinct_sql = f"COUNT(DISTINCT {key_exprs[0]})"
        else:
            grouped_cols = ", ".join(key_exprs)
            distinct_sql = (
                f"(SELECT COUNT(*) FROM (SELECT {grouped_cols} FROM {base} "
                f"WHERE NOT ({null_condition}) GROUP BY {grouped_cols}) keys)"
            )
        sql = f"""
            SELECT
              COUNT(*) AS row_count,
              COUNT(*) FILTER (WHERE {null_condition}) AS null_key_rows,
              {distinct_sql} AS distinct_key_count
            FROM {base}
        """
        result = fetch_dicts(con, sql)[0]
        row_count = result["row_count"]
        null_key_rows = result["null_key_rows"]
        distinct_key_count = result["distinct_key_count"]
        duplicate_key_rows = row_count - null_key_rows - distinct_key_count
        confidence = "confirmed" if null_key_rows == 0 and duplicate_key_rows == 0 else "rejected"
        rows.append(
            {
                "table_name": table_name,
                "candidate_key": ", ".join(key_columns),
                "business_meaning": meaning,
                "row_count": row_count,
                "null_key_rows": null_key_rows,
                "distinct_key_count": distinct_key_count,
                "duplicate_key_rows": duplicate_key_rows,
                "confidence": confidence,
                "sql": clean_sql(sql),
                "duration_seconds": round(time.time() - started, 3),
            }
        )
    return rows


def storage_estimates(con: duckdb.DuckDBPyConnection, tables: list[dict[str, Any]]) -> list[dict[str, Any]]:
    db_size = fetch_dicts(con, "PRAGMA database_size")[0]
    block_size = int(db_size["block_size"])
    rows: list[dict[str, Any]] = []
    for table in tables:
        if table["table_schema"] != "main":
            continue
        started = time.time()
        table_name = table["table_name"]
        block_ids: set[int] = set()
        storage_rows = fetch_dicts(con, f"PRAGMA storage_info({quote_literal(table_name)})")
        for storage_row in storage_rows:
            block_id = storage_row.get("block_id")
            if isinstance(block_id, int) and block_id >= 0:
                block_ids.add(block_id)
            additional = storage_row.get("additional_block_ids") or []
            if isinstance(additional, list):
                block_ids.update(block for block in additional if isinstance(block, int) and block >= 0)
        estimated_bytes = len(block_ids) * block_size
        rows.append(
            {
                "table_schema": table["table_schema"],
                "table_name": table_name,
                "row_count": table["row_count"],
                "persistent_block_count": len(block_ids),
                "estimated_bytes": estimated_bytes,
                "estimated_gib": round(estimated_bytes / (1024**3), 4),
                "database_size": db_size["database_size"],
                "sql": clean_sql(f"PRAGMA storage_info({quote_literal(table_name)})"),
                "duration_seconds": round(time.time() - started, 3),
            }
        )
    return rows


def top_frequent_values(con: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for table_name, column_name, meaning in TOP_VALUE_SPECS:
        started = time.time()
        colref = quote_ident(column_name)
        sql = f"""
            SELECT
              {colref} AS value,
              COUNT(*) AS row_count
            FROM {quote_ident(table_name)}
            GROUP BY 1
            ORDER BY row_count DESC, value
            LIMIT 10
        """
        for rank, item in enumerate(fetch_dicts(con, sql), start=1):
            rows.append(
                {
                    "table_name": table_name,
                    "column_name": column_name,
                    "business_meaning": meaning,
                    "rank": rank,
                    "value": item["value"],
                    "row_count": item["row_count"],
                    "sql": clean_sql(sql),
                    "duration_seconds": round(time.time() - started, 3),
                }
            )
    return rows


def data_quality_checks(con: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    checks = [
        (
            "DQ001",
            "Altas anteriores a internacao",
            "critical",
            "Datas de saida anteriores a entrada quebram analises de permanencia e desfecho.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DT_SAIDA < DT_INTER",
        ),
        (
            "DQ002",
            "DT_INTER fora do periodo 2007-2023",
            "high",
            "O calendario `tempo` cobre 2007-2023; registros fora desse intervalo podem indicar carga historica residual ou erro.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DT_INTER < DATE '2007-01-01' OR DT_INTER > DATE '2023-12-31'",
        ),
        (
            "DQ003",
            "DT_SAIDA fora do periodo 2007-2023",
            "high",
            "Saidas fora do calendario esperado afetam series temporais por competencia/alta.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DT_SAIDA < DATE '2007-01-01' OR DT_SAIDA > DATE '2023-12-31'",
        ),
        (
            "DQ004",
            "DIAS_PERM diferente da diferenca simples entre saida e entrada",
            "medium",
            "Pode ser regra de negocio inclusiva ou divergencia de calculo; deve ser documentado antes de usar como permanencia exata.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DT_INTER IS NOT NULL AND DT_SAIDA IS NOT NULL AND DIAS_PERM <> date_diff('day', DT_INTER, DT_SAIDA)",
        ),
        (
            "DQ005",
            "Valores financeiros negativos",
            "critical",
            "Valores negativos em VAL_SH, VAL_SP, VAL_UTI ou VAL_TOT podem distorcer totais financeiros.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes WHERE VAL_SH < 0 OR VAL_SP < 0 OR VAL_UTI < 0 OR VAL_TOT < 0",
        ),
        (
            "DQ006",
            "Idades fora do intervalo 0-150",
            "critical",
            "Idades impossiveis invalidam analises demograficas e coortes.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes WHERE IDADE < 0 OR IDADE > 150",
        ),
        (
            "DQ007",
            "Internacoes sem CNES",
            "high",
            "CNES ausente impede analise por estabelecimento hospitalar.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes WHERE CNES IS NULL",
        ),
        (
            "DQ008",
            "Internacoes sem diagnostico principal",
            "high",
            "Diagnostico principal ausente limita analises clinicas por CID.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes WHERE DIAG_PRINC IS NULL OR DIAG_PRINC = ''",
        ),
        (
            "DQ009",
            "Internacoes com CNES sem correspondencia em hospital",
            "high",
            "Orfaos de CNES reduzem confianca em rankings e agregacoes por hospital.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES WHERE i.CNES IS NOT NULL AND h.CNES IS NULL",
        ),
        (
            "DQ010",
            "Internacoes com municipio de residencia sem correspondencia",
            "high",
            "Municipios orfaos prejudicam analises territoriais.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes i LEFT JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D WHERE i.MUNIC_RES IS NOT NULL AND m.CO_MUNICIPIO_6D IS NULL",
        ),
        (
            "DQ011",
            "Diagnosticos principais sem correspondencia na tabela CID",
            "high",
            "CIDs orfaos impedem interpretacao clinica por descricao, grupo e capitulo.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes i LEFT JOIN cid c ON i.DIAG_PRINC = c.CID WHERE i.DIAG_PRINC IS NOT NULL AND c.CID IS NULL",
        ),
        (
            "DQ012",
            "Procedimentos realizados sem descricao",
            "high",
            "Procedimentos orfaos impedem interpretacao assistencial do codigo PROC_REA.",
            "SELECT COUNT(*) AS affected_rows FROM internacao_procedimento ip LEFT JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA WHERE ip.PROC_REA IS NOT NULL AND p.PROC_REA IS NULL",
        ),
        (
            "DQ013",
            "Hospitais referenciados sem nome cadastrado",
            "medium",
            "CNES com nome ausente dificulta comunicacao com gestores e auditoria nominal.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes i JOIN hospital h ON i.CNES = h.CNES WHERE h.NO_HOSPITAL IS NULL OR h.NO_HOSPITAL = ''",
        ),
        (
            "DQ014",
            "Tabela sexo possui descricoes duplicadas",
            "medium",
            "Codigos distintos com mesma descricao podem distorcer agrupamentos se o usuario agrupar por descricao sem entender os codigos.",
            "SELECT COUNT(*) AS affected_rows FROM (SELECT DESCRICAO FROM sexo GROUP BY DESCRICAO HAVING COUNT(*) > 1) t",
        ),
        (
            "DQ015",
            "VAL_TOT menor que a soma VAL_SH + VAL_SP + VAL_UTI",
            "medium",
            "Divergencia pode indicar que VAL_TOT nao e soma direta dos componentes ou que ha inconsistencia financeira.",
            "SELECT COUNT(*) AS affected_rows FROM internacoes WHERE VAL_TOT + 0.01 < COALESCE(VAL_SH, 0) + COALESCE(VAL_SP, 0) + COALESCE(VAL_UTI, 0)",
        ),
    ]
    output = []
    for check_id, title, severity, why, sql in checks:
        started = time.time()
        affected_rows = con.execute(clean_sql(sql)).fetchone()[0]
        sample_sql = sample_sql_for_check(check_id)
        sample_rows = fetch_dicts(con, sample_sql) if sample_sql else []
        output.append(
            {
                "id": check_id,
                "title": title,
                "severity": severity,
                "why_it_matters": why,
                "affected_rows": affected_rows,
                "sql": clean_sql(sql),
                "sample_sql": clean_sql(sample_sql) if sample_sql else None,
                "sample_rows": sample_rows[:10],
                "blocks_ground_truth": severity in {"critical", "high"} and affected_rows > 0,
                "duration_seconds": round(time.time() - started, 3),
            }
        )
    return output


def sample_sql_for_check(check_id: str) -> str | None:
    samples = {
        "DQ001": "SELECT N_AIH, DT_INTER, DT_SAIDA, DIAS_PERM FROM internacoes WHERE DT_SAIDA < DT_INTER LIMIT 10",
        "DQ002": "SELECT N_AIH, DT_INTER, DT_SAIDA FROM internacoes WHERE DT_INTER < DATE '2007-01-01' OR DT_INTER > DATE '2023-12-31' ORDER BY DT_INTER LIMIT 10",
        "DQ003": "SELECT N_AIH, DT_INTER, DT_SAIDA FROM internacoes WHERE DT_SAIDA < DATE '2007-01-01' OR DT_SAIDA > DATE '2023-12-31' ORDER BY DT_SAIDA LIMIT 10",
        "DQ004": "SELECT N_AIH, DT_INTER, DT_SAIDA, DIAS_PERM, date_diff('day', DT_INTER, DT_SAIDA) AS diff_dias FROM internacoes WHERE DT_INTER IS NOT NULL AND DT_SAIDA IS NOT NULL AND DIAS_PERM <> date_diff('day', DT_INTER, DT_SAIDA) LIMIT 10",
        "DQ005": "SELECT N_AIH, VAL_SH, VAL_SP, VAL_UTI, VAL_TOT FROM internacoes WHERE VAL_SH < 0 OR VAL_SP < 0 OR VAL_UTI < 0 OR VAL_TOT < 0 LIMIT 10",
        "DQ006": "SELECT N_AIH, NASC, IDADE, DT_INTER FROM internacoes WHERE IDADE < 0 OR IDADE > 150 LIMIT 10",
        "DQ009": "SELECT i.CNES, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES WHERE i.CNES IS NOT NULL AND h.CNES IS NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10",
        "DQ010": "SELECT i.MUNIC_RES, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D WHERE i.MUNIC_RES IS NOT NULL AND m.CO_MUNICIPIO_6D IS NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10",
        "DQ011": "SELECT i.DIAG_PRINC, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN cid c ON i.DIAG_PRINC = c.CID WHERE i.DIAG_PRINC IS NOT NULL AND c.CID IS NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10",
        "DQ012": "SELECT ip.PROC_REA, COUNT(*) AS ocorrencias FROM internacao_procedimento ip LEFT JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA WHERE ip.PROC_REA IS NOT NULL AND p.PROC_REA IS NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 10",
        "DQ013": "SELECT i.CNES, COUNT(*) AS internacoes FROM internacoes i JOIN hospital h ON i.CNES = h.CNES WHERE h.NO_HOSPITAL IS NULL OR h.NO_HOSPITAL = '' GROUP BY 1 ORDER BY 2 DESC LIMIT 10",
        "DQ014": "SELECT DESCRICAO, COUNT(*) AS codigos FROM sexo GROUP BY DESCRICAO HAVING COUNT(*) > 1",
        "DQ015": "SELECT N_AIH, VAL_SH, VAL_SP, VAL_UTI, VAL_TOT, COALESCE(VAL_SH, 0) + COALESCE(VAL_SP, 0) + COALESCE(VAL_UTI, 0) AS soma_componentes FROM internacoes WHERE VAL_TOT + 0.01 < COALESCE(VAL_SH, 0) + COALESCE(VAL_SP, 0) + COALESCE(VAL_UTI, 0) LIMIT 10",
    }
    return samples.get(check_id)


def question_specs() -> list[QuestionSpec]:
    specs: list[QuestionSpec] = []
    l1 = "L1: uma tabela, contagem ou estatistica direta, sem joins."
    l2 = "L2: agregacao, filtro, ordenacao ou ranking em uma tabela."
    l3 = "L3: consulta de negocio com joins validados entre fato e dimensao."
    l4 = "L4: CTE/subconsulta, denominador explicito, comparacao temporal, janela ou multiplas agregacoes."
    l5 = "L5: auditoria ou analise especialista com regras de qualidade, orfaos, inconsistencias ou definicoes alternativas."

    specs.extend(
        [
            q(PERSONAS[2], "Quantas internacoes existem na tabela principal?", "Medir o volume total de registros de internacao disponiveis.", "L1", l1, "SELECT COUNT(*) AS total_internacoes FROM internacoes", "scalar"),
            q(PERSONAS[2], "Quantos registros de procedimentos realizados existem?", "Medir o volume da tabela de procedimentos por internacao.", "L1", l1, "SELECT COUNT(*) AS total_procedimentos_realizados FROM internacao_procedimento", "scalar"),
            q(PERSONAS[2], "Qual e o periodo minimo e maximo de entrada e saida das internacoes?", "Entender a cobertura temporal bruta da base.", "L1", l1, "SELECT MIN(DT_INTER) AS primeira_internacao, MAX(DT_INTER) AS ultima_internacao, MIN(DT_SAIDA) AS primeira_saida, MAX(DT_SAIDA) AS ultima_saida FROM internacoes", "table"),
            q(PERSONAS[4], "Quantos hospitais existem no cadastro de estabelecimentos?", "Medir a cobertura cadastral de CNES/hospitais.", "L1", l1, "SELECT COUNT(*) AS total_hospitais FROM hospital", "scalar"),
            q(PERSONAS[0], "Quantos municipios e quantas UFs aparecem na dimensao territorial?", "Medir a cobertura geografica da dimensao de municipios.", "L1", l1, "SELECT COUNT(*) AS total_municipios, COUNT(DISTINCT SG_UF) AS total_ufs FROM municipios", "table"),
            q(PERSONAS[2], "Quantos procedimentos distintos existem no cadastro de procedimentos?", "Medir a abrangencia do dicionario de procedimentos.", "L1", l1, "SELECT COUNT(*) AS total_procedimentos_cadastrados FROM procedimentos", "scalar"),
            q(PERSONAS[7], "Quantos codigos CID existem na tabela de diagnosticos?", "Medir a abrangencia do dicionario de diagnosticos CID.", "L1", l1, "SELECT COUNT(*) AS total_cids FROM cid", "scalar"),
            q(PERSONAS[7], "Qual e o intervalo de anos dos indicadores socioeconomicos?", "Entender cobertura temporal dos indicadores municipais auxiliares.", "L1", l1, "SELECT MIN(NU_ANO) AS primeiro_ano, MAX(NU_ANO) AS ultimo_ano, COUNT(*) AS registros FROM socioeconomico", "table"),
            q(PERSONAS[5], "Quantas internacoes tiveram morte registrada?", "Medir o volume bruto de obitos hospitalares marcados.", "L1", l1, "SELECT COUNT(*) AS internacoes_com_morte FROM internacoes WHERE MORTE = TRUE", "scalar"),
            q(PERSONAS[6], "Quantas internacoes indicam uso de UTI pelo marcador de UTI?", "Medir volume bruto de uso de UTI.", "L1", l1, "SELECT COUNT(*) AS internacoes_com_uti FROM internacoes WHERE MARCA_UTI <> 0 OR UTI_INT_TO > 0", "scalar"),
            q(PERSONAS[3], "Qual e a menor e a maior idade registradas nas internacoes?", "Avaliar limites demograficos antes de analises por idade.", "L1", l1, "SELECT MIN(IDADE) AS idade_minima, MAX(IDADE) AS idade_maxima FROM internacoes", "table"),
            q(PERSONAS[9], "Qual e o valor total aprovado registrado em VAL_TOT?", "Medir o total financeiro bruto da tabela principal.", "L1", l1, "SELECT ROUND(SUM(VAL_TOT), 2) AS valor_total FROM internacoes", "scalar"),
            q(PERSONAS[2], "Quantos CNES distintos aparecem nas internacoes?", "Medir quantos estabelecimentos sao efetivamente usados nos fatos.", "L1", l1, "SELECT COUNT(DISTINCT CNES) AS cnes_distintos FROM internacoes", "scalar"),
            q(PERSONAS[2], "Quantos municipios de residencia distintos aparecem nas internacoes?", "Medir cobertura territorial efetiva dos fatos.", "L1", l1, "SELECT COUNT(DISTINCT MUNIC_RES) AS municipios_residencia_distintos FROM internacoes", "scalar"),
            q(PERSONAS[2], "Quantos dias existem na dimensao tempo?", "Medir cobertura do calendario analitico.", "L1", l1, "SELECT COUNT(*) AS dias_calendario, MIN(data) AS data_inicial, MAX(data) AS data_final FROM tempo", "table"),
        ]
    )

    specs.extend(
        [
            q(PERSONAS[1], "Quantas internacoes ocorreram por ano de entrada?", "Acompanhar volume anual de internacoes.", "L2", l2, "SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[1], "Qual foi o valor total por ano de entrada?", "Acompanhar gasto/reembolso anual.", "L2", l2, "SELECT year(DT_INTER) AS ano, ROUND(SUM(VAL_TOT), 2) AS valor_total FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[5], "Quantas mortes hospitalares foram registradas por ano?", "Acompanhar desfechos de obito ao longo do tempo.", "L2", l2, "SELECT year(DT_INTER) AS ano, COUNT(*) FILTER (WHERE MORTE) AS mortes FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[5], "Qual foi a taxa bruta de mortalidade hospitalar por ano?", "Comparar desfecho de morte usando internacoes como denominador.", "L2", l2, "SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE MORTE) AS mortes, ROUND(100.0 * COUNT(*) FILTER (WHERE MORTE) / COUNT(*), 4) AS taxa_morte_pct FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[9], "Qual foi o valor medio por internacao em cada ano?", "Monitorar custo medio bruto anual.", "L2", l2, "SELECT year(DT_INTER) AS ano, ROUND(AVG(VAL_TOT), 2) AS valor_medio FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[4], "Quais CNES concentraram mais internacoes?", "Identificar estabelecimentos com maior volume usando codigo CNES.", "L2", l2, "SELECT CNES, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[5], "Quais codigos de diagnostico principal foram mais frequentes?", "Identificar principais CIDs em volume bruto.", "L2", l2, "SELECT DIAG_PRINC, COUNT(*) AS internacoes FROM internacoes WHERE DIAG_PRINC IS NOT NULL GROUP BY 1 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[8], "Como as internacoes se distribuem por carater de internacao?", "Avaliar mix entre eletivo, urgencia e acidentes usando codigo bruto.", "L2", l2, "SELECT CAR_INT, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[5], "Como as internacoes se distribuem por codigo de sexo?", "Avaliar distribuicao demografica basica por codigo.", "L2", l2, "SELECT SEXO, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY SEXO", "distribution"),
            q(PERSONAS[5], "Como as internacoes se distribuem por codigo de raca/cor?", "Avaliar distribuicao demografica basica por raca/cor.", "L2", l2, "SELECT RACA_COR, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY RACA_COR", "distribution"),
            q(PERSONAS[5], "Qual e a distribuicao das internacoes por faixa etaria?", "Preparar analise populacional por grupos de idade.", "L2", l2, "SELECT CASE WHEN IDADE < 1 THEN '00_<1' WHEN IDADE BETWEEN 1 AND 4 THEN '01_1_4' WHEN IDADE BETWEEN 5 AND 14 THEN '02_5_14' WHEN IDADE BETWEEN 15 AND 24 THEN '03_15_24' WHEN IDADE BETWEEN 25 AND 44 THEN '04_25_44' WHEN IDADE BETWEEN 45 AND 64 THEN '05_45_64' WHEN IDADE >= 65 THEN '06_65_plus' ELSE '99_ignorado' END AS faixa_etaria, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY 1", "distribution"),
            q(PERSONAS[6], "Como as internacoes se distribuem por complexidade do atendimento?", "Avaliar mix de atencao basica, media e alta complexidade no codigo bruto.", "L2", l2, "SELECT COMPLEX, COUNT(*) AS internacoes, ROUND(SUM(VAL_TOT), 2) AS valor_total FROM internacoes GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[6], "Como as internacoes se distribuem pelo marcador de UTI?", "Entender uso de UTI por codigo bruto.", "L2", l2, "SELECT MARCA_UTI, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[6], "Qual foi a media de dias de permanencia por ano?", "Acompanhar permanencia hospitalar media no tempo.", "L2", l2, "SELECT year(DT_INTER) AS ano, ROUND(AVG(DIAS_PERM), 2) AS media_dias_permanencia FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[6], "Qual e a distribuicao de permanencia em faixas de dias?", "Entender concentracao de internacoes curtas e longas.", "L2", l2, "SELECT CASE WHEN DIAS_PERM = 0 THEN '00_0' WHEN DIAS_PERM BETWEEN 1 AND 3 THEN '01_1_3' WHEN DIAS_PERM BETWEEN 4 AND 7 THEN '02_4_7' WHEN DIAS_PERM BETWEEN 8 AND 14 THEN '03_8_14' WHEN DIAS_PERM BETWEEN 15 AND 30 THEN '04_15_30' WHEN DIAS_PERM > 30 THEN '05_31_plus' ELSE '99_ignorado' END AS faixa_dias, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY 1", "distribution"),
            q(PERSONAS[9], "Qual foi o valor total por codigo de complexidade?", "Comparar volume financeiro por nivel de complexidade.", "L2", l2, "SELECT COMPLEX, ROUND(SUM(VAL_TOT), 2) AS valor_total, COUNT(*) AS internacoes FROM internacoes GROUP BY 1 ORDER BY valor_total DESC", "distribution"),
            q(PERSONAS[5], "Quantas internacoes com gestacao de risco foram registradas por ano?", "Monitorar marcador de gestacao de risco no tempo.", "L2", l2, "SELECT year(DT_INTER) AS ano, COUNT(*) FILTER (WHERE GESTRISCO) AS gestacao_risco FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[6], "Quantos dias de UTI foram registrados por ano?", "Acompanhar intensidade anual de uso de UTI.", "L2", l2, "SELECT year(DT_INTER) AS ano, SUM(UTI_INT_TO) AS dias_uti FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[1], "Quantas internacoes ocorreram por mes calendario?", "Avaliar sazonalidade mensal bruta.", "L2", l2, "SELECT year(DT_INTER) AS ano, month(DT_INTER) AS mes, COUNT(*) AS internacoes FROM internacoes GROUP BY 1, 2 ORDER BY 1, 2", "time_series"),
            q(PERSONAS[1], "Quantas saidas hospitalares ocorreram por ano?", "Comparar series por data de saida.", "L2", l2, "SELECT year(DT_SAIDA) AS ano_saida, COUNT(*) AS saidas FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[2], "Quais codigos PROC_REA aparecem mais na tabela de procedimentos realizados?", "Identificar procedimentos mais frequentes por codigo bruto.", "L2", l2, "SELECT PROC_REA, COUNT(*) AS ocorrencias FROM internacao_procedimento GROUP BY 1 ORDER BY ocorrencias DESC LIMIT 20", "ranking"),
            q(PERSONAS[1], "Qual e a populacao total registrada por ano nos indicadores socioeconomicos?", "Entender denominadores populacionais disponiveis.", "L2", l2, "SELECT NU_ANO AS ano, SUM(QT_POPULACAO) AS populacao_total FROM socioeconomico GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[6], "Quantos leitos SUS estao registrados por ano nos indicadores socioeconomicos?", "Acompanhar capacidade assistencial agregada.", "L2", l2, "SELECT NU_ANO AS ano, SUM(QT_LEITOS_SUS) AS leitos_sus FROM socioeconomico GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[0], "Quantos municipios existem por UF no cadastro territorial?", "Medir cobertura territorial por estado.", "L2", l2, "SELECT SG_UF, COUNT(*) AS municipios FROM municipios GROUP BY 1 ORDER BY municipios DESC, SG_UF", "distribution"),
            q(PERSONAS[4], "Quantos hospitais existem por tipo de gestao cadastral?", "Entender distribuicao dos estabelecimentos por codigo de gestao.", "L2", l2, "SELECT GESTAO, COUNT(*) AS hospitais FROM hospital GROUP BY 1 ORDER BY hospitais DESC", "distribution"),
        ]
    )

    specs.extend(
        [
            q(PERSONAS[1], "Quantas internacoes e qual valor total por UF de residencia?", "Comparar volume e valor financeiro por estado de residencia.", "L3", l3, "SELECT m.SG_UF, COUNT(*) AS internacoes, ROUND(SUM(i.VAL_TOT), 2) AS valor_total FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[1], "Quantas internacoes ocorreram por UF do hospital?", "Comparar producao assistencial por estado do estabelecimento.", "L3", l3, "SELECT mh.SG_UF, COUNT(*) AS internacoes FROM internacoes i JOIN hospital h ON i.CNES = h.CNES JOIN municipios mh ON h.MUNIC_MOV = mh.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[5], "Como as internacoes se distribuem por sexo descrito?", "Usar a dimensao de sexo para resultado interpretavel.", "L3", l3, "SELECT s.DESCRICAO AS sexo, COUNT(*) AS internacoes FROM internacoes i JOIN sexo s ON i.SEXO = s.SEXO GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[5], "Como as internacoes se distribuem por raca/cor descrita?", "Usar a dimensao de raca/cor para resultado interpretavel.", "L3", l3, "SELECT r.DESCRICAO AS raca_cor, COUNT(*) AS internacoes FROM internacoes i JOIN raca_cor r ON i.RACA_COR = r.RACA_COR GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[8], "Quantas internacoes ocorreram por descricao do carater de internacao?", "Interpretar eletivo, urgencia e acidentes com descricao.", "L3", l3, "SELECT c.DESCRICAO AS carater_internacao, COUNT(*) AS internacoes FROM internacoes i JOIN car_int c ON i.CAR_INT = c.CAR_INT GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[6], "Quais especialidades tiveram maior volume de internacoes?", "Identificar especialidades/leitos mais demandados.", "L3", l3, "SELECT e.DESCRICAO AS especialidade, COUNT(*) AS internacoes FROM internacoes i JOIN especialidade e ON i.ESPEC = e.ESPEC GROUP BY 1 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[6], "Quantas internacoes existem por descricao de complexidade?", "Interpretar o mix de complexidade com descricao oficial da dimensao.", "L3", l3, "SELECT c.DESCRICAO AS complexidade, COUNT(*) AS internacoes, ROUND(SUM(i.VAL_TOT), 2) AS valor_total FROM internacoes i JOIN complexidade c ON i.COMPLEX = c.COMPLEX GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[6], "Quais tipos de UTI aparecem mais nas internacoes?", "Interpretar o marcador de UTI por descricao.", "L3", l3, "SELECT mu.DESCRICAO AS marca_uti, COUNT(*) AS internacoes FROM internacoes i JOIN marca_uti mu ON i.MARCA_UTI = mu.MARCA_UTI GROUP BY 1 ORDER BY internacoes DESC", "distribution"),
            q(PERSONAS[2], "Quais procedimentos realizados foram mais frequentes por descricao?", "Identificar procedimentos principais em linguagem de negocio.", "L3", l3, "SELECT p.NOME_PROC, COUNT(*) AS ocorrencias FROM internacao_procedimento ip JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1 ORDER BY ocorrencias DESC LIMIT 20", "ranking"),
            q(PERSONAS[5], "Quais diagnosticos principais foram mais frequentes por descricao CID?", "Interpretar diagnosticos principais com descricao.", "L3", l3, "SELECT c.CID, c.DESCRICAO, COUNT(*) AS internacoes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[5], "Quais capitulos CID concentraram mais internacoes?", "Analisar perfil clinico agregado por capitulo CID.", "L3", l3, "SELECT c.DS_CAPITULO, COUNT(*) AS internacoes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID GROUP BY 1 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[4], "Quais hospitais tiveram maior volume de internacoes?", "Criar ranking nominal de hospitais por volume.", "L3", l3, "SELECT i.CNES, h.NO_HOSPITAL, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[0], "Quais municipios de residencia tiveram mais internacoes?", "Identificar municipios de maior demanda por residencia.", "L3", l3, "SELECT m.SG_UF, m.NO_MUNICIPIO, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[1], "Quais regioes de saude tiveram mais internacoes por residencia?", "Apoiar planejamento regional de rede assistencial.", "L3", l3, "SELECT m.SG_UF, m.NO_REGIAO_SAUDE, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[5], "Qual e a taxa de mortalidade hospitalar por UF de residencia?", "Comparar desfecho de morte usando UF de residencia.", "L3", l3, "SELECT m.SG_UF, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE i.MORTE) AS mortes, ROUND(100.0 * COUNT(*) FILTER (WHERE i.MORTE) / COUNT(*), 4) AS taxa_morte_pct FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY taxa_morte_pct DESC", "distribution"),
            q(PERSONAS[6], "Qual e a media de permanencia por UF de residencia?", "Comparar permanencia media entre estados.", "L3", l3, "SELECT m.SG_UF, ROUND(AVG(i.DIAS_PERM), 2) AS media_dias_permanencia, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY media_dias_permanencia DESC", "distribution"),
            q(PERSONAS[9], "Qual e o valor medio por internacao em cada UF de residencia?", "Comparar custo medio bruto entre estados.", "L3", l3, "SELECT m.SG_UF, ROUND(AVG(i.VAL_TOT), 2) AS valor_medio, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1 ORDER BY valor_medio DESC", "distribution"),
            q(PERSONAS[1], "Quais procedimentos por descricao tiveram maior valor total?", "Identificar procedimentos que mais concentram valor aprovado.", "L3", l3, "SELECT p.NOME_PROC, COUNT(*) AS ocorrencias, ROUND(SUM(i.VAL_TOT), 2) AS valor_total FROM internacao_procedimento ip JOIN internacoes i ON ip.N_AIH = i.N_AIH JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1 ORDER BY valor_total DESC LIMIT 20", "ranking"),
            q(PERSONAS[1], "Quais municipios dos hospitais tiveram mais internacoes?", "Analisar producao por municipio de atendimento.", "L3", l3, "SELECT mh.SG_UF, mh.NO_MUNICIPIO, COUNT(*) AS internacoes FROM internacoes i JOIN hospital h ON i.CNES = h.CNES JOIN municipios mh ON h.MUNIC_MOV = mh.CO_MUNICIPIO_6D GROUP BY 1, 2 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[4], "Quais hospitais tiveram maior valor total registrado?", "Rankear estabelecimentos por valor aprovado.", "L3", l3, "SELECT i.CNES, h.NO_HOSPITAL, ROUND(SUM(i.VAL_TOT), 2) AS valor_total, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES GROUP BY 1, 2 ORDER BY valor_total DESC LIMIT 20", "ranking"),
            q(PERSONAS[5], "Como as internacoes por sexo se distribuem em cada UF?", "Cruzar sexo e territorio para analise demografica regional.", "L3", l3, "SELECT m.SG_UF, s.DESCRICAO AS sexo, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D JOIN sexo s ON i.SEXO = s.SEXO GROUP BY 1, 2 ORDER BY 1, internacoes DESC", "table"),
            q(PERSONAS[1], "Como a complexidade das internacoes se distribui em cada UF?", "Comparar mix assistencial por estado.", "L3", l3, "SELECT m.SG_UF, c.DESCRICAO AS complexidade, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D JOIN complexidade c ON i.COMPLEX = c.COMPLEX GROUP BY 1, 2 ORDER BY 1, internacoes DESC", "table"),
            q(PERSONAS[5], "Quais grupos CID foram mais frequentes entre internacoes femininas?", "Analisar perfil clinico de internacoes femininas.", "L3", l3, "SELECT c.DS_GRUPO, COUNT(*) AS internacoes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID JOIN sexo s ON i.SEXO = s.SEXO WHERE s.DESCRICAO = 'Feminino' GROUP BY 1 ORDER BY internacoes DESC LIMIT 20", "ranking"),
            q(PERSONAS[7], "Qual e a populacao e o total de internacoes por UF e ano quando ha denominador socioeconomico?", "Conectar fatos assistenciais a denominadores populacionais agregados.", "L3", l3, "SELECT m.SG_UF, se.NU_ANO AS ano, SUM(se.QT_POPULACAO) AS populacao, COUNT(i.N_AIH) AS internacoes FROM socioeconomico se JOIN municipios m ON se.CO_MUNICIPIO_6D = m.CO_MUNICIPIO_6D LEFT JOIN internacoes i ON i.MUNIC_RES = se.CO_MUNICIPIO_6D AND year(i.DT_INTER) = se.NU_ANO GROUP BY 1, 2 ORDER BY 1, 2", "table"),
            q(PERSONAS[0], "Quais municipios tiveram maior valor total por residencia?", "Identificar territorios de residencia com maior concentracao financeira.", "L3", l3, "SELECT m.SG_UF, m.NO_MUNICIPIO, ROUND(SUM(i.VAL_TOT), 2) AS valor_total, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2 ORDER BY valor_total DESC LIMIT 20", "ranking"),
        ]
    )

    specs.extend(
        [
            q(PERSONAS[1], "Qual foi a variacao ano contra ano no volume de internacoes?", "Medir crescimento ou queda anual em internacoes.", "L4", l4, "WITH anual AS (SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes FROM internacoes GROUP BY 1) SELECT ano, internacoes, internacoes - LAG(internacoes) OVER (ORDER BY ano) AS diff_abs, ROUND(100.0 * (internacoes - LAG(internacoes) OVER (ORDER BY ano)) / NULLIF(LAG(internacoes) OVER (ORDER BY ano), 0), 4) AS diff_pct FROM anual ORDER BY ano", "time_series"),
            q(PERSONAS[9], "Qual foi a variacao ano contra ano do valor total?", "Medir crescimento financeiro anual.", "L4", l4, "WITH anual AS (SELECT year(DT_INTER) AS ano, SUM(VAL_TOT) AS valor_total FROM internacoes GROUP BY 1) SELECT ano, ROUND(valor_total, 2) AS valor_total, ROUND(valor_total - LAG(valor_total) OVER (ORDER BY ano), 2) AS diff_abs, ROUND(100.0 * (valor_total - LAG(valor_total) OVER (ORDER BY ano)) / NULLIF(LAG(valor_total) OVER (ORDER BY ano), 0), 4) AS diff_pct FROM anual ORDER BY ano", "time_series"),
            q(PERSONAS[1], "Qual e a media movel de 3 meses das internacoes?", "Suavizar sazonalidade mensal para monitoramento.", "L4", l4, "WITH mensal AS (SELECT date_trunc('month', DT_INTER) AS mes_ref, COUNT(*) AS internacoes FROM internacoes GROUP BY 1) SELECT mes_ref, internacoes, ROUND(AVG(internacoes) OVER (ORDER BY mes_ref ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS media_movel_3m FROM mensal ORDER BY mes_ref", "time_series"),
            q(PERSONAS[5], "Quais UFs tiveram maior taxa de mortalidade entre UFs com pelo menos 100 mil internacoes?", "Evitar rankings instaveis por baixo denominador.", "L4", l4, "WITH uf AS (SELECT m.SG_UF, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE i.MORTE) AS mortes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1) SELECT SG_UF, internacoes, mortes, ROUND(100.0 * mortes / internacoes, 4) AS taxa_morte_pct FROM uf WHERE internacoes >= 100000 ORDER BY taxa_morte_pct DESC", "ranking"),
            q(PERSONAS[9], "Quais procedimentos tiveram maior valor medio por ocorrencia entre os com pelo menos 10 mil ocorrencias?", "Identificar procedimentos de alto custo medio com volume relevante.", "L4", l4, "WITH proc AS (SELECT p.NOME_PROC, COUNT(*) AS ocorrencias, AVG(i.VAL_TOT) AS valor_medio FROM internacao_procedimento ip JOIN internacoes i ON ip.N_AIH = i.N_AIH JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1) SELECT NOME_PROC, ocorrencias, ROUND(valor_medio, 2) AS valor_medio FROM proc WHERE ocorrencias >= 10000 ORDER BY valor_medio DESC LIMIT 20", "ranking"),
            q(PERSONAS[3], "Quais hospitais estao acima do percentil 95 de volume de internacoes?", "Identificar estabelecimentos extremamente concentradores de volume.", "L4", l4, "WITH hosp AS (SELECT i.CNES, h.NO_HOSPITAL, COUNT(*) AS internacoes FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES GROUP BY 1, 2), limiar AS (SELECT quantile_cont(internacoes, 0.95) AS p95 FROM hosp) SELECT hosp.CNES, hosp.NO_HOSPITAL, hosp.internacoes, limiar.p95 FROM hosp, limiar WHERE hosp.internacoes >= limiar.p95 ORDER BY hosp.internacoes DESC", "ranking"),
            q(PERSONAS[6], "Quais especialidades tiveram maior permanencia media entre as com pelo menos 100 mil internacoes?", "Comparar permanencia evitando especialidades raras.", "L4", l4, "WITH esp AS (SELECT e.DESCRICAO AS especialidade, COUNT(*) AS internacoes, AVG(i.DIAS_PERM) AS media_dias FROM internacoes i JOIN especialidade e ON i.ESPEC = e.ESPEC GROUP BY 1) SELECT especialidade, internacoes, ROUND(media_dias, 2) AS media_dias FROM esp WHERE internacoes >= 100000 ORDER BY media_dias DESC LIMIT 20", "ranking"),
            q(PERSONAS[5], "Qual proporcao das mortes vem de cada capitulo CID?", "Entender concentracao de obitos por grupo clinico amplo.", "L4", l4, "WITH mortes AS (SELECT c.DS_CAPITULO, COUNT(*) AS mortes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID WHERE i.MORTE GROUP BY 1), total AS (SELECT SUM(mortes) AS total_mortes FROM mortes) SELECT DS_CAPITULO, mortes, ROUND(100.0 * mortes / total_mortes, 4) AS proporcao_mortes_pct FROM mortes, total ORDER BY mortes DESC", "distribution"),
            q(PERSONAS[6], "Quais foram os percentis de permanencia por ano?", "Entender distribuicao da permanencia alem da media.", "L4", l4, "SELECT year(DT_INTER) AS ano, quantile_cont(DIAS_PERM, 0.5) AS p50_dias, quantile_cont(DIAS_PERM, 0.9) AS p90_dias, quantile_cont(DIAS_PERM, 0.99) AS p99_dias FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[1], "Qual foi a taxa de internacoes por 1.000 habitantes por UF e ano?", "Usar denominador populacional para comparacao territorial.", "L4", l4, "WITH internacoes_uf AS (SELECT m.SG_UF, year(i.DT_INTER) AS ano, COUNT(*) AS internacoes FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2), pop_uf AS (SELECT m.SG_UF, se.NU_ANO AS ano, SUM(se.QT_POPULACAO) AS populacao FROM socioeconomico se JOIN municipios m ON se.CO_MUNICIPIO_6D = m.CO_MUNICIPIO_6D GROUP BY 1, 2) SELECT p.SG_UF, p.ano, p.populacao, COALESCE(i.internacoes, 0) AS internacoes, ROUND(1000.0 * COALESCE(i.internacoes, 0) / NULLIF(p.populacao, 0), 4) AS internacoes_por_1000 FROM pop_uf p LEFT JOIN internacoes_uf i ON p.SG_UF = i.SG_UF AND p.ano = i.ano ORDER BY p.SG_UF, p.ano", "table"),
            q(PERSONAS[9], "Qual foi o valor total por habitante por UF e ano?", "Comparar intensidade financeira com denominador populacional.", "L4", l4, "WITH valor_uf AS (SELECT m.SG_UF, year(i.DT_INTER) AS ano, SUM(i.VAL_TOT) AS valor_total FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D GROUP BY 1, 2), pop_uf AS (SELECT m.SG_UF, se.NU_ANO AS ano, SUM(se.QT_POPULACAO) AS populacao FROM socioeconomico se JOIN municipios m ON se.CO_MUNICIPIO_6D = m.CO_MUNICIPIO_6D GROUP BY 1, 2) SELECT p.SG_UF, p.ano, ROUND(COALESCE(v.valor_total, 0), 2) AS valor_total, p.populacao, ROUND(COALESCE(v.valor_total, 0) / NULLIF(p.populacao, 0), 4) AS valor_por_habitante FROM pop_uf p LEFT JOIN valor_uf v ON p.SG_UF = v.SG_UF AND p.ano = v.ano ORDER BY p.SG_UF, p.ano", "table"),
            q(PERSONAS[5], "Quais capitulos CID tiveram maior taxa de mortalidade com pelo menos 100 mil internacoes?", "Comparar risco de morte por capitulo com denominador minimo.", "L4", l4, "WITH cap AS (SELECT c.DS_CAPITULO, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE i.MORTE) AS mortes FROM internacoes i JOIN cid c ON i.DIAG_PRINC = c.CID GROUP BY 1) SELECT DS_CAPITULO, internacoes, mortes, ROUND(100.0 * mortes / internacoes, 4) AS taxa_morte_pct FROM cap WHERE internacoes >= 100000 ORDER BY taxa_morte_pct DESC", "ranking"),
            q(PERSONAS[1], "Qual foi o procedimento mais frequente em cada UF de residencia?", "Identificar o procedimento dominante por estado.", "L4", l4, "WITH proc_uf AS (SELECT m.SG_UF, p.NOME_PROC, COUNT(*) AS ocorrencias, ROW_NUMBER() OVER (PARTITION BY m.SG_UF ORDER BY COUNT(*) DESC) AS rn FROM internacao_procedimento ip JOIN internacoes i ON ip.N_AIH = i.N_AIH JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1, 2) SELECT SG_UF, NOME_PROC, ocorrencias FROM proc_uf WHERE rn = 1 ORDER BY SG_UF", "table"),
            q(PERSONAS[1], "Qual hospital teve maior volume em cada UF do estabelecimento?", "Identificar lideres de producao por estado de atendimento.", "L4", l4, "WITH hosp_uf AS (SELECT mh.SG_UF, i.CNES, h.NO_HOSPITAL, COUNT(*) AS internacoes, ROW_NUMBER() OVER (PARTITION BY mh.SG_UF ORDER BY COUNT(*) DESC) AS rn FROM internacoes i JOIN hospital h ON i.CNES = h.CNES JOIN municipios mh ON h.MUNIC_MOV = mh.CO_MUNICIPIO_6D GROUP BY 1, 2, 3) SELECT SG_UF, CNES, NO_HOSPITAL, internacoes FROM hosp_uf WHERE rn = 1 ORDER BY SG_UF", "table"),
            q(PERSONAS[9], "Como variou ano a ano o valor total por complexidade?", "Acompanhar crescimento financeiro por nivel de complexidade.", "L4", l4, "WITH anual AS (SELECT c.DESCRICAO AS complexidade, year(i.DT_INTER) AS ano, SUM(i.VAL_TOT) AS valor_total FROM internacoes i JOIN complexidade c ON i.COMPLEX = c.COMPLEX GROUP BY 1, 2) SELECT complexidade, ano, ROUND(valor_total, 2) AS valor_total, ROUND(valor_total - LAG(valor_total) OVER (PARTITION BY complexidade ORDER BY ano), 2) AS diff_abs FROM anual ORDER BY complexidade, ano", "time_series"),
            q(PERSONAS[6], "Qual foi a taxa de uso de UTI por ano?", "Medir proporcao anual de internacoes com marcador de UTI.", "L4", l4, "SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes, COUNT(*) FILTER (WHERE MARCA_UTI <> 0 OR UTI_INT_TO > 0) AS com_uti, ROUND(100.0 * COUNT(*) FILTER (WHERE MARCA_UTI <> 0 OR UTI_INT_TO > 0) / COUNT(*), 4) AS taxa_uti_pct FROM internacoes GROUP BY 1 ORDER BY 1", "time_series"),
            q(PERSONAS[8], "Qual foi o mix percentual de carater de internacao por ano?", "Comparar eletivo/urgencia/acidentes no tempo.", "L4", l4, "WITH base AS (SELECT year(i.DT_INTER) AS ano, c.DESCRICAO AS carater, COUNT(*) AS internacoes FROM internacoes i JOIN car_int c ON i.CAR_INT = c.CAR_INT GROUP BY 1, 2), total AS (SELECT ano, SUM(internacoes) AS total_ano FROM base GROUP BY 1) SELECT b.ano, b.carater, b.internacoes, ROUND(100.0 * b.internacoes / t.total_ano, 4) AS percentual_ano FROM base b JOIN total t ON b.ano = t.ano ORDER BY b.ano, percentual_ano DESC", "time_series"),
            q(PERSONAS[5], "Como evoluiram as internacoes obstetricas por ano?", "Monitorar linhas de cuidado obstetricas pela especialidade.", "L4", l4, "SELECT year(i.DT_INTER) AS ano, e.DESCRICAO AS especialidade, COUNT(*) AS internacoes FROM internacoes i JOIN especialidade e ON i.ESPEC = e.ESPEC WHERE e.DESCRICAO ILIKE '%OBSTETRICIA%' GROUP BY 1, 2 ORDER BY 1, 2", "time_series"),
            q(PERSONAS[1], "Quantas internacoes ocorreram em UF de residencia diferente da UF do hospital?", "Medir deslocamento interestadual entre residencia e atendimento.", "L4", l4, "WITH fluxo AS (SELECT mr.SG_UF AS uf_residencia, mh.SG_UF AS uf_hospital, COUNT(*) AS internacoes FROM internacoes i JOIN municipios mr ON i.MUNIC_RES = mr.CO_MUNICIPIO_6D JOIN hospital h ON i.CNES = h.CNES JOIN municipios mh ON h.MUNIC_MOV = mh.CO_MUNICIPIO_6D GROUP BY 1, 2) SELECT uf_residencia, uf_hospital, internacoes FROM fluxo WHERE uf_residencia <> uf_hospital ORDER BY internacoes DESC LIMIT 30", "ranking"),
            q(PERSONAS[2], "Quais anos tem meses faltantes na serie de internacoes por entrada?", "Auditar completude mensal da serie temporal.", "L4", l4, "WITH meses AS (SELECT year(DT_INTER) AS ano, COUNT(DISTINCT month(DT_INTER)) AS meses_com_dados FROM internacoes GROUP BY 1) SELECT ano, meses_com_dados, 12 - meses_com_dados AS meses_faltantes FROM meses ORDER BY ano", "data_quality_finding"),
        ]
    )

    specs.extend(
        [
            q(PERSONAS[3], "Existem internacoes com data de saida anterior a data de entrada?", "Detectar erro temporal critico.", "L5", l5, "SELECT COUNT(*) AS registros_invalidos FROM internacoes WHERE DT_SAIDA < DT_INTER", "data_quality_finding", notes="Se maior que zero, bloquear perguntas de permanencia sem filtro ou caveat."),
            q(PERSONAS[3], "Quantas internacoes tem DIAS_PERM diferente da diferenca simples entre saida e entrada?", "Avaliar se DIAS_PERM pode ser usado como permanencia sem regra adicional.", "L5", l5, "SELECT COUNT(*) AS divergencias FROM internacoes WHERE DT_INTER IS NOT NULL AND DT_SAIDA IS NOT NULL AND DIAS_PERM <> date_diff('day', DT_INTER, DT_SAIDA)", "data_quality_finding", notes="Pode refletir regra inclusiva do SIH; exige documentacao antes de chamar de erro."),
            q(PERSONAS[3], "Existem valores financeiros negativos nos campos de valor?", "Detectar problemas financeiros criticos.", "L5", l5, "SELECT COUNT(*) AS registros_com_valor_negativo FROM internacoes WHERE VAL_SH < 0 OR VAL_SP < 0 OR VAL_UTI < 0 OR VAL_TOT < 0", "data_quality_finding"),
            q(PERSONAS[5], "Existem idades fora do intervalo aceito de 0 a 150 anos?", "Validar campo etario antes de analises demograficas.", "L5", l5, "SELECT COUNT(*) AS idades_invalidas FROM internacoes WHERE IDADE < 0 OR IDADE > 150", "data_quality_finding"),
            q(PERSONAS[2], "Quantos CNES das internacoes nao existem no cadastro hospitalar?", "Medir orfandade do relacionamento internacao-hospital.", "L5", l5, "SELECT COUNT(*) AS internacoes_cnes_orfao FROM internacoes i LEFT JOIN hospital h ON i.CNES = h.CNES WHERE i.CNES IS NOT NULL AND h.CNES IS NULL", "data_quality_finding"),
            q(PERSONAS[0], "Quantas internacoes tem municipio de residencia sem cadastro territorial?", "Medir orfandade territorial.", "L5", l5, "SELECT COUNT(*) AS internacoes_municipio_orfao FROM internacoes i LEFT JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D WHERE i.MUNIC_RES IS NOT NULL AND m.CO_MUNICIPIO_6D IS NULL", "data_quality_finding"),
            q(PERSONAS[5], "Quantos diagnosticos principais nao existem na tabela CID?", "Medir perda de interpretabilidade clinica.", "L5", l5, "SELECT COUNT(*) AS diagnosticos_principais_orfaos FROM internacoes i LEFT JOIN cid c ON i.DIAG_PRINC = c.CID WHERE i.DIAG_PRINC IS NOT NULL AND c.CID IS NULL", "data_quality_finding"),
            q(PERSONAS[2], "Quantos procedimentos realizados nao existem no cadastro de procedimentos?", "Medir orfandade de procedimentos.", "L5", l5, "SELECT COUNT(*) AS procedimentos_orfaos FROM internacao_procedimento ip LEFT JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA WHERE ip.PROC_REA IS NOT NULL AND p.PROC_REA IS NULL", "data_quality_finding"),
            q(PERSONAS[5], "A dimensao sexo possui descricoes duplicadas entre codigos?", "Identificar risco de agrupamento errado por descricao.", "L5", l5, "SELECT DESCRICAO, COUNT(*) AS quantidade_codigos FROM sexo GROUP BY DESCRICAO HAVING COUNT(*) > 1", "data_quality_finding"),
            q(PERSONAS[9], "Quantas internacoes tem VAL_TOT menor que VAL_SH + VAL_SP + VAL_UTI?", "Testar consistencia financeira entre total e componentes.", "L5", l5, "SELECT COUNT(*) AS divergencias_financeiras FROM internacoes WHERE VAL_TOT + 0.01 < COALESCE(VAL_SH, 0) + COALESCE(VAL_SP, 0) + COALESCE(VAL_UTI, 0)", "data_quality_finding", notes="Pode indicar que VAL_TOT nao deve ser interpretado como soma direta desses tres componentes."),
            q(PERSONAS[2], "Quantas internacoes tem data de entrada fora da dimensao tempo?", "Verificar cobertura do calendario para DT_INTER.", "L5", l5, "SELECT COUNT(*) AS dt_inter_sem_tempo FROM internacoes i LEFT JOIN tempo t ON i.DT_INTER = t.data WHERE i.DT_INTER IS NOT NULL AND t.data IS NULL", "data_quality_finding"),
            q(PERSONAS[2], "Quantas internacoes tem data de saida fora da dimensao tempo?", "Verificar cobertura do calendario para DT_SAIDA.", "L5", l5, "SELECT COUNT(*) AS dt_saida_sem_tempo FROM internacoes i LEFT JOIN tempo t ON i.DT_SAIDA = t.data WHERE i.DT_SAIDA IS NOT NULL AND t.data IS NULL", "data_quality_finding"),
            q(PERSONAS[4], "Quais CNES sem nome cadastrado concentram mais internacoes?", "Avaliar impacto pratico de hospitais sem nome.", "L5", l5, "SELECT i.CNES, COUNT(*) AS internacoes FROM internacoes i JOIN hospital h ON i.CNES = h.CNES WHERE h.NO_HOSPITAL IS NULL OR h.NO_HOSPITAL = '' GROUP BY 1 ORDER BY internacoes DESC LIMIT 20", "data_quality_finding"),
            q(PERSONAS[2], "A tabela final de internacoes tem o mesmo volume da staging?", "Comparar carga final contra staging.", "L5", l5, "SELECT (SELECT COUNT(*) FROM stg_internacoes) AS stg_internacoes, (SELECT COUNT(*) FROM internacoes) AS internacoes, (SELECT COUNT(*) FROM stg_internacoes) - (SELECT COUNT(*) FROM internacoes) AS diferenca", "data_quality_finding"),
            q(PERSONAS[3], "Quais anos tiveram volume extremamente baixo de internacoes e podem indicar cobertura parcial?", "Encontrar anos anomalo-baixos na serie.", "L5", l5, "WITH anual AS (SELECT year(DT_INTER) AS ano, COUNT(*) AS internacoes FROM internacoes GROUP BY 1), stats AS (SELECT quantile_cont(internacoes, 0.25) AS q1, quantile_cont(internacoes, 0.75) AS q3 FROM anual) SELECT a.ano, a.internacoes, s.q1, s.q3, s.q1 - 1.5 * (s.q3 - s.q1) AS limite_inferior_iqr FROM anual a, stats s WHERE a.internacoes < s.q1 - 1.5 * (s.q3 - s.q1) ORDER BY a.ano", "data_quality_finding"),
        ]
    )
    return specs


FORBIDDEN_SQL = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|COPY|EXPORT|IMPORT|ATTACH|DETACH|VACUUM|CALL)\b", re.I)


def validate_sql_is_read_only(sql: str) -> None:
    stripped = sql.strip().upper()
    if not (stripped.startswith("SELECT") or stripped.startswith("WITH")):
        raise ValueError(f"SQL must start with SELECT or WITH: {sql[:80]}")
    if FORBIDDEN_SQL.search(sql):
        raise ValueError(f"Forbidden SQL keyword found: {sql[:120]}")


def extract_tables_and_columns(sql: str, columns_by_table: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    lowered = sql.lower()
    tables = [table for table in MAIN_TABLES if re.search(rf"\b{re.escape(table.lower())}\b", lowered)]
    cols: list[str] = []
    for table in tables:
        for col in columns_by_table.get(table, []):
            if re.search(rf"\b{re.escape(col.lower())}\b", lowered):
                cols.append(f"{table}.{col}")
    return sorted(set(tables)), sorted(set(cols))


def validate_ground_truth(
    con: duckdb.DuckDBPyConnection, columns_by_table: dict[str, list[str]]
) -> list[dict[str, Any]]:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    accepted: list[dict[str, Any]] = []
    specs = question_specs()
    executed_at = datetime.now().isoformat(timespec="seconds")
    for index, spec in enumerate(specs, start=1):
        query_id = f"SIHRD5_Q{index:03d}"
        validate_sql_is_read_only(spec.sql)
        started = time.time()
        result = con.execute(spec.sql)
        columns = [d[0] for d in result.description]
        rows = rows_to_dicts(columns, result.fetchall())
        duration = round(time.time() - started, 3)
        preview = rows[:30]
        evidence_payload = {
            "id": query_id,
            "question_pt": spec.question_pt,
            "executed_at": executed_at,
            "database_file": str(DB_PATH.name),
            "sql": spec.sql,
            "duration_seconds": duration,
            "row_count": len(rows),
            "columns": columns,
            "preview_rows": preview,
            "result_hash": hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest(),
        }
        evidence_path = RESULTS_DIR / f"{query_id}.json"
        write_json(evidence_path, evidence_payload)
        tables_used, columns_used = extract_tables_and_columns(spec.sql, columns_by_table)
        accepted.append(
            {
                "id": query_id,
                "persona": spec.persona,
                "question_pt": spec.question_pt,
                "business_intent": spec.business_intent,
                "difficulty": spec.difficulty,
                "difficulty_rationale": spec.difficulty_rationale,
                "sql": spec.sql,
                "tables_used": tables_used,
                "columns_used": columns_used,
                "expected_result_type": spec.expected_result_type,
                "execution_status": "passed",
                "row_count": len(rows),
                "result_summary": summarize_result(columns, rows),
                "validation_evidence": str(evidence_path.relative_to(ROOT)),
                "assumptions": spec.assumptions,
                "data_quality_notes": spec.data_quality_notes,
                "duration_seconds": duration,
                "created_at": executed_at[:10],
            }
        )
        print(f"[ground_truth] {query_id} {spec.difficulty} rows={len(rows)} seconds={duration}")
    return accepted


def summarize_result(columns: list[str], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "A consulta executou corretamente e retornou 0 linhas."
    if len(rows) == 1 and len(columns) <= 4:
        parts = [f"{col}={rows[0].get(col)}" for col in columns]
        return "Resultado unico: " + ", ".join(parts) + "."
    return f"A consulta executou corretamente e retornou {len(rows)} linhas; a evidencia contem uma amostra das primeiras linhas."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_database_overview(
    tables: list[dict[str, Any]],
    top_values: dict[str, list[dict[str, Any]]],
    storage_rows: list[dict[str, Any]],
    generated_at: str,
) -> None:
    write_csv(DOCS_DIR / "generated" / "table_storage_estimates.csv", storage_rows)
    main_tables = [t for t in tables if t["table_schema"] == "main"]
    audit_tables = [t for t in tables if t["table_schema"] == "main_dbt_test__audit"]
    fact_rows = {t["table_name"]: t["row_count"] for t in main_tables if t["table_name"] in FACT_TABLES}
    largest_tables = sorted(storage_rows, key=lambda row: row["estimated_bytes"], reverse=True)[:10]
    content = f"""# Database Overview: sihrd5.duckdb

Generated at: {generated_at}

## Scope

**Observed:** `sihrd5.duckdb` is a DuckDB database with `{len(tables)}` tables: `{len(main_tables)}` analytical tables in schema `main` and `{len(audit_tables)}` dbt audit tables in schema `main_dbt_test__audit`.

**Observed:** the main fact table `internacoes` has `{fact_rows.get('internacoes'):,}` rows and the bridge/detail table `internacao_procedimento` has `{fact_rows.get('internacao_procedimento'):,}` rows. The database therefore appears to model SIH/SUS hospital admissions (AIH/internacoes), procedures, hospitals, municipalities, clinical diagnoses, and socioeconomic context.

**Observed:** `PRAGMA database_size` reports the database size as `{storage_rows[0]['database_size'] if storage_rows else 'unknown'}`. Main-schema table storage estimates are derived from `PRAGMA storage_info` persistent block ids, so they are approximate and intended for prioritizing exploration rather than billing or physical storage guarantees.

**Inferred:** one row in `internacoes` most likely represents one hospital admission/AIH-level event. `internacao_procedimento` links admissions to performed procedures and can contain multiple records per admission.

**Unknown:** official DATASUS field definitions were not fetched in this run. Field meanings below are inferred from table/column names, dimension descriptions, and executed SQL evidence.

## Table Inventory

{markdown_table(main_tables)}

## Largest Main Tables By Estimated Storage

{markdown_table(largest_tables)}

## dbt Audit Tables

**Observed:** schema `main_dbt_test__audit` contains `{len(audit_tables)}` tables, mostly named after accepted-value/range tests. These look like persisted dbt audit/failure tables and should be treated as quality evidence, not primary analytical facts.

## Temporal Coverage Snapshot

{markdown_table(top_values['internacoes_por_ano_inter'])}

## UF Residence Snapshot

{markdown_table(top_values['internacoes_por_uf_residencia'])}

## Top Procedures

{markdown_table(top_values['top_procedimentos'])}

## Top CID Chapters

{markdown_table(top_values['top_cid_capitulo'])}

## Executed Inventory SQL

```sql
SELECT * FROM information_schema.tables ORDER BY table_schema, table_name;
```

```sql
SELECT table_schema, table_name, column_name, data_type, is_nullable
FROM information_schema.columns
ORDER BY table_schema, table_name, ordinal_position;
```

```sql
SELECT COUNT(*) FROM <schema>.<table>;
```

```sql
PRAGMA database_size;
PRAGMA storage_info('<main_table_name>');
```
"""
    write_text(DOCS_DIR / "database_overview.md", content)


def write_schema_catalog(
    tables: list[dict[str, Any]],
    columns: list[dict[str, Any]],
    profiles: list[dict[str, Any]],
    top_frequencies: list[dict[str, Any]],
    generated_at: str,
) -> None:
    write_csv(DOCS_DIR / "generated" / "table_inventory.csv", tables)
    write_csv(DOCS_DIR / "generated" / "column_catalog.csv", columns)
    write_csv(DOCS_DIR / "generated" / "column_profiles.csv", profiles)
    write_csv(DOCS_DIR / "generated" / "top_frequent_values.csv", top_frequencies)

    content = [f"# Schema Catalog\n\nGenerated at: {generated_at}\n"]
    content.append("## Tables\n")
    content.append(markdown_table(tables))
    content.append("\n## Top Frequent Values For Selected Categorical Fields\n")
    content.append(
        "These values are **observed** from executed `GROUP BY` queries and focus on important categorical/code fields used by the Stage 1 questions.\n"
    )
    content.append(markdown_table(top_frequencies))
    content.append("\n## Main Schema Columns\n")
    for table in [t for t in tables if t["table_schema"] == "main"]:
        table_cols = [c for c in columns if c["table_schema"] == "main" and c["table_name"] == table["table_name"]]
        table_profiles = [
            {
                "column_name": p["column_name"],
                "data_type": p["data_type"],
                "null_rate": p["null_rate"],
                "approx_distinct": p["approx_distinct"],
                "min_value": p["min_value"],
                "max_value": p["max_value"],
            }
            for p in profiles
            if p["table_name"] == table["table_name"]
        ]
        content.append(f"\n### {table['table_name']}\n")
        content.append(f"\nRows: `{table['row_count']:,}`. Classification: `{table['classificacao']}`.\n")
        content.append(markdown_table(table_cols))
        content.append("\n\nColumn profile:\n")
        content.append(markdown_table(table_profiles))
    write_text(DOCS_DIR / "schema_catalog.md", "\n".join(content))


def write_business_dictionary(tables: list[dict[str, Any]], generated_at: str) -> None:
    table_notes = {
        "internacoes": "Fato principal. Uma linha parece representar uma internacao/AIH com datas, permanencia, hospital, diagnosticos, valores, demografia, municipio de residencia e marcadores assistenciais.",
        "internacao_procedimento": "Tabela de detalhe/ponte entre internacao (`N_AIH`) e procedimento realizado (`PROC_REA`). Permite analisar mix de procedimentos, mas pode multiplicar linhas ao juntar com `internacoes`.",
        "procedimentos": "Dicionario de procedimentos realizados. `PROC_REA` e o codigo e `NOME_PROC` e a descricao.",
        "cid": "Dicionario de diagnosticos CID com descricao, categoria, grupo e capitulo. Usado para interpretar `DIAG_PRINC`, `DIAG_SECUN`, `CID_MORTE`, `CID_NOTIF` e diagnosticos secundarios.",
        "hospital": "Cadastro de estabelecimentos por CNES, com nome, municipio de movimento/atendimento e codigos administrativos.",
        "municipios": "Dimensao territorial com codigos municipais de 6 e 7 digitos, UF, regiao de saude e coordenadas.",
        "socioeconomico": "Indicadores municipais anuais: populacao, PIB per capita, obitos infantis, nascidos vivos, leitos SUS e medicos.",
        "tempo": "Calendario diario com ano, mes, trimestre e dia da semana.",
        "sexo": "Dimensao de sexo. Observacao importante: ha descricoes duplicadas para `Feminino`.",
        "raca_cor": "Dimensao de raca/cor.",
        "car_int": "Carater da internacao: eletivo, urgencia e categorias de acidente/lesao.",
        "especialidade": "Especialidade/leito/linha assistencial associada a internacao.",
        "complexidade": "Nivel de complexidade: atencao basica, media complexidade e alta complexidade.",
        "marca_uti": "Marcador/tipo de UTI usado na internacao.",
        "etnia": "Dimensao de etnia.",
        "nacionalidade": "Dimensao de nacionalidade.",
        "instrucao": "Dimensao de instrucao/escolaridade.",
        "vincprev": "Dimensao de vinculo previdenciario.",
        "cbor": "Dicionario de ocupacao CBO-R.",
        "contraceptivos": "Dicionario de metodos contraceptivos.",
        "stg_internacoes": "Tabela staging da internacao; usada para conferir carga final.",
        "stg_hospital": "Tabela staging do cadastro hospitalar.",
        "stg_sexo": "Tabela staging de sexo.",
    }

    metric_notes = [
        ("N_AIH", "Identificador da AIH/internacao. Deve ser tratado como chave candidata somente apos validar unicidade."),
        ("CNES", "Codigo nacional do estabelecimento de saude; liga `internacoes` a `hospital`."),
        ("DT_INTER", "Data de entrada/internacao."),
        ("DT_SAIDA", "Data de saida/alta."),
        ("DIAS_PERM", "Dias de permanencia. A relacao com `DT_SAIDA - DT_INTER` precisa de caveat porque pode seguir regra inclusiva ou ter divergencias."),
        ("VAL_SH", "Valor de servicos hospitalares."),
        ("VAL_SP", "Valor de servicos profissionais."),
        ("VAL_UTI", "Valor associado a UTI."),
        ("VAL_TOT", "Valor total registrado. Nao assumir soma direta de VAL_SH + VAL_SP + VAL_UTI sem verificar."),
        ("MORTE", "Marcador booleano de morte/desfecho obito."),
        ("MUNIC_RES", "Municipio de residencia do usuario."),
        ("PROC_REA", "Procedimento realizado."),
        ("DIAG_PRINC", "Diagnostico principal CID."),
    ]

    content = [f"# Business Dictionary\n\nGenerated at: {generated_at}\n"]
    content.append("## Reading Rules\n")
    content.append("- **Observed:** supported by executed SQL and schema inspection.\n- **Inferred:** likely from names/descriptions, not externally verified in this run.\n- **Unknown:** do not rely on without more evidence.\n")
    content.append("## Table Meanings\n")
    for table in [t["table_name"] for t in tables if t["table_schema"] == "main"]:
        note = table_notes.get(table, "Tabela presente no schema main; significado detalhado ainda depende de exploracao adicional.")
        label = "Inferred"
        if table in {"sexo"}:
            note += " A duplicidade de descricao citada e observada por SQL no data quality report."
        content.append(f"### {table}\n\n**{label}:** {note}\n")
    content.append("## Key Business Fields\n")
    content.append(markdown_table([{"field": f, "business_meaning": m} for f, m in metric_notes]))
    content.append(
        """
## Important Business Caveats

- Joining `internacoes` to `internacao_procedimento` can multiply admissions because one admission can have more than one procedure.
- Analyses by hospital use CNES and may lose interpretability when `NO_HOSPITAL` is missing.
- Analyses by CID should prefer joins to `cid` and should document whether `DIAG_PRINC`, `DIAG_SECUN`, or another diagnosis field is being used.
- Analyses by geography must state whether they use residence municipality (`MUNIC_RES`) or hospital movement municipality (`hospital.MUNIC_MOV`).
- Analyses by value must state whether they use `VAL_TOT`, components, or derived averages.
"""
    )
    write_text(DOCS_DIR / "business_dictionary.md", "\n".join(content))


def write_relationship_map(
    relationships: list[dict[str, Any]], candidate_keys: list[dict[str, Any]], generated_at: str
) -> None:
    write_csv(DOCS_DIR / "generated" / "relationship_coverage.csv", relationships)
    write_csv(DOCS_DIR / "generated" / "candidate_keys.csv", candidate_keys)
    rows = [
        {
            "left": f"{r['left_table']}.{r['left_key']}",
            "right": f"{r['right_table']}.{r['right_key']}",
            "meaning": r["business_meaning"],
            "left_rows": r["left_rows"],
            "matched_rows": r["matched_rows"],
            "unmatched_rows": r["unmatched_rows"],
            "match_rate_non_null": r["match_rate_non_null"],
            "confidence": r["confidence"],
        }
        for r in relationships
    ]
    candidate_rows = [
        {
            "table": r["table_name"],
            "candidate_key": r["candidate_key"],
            "row_count": r["row_count"],
            "null_key_rows": r["null_key_rows"],
            "distinct_key_count": r["distinct_key_count"],
            "duplicate_key_rows": r["duplicate_key_rows"],
            "confidence": r["confidence"],
        }
        for r in candidate_keys
    ]
    content = f"""# Relationship Map

Generated at: {generated_at}

## Candidate Keys

Candidate-key confidence is **observed** from null checks and exact distinct-key counts. A key is `confirmed` only when it has zero null-key rows and zero duplicate-key rows.

{markdown_table(candidate_rows)}

Relationship confidence is based on non-null match coverage:

- `confirmed`: >= 99.5%
- `likely`: >= 95%
- `weak`: >= 80%
- `rejected`: < 80% or unavailable

{markdown_table(rows)}

## SQL Evidence

### Candidate Key Checks

"""
    for r in candidate_keys:
        content += f"#### {r['table_name']} ({r['candidate_key']})\n\n```sql\n{r['sql']}\n```\n\n"

    content += "### Relationship Coverage Checks\n\n"
    for r in relationships:
        content += f"#### {r['left_table']}.{r['left_key']} -> {r['right_table']}.{r['right_key']}\n\n```sql\n{r['sql']}\n```\n\n"
    write_text(DOCS_DIR / "relationship_map.md", content)


def write_data_quality_report(checks: list[dict[str, Any]], generated_at: str) -> None:
    write_json(DOCS_DIR / "generated" / "data_quality_checks.json", checks)
    summary = [
        {
            "id": c["id"],
            "title": c["title"],
            "severity": c["severity"],
            "affected_rows": c["affected_rows"],
            "blocks_ground_truth": c["blocks_ground_truth"],
        }
        for c in checks
    ]
    content = f"# Data Quality Report\n\nGenerated at: {generated_at}\n\n## Summary\n\n{markdown_table(summary)}\n\n"
    for check in checks:
        content += f"""## {check['id']}: {check['title']}

- Severity: `{check['severity']}`
- Affected rows: `{check['affected_rows']}`
- Blocks ground truth: `{check['blocks_ground_truth']}`

Why it matters: {check['why_it_matters']}

```sql
{check['sql']}
```
"""
        if check["sample_sql"]:
            content += f"\nSample SQL:\n\n```sql\n{check['sample_sql']}\n```\n\nSample rows:\n\n{markdown_table(check['sample_rows'])}\n\n"
    write_text(DOCS_DIR / "data_quality_report.md", content)


def write_query_methodology(generated_at: str) -> None:
    content = f"""# Query Design Methodology

Generated at: {generated_at}

## Goal

The ground truth evaluates whether a future chatbot can convert realistic Brazilian health-system questions into executable SQL over `sihrd5.duckdb`.

## Acceptance Gate

Each accepted question must:

- be written as a natural Portuguese question from a realistic SUS/DATASUS persona;
- contain read-only SQL starting with `SELECT` or `WITH`;
- execute successfully against `sihrd5.duckdb`;
- return compact evidence stored under `evaluation/ground_truth/query_results/`;
- include tables, columns, difficulty, business intent, assumptions, and data quality notes.

## Difficulty Criteria

- `L1`: one table, basic retrieval/count/min/max, no joins.
- `L2`: one table aggregation, filtering, grouping, ordering, or simple ranking.
- `L3`: joins between fact and dimensions with business interpretation.
- `L4`: CTEs, windows, denominators, rates, temporal comparisons, percentiles, or multiple aggregation stages.
- `L5`: expert audit/data-quality question with inconsistency detection, orphan checks, or caveated metric definitions.

The criteria follow the same spirit as component-complexity evaluation in Text-to-SQL benchmarks such as Spider/BIRD: tables, joins, aggregation, nesting, windows, ordering, and domain ambiguity increase difficulty.

## Evidence Format

For each accepted item, the validator writes one JSON evidence file with:

- query id;
- question text;
- executed SQL;
- execution timestamp;
- duration;
- row count;
- result columns;
- preview rows;
- SHA-256 hash of the full returned result.

## Rejection Rules

A question is rejected or left pending when the SQL fails, is too ambiguous, requires unavailable external data, exposes unnecessary row-level personal detail, mutates the database, or depends on unsupported business assumptions.
"""
    write_text(DOCS_DIR / "query_design_methodology.md", content)


def write_ground_truth_docs(items: list[dict[str, Any]]) -> None:
    with (GT_DIR / "stage1_questions.jsonl").open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    by_diff: dict[str, int] = {}
    for item in items:
        by_diff[item["difficulty"]] = by_diff.get(item["difficulty"], 0) + 1

    content = "# Stage 1 Ground Truth Questions\n\n"
    content += f"Accepted validated questions: `{len(items)}`\n\n"
    content += "## Difficulty Distribution\n\n"
    content += markdown_table([{"difficulty": k, "count": by_diff[k]} for k in sorted(by_diff)])
    content += "\n\n## Questions\n\n"
    for item in items:
        content += f"""### {item['id']} ({item['difficulty']})

- Persona: {item['persona']}
- Question: {item['question_pt']}
- Intent: {item['business_intent']}
- Evidence: `{item['validation_evidence']}`
- Rows returned: `{item['row_count']}`
- Duration seconds: `{item['duration_seconds']}`

```sql
{item['sql']}
```

"""
    write_text(GT_DIR / "stage1_questions.md", content)

    rejected = """# Rejected Or Pending Questions

No candidate questions were rejected by the current automated validation run.

Future rejected questions should be recorded here with:

- question text;
- reason for rejection;
- failed SQL or ambiguity;
- whether the question can be fixed by schema clarification, external dictionary lookup, or query optimization.
"""
    write_text(GT_DIR / "rejected_questions.md", rejected)


def write_stage2_readiness(items: list[dict[str, Any]], checks: list[dict[str, Any]], generated_at: str) -> None:
    critical = [c for c in checks if c["affected_rows"] and c["severity"] in {"critical", "high"}]
    content = f"""# Stage 2 Readiness Notes

Generated at: {generated_at}

## What Is Ready

- A validated Stage 1 Text-to-SQL benchmark exists with `{len(items)}` executable question/SQL pairs.
- The schema, relationship map, business dictionary, and data-quality report are generated from the real DuckDB file.
- Query evidence exists for every accepted ground-truth item.

## Chatbot Requirements Derived From Stage 1

- The chatbot must always distinguish residence geography (`MUNIC_RES`) from hospital geography (`hospital.MUNIC_MOV`).
- The chatbot must warn users that joining procedures can multiply admissions unless the query intentionally counts procedure occurrences.
- The chatbot must cite whether a metric is based on `VAL_TOT` or component fields.
- The chatbot must use CID/procedure/hospital/municipality dimensions for human-readable answers.
- The chatbot should refuse or ask a clarification when the user asks for undefined terms such as "custo", "produção", "mortalidade" or "local" without specifying denominator/date/geography.

## Known Data Quality Caveats

{markdown_table([{'id': c['id'], 'title': c['title'], 'severity': c['severity'], 'affected_rows': c['affected_rows']} for c in critical])}

## Baseline Evaluation Metrics For Stage 2

- SQL execution accuracy.
- Answer correctness against query evidence.
- Correct use of denominator and date field.
- Correct handling of joins that multiply rows.
- Caveat/citation quality.
- Latency.
- Refusal or clarification accuracy for ambiguous questions.
"""
    write_text(DOCS_DIR / "stage2_readiness.md", content)


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found: {DB_PATH}")
    DOCS_DIR.mkdir(exist_ok=True)
    GT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().isoformat(timespec="seconds")
    con = duckdb.connect(str(DB_PATH), read_only=True)
    con.execute("PRAGMA threads=4")

    print("[stage1] loading catalog")
    tables, columns = get_catalog(con)
    columns_by_table: dict[str, list[str]] = {}
    for col in columns:
        if col["table_schema"] == "main":
            columns_by_table.setdefault(col["table_name"], []).append(col["column_name"])

    print("[stage1] profiling columns")
    profiles = profile_columns(con, tables, columns)

    print("[stage1] calculating top-value snapshots")
    top_values = top_value_queries(con)

    print("[stage1] estimating table storage")
    storage_rows = storage_estimates(con, tables)

    print("[stage1] calculating categorical top values")
    top_frequencies = top_frequent_values(con)

    print("[stage1] mapping relationships")
    relationships = relationship_coverage(con)

    print("[stage1] checking candidate keys")
    candidate_keys = candidate_key_checks(con)

    print("[stage1] running data-quality checks")
    checks = data_quality_checks(con)

    print("[stage1] validating ground-truth questions")
    items = validate_ground_truth(con, columns_by_table)

    print("[stage1] writing documentation")
    write_database_overview(tables, top_values, storage_rows, generated_at)
    write_schema_catalog(tables, columns, profiles, top_frequencies, generated_at)
    write_business_dictionary(tables, generated_at)
    write_relationship_map(relationships, candidate_keys, generated_at)
    write_data_quality_report(checks, generated_at)
    write_query_methodology(generated_at)
    write_ground_truth_docs(items)
    write_stage2_readiness(items, checks, generated_at)

    distribution: dict[str, int] = {}
    for item in items:
        distribution[item["difficulty"]] = distribution.get(item["difficulty"], 0) + 1
    write_json(
        MANIFEST_PATH,
        {
            "generated_at": generated_at,
            "database_file": DB_PATH.name,
            "table_count": len(tables),
            "main_table_count": len([t for t in tables if t["table_schema"] == "main"]),
            "audit_table_count": len([t for t in tables if t["table_schema"] == "main_dbt_test__audit"]),
            "ground_truth_count": len(items),
            "difficulty_distribution": distribution,
            "docs": [
                "docs/database_overview.md",
                "docs/schema_catalog.md",
                "docs/business_dictionary.md",
                "docs/relationship_map.md",
                "docs/data_quality_report.md",
                "docs/query_design_methodology.md",
                "docs/stage2_readiness.md",
            ],
            "ground_truth": [
                "evaluation/ground_truth/stage1_questions.jsonl",
                "evaluation/ground_truth/stage1_questions.md",
                "evaluation/ground_truth/rejected_questions.md",
                "evaluation/ground_truth/query_results/",
            ],
            "generated_artifacts": [
                "docs/generated/table_inventory.csv",
                "docs/generated/table_storage_estimates.csv",
                "docs/generated/column_catalog.csv",
                "docs/generated/column_profiles.csv",
                "docs/generated/top_frequent_values.csv",
                "docs/generated/candidate_keys.csv",
                "docs/generated/relationship_coverage.csv",
                "docs/generated/data_quality_checks.json",
            ],
        },
    )
    print(f"[stage1] complete questions={len(items)} distribution={distribution}")


if __name__ == "__main__":
    main()
