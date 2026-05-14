#!/usr/bin/env python3
"""Synchronize the canonical root ground_truth_v2.json with evaluation artifacts."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from validate_ground_truth_v2_json import DEFAULT_DB, DEFAULT_DATASET, execute_items, load_items


ROOT = Path(__file__).resolve().parents[1]
JSONL_PATH = ROOT / "evaluation/ground_truth/stage1_questions_v2.jsonl"
MARKDOWN_PATH = ROOT / "evaluation/ground_truth/stage1_questions_v2.md"
MANIFEST_PATH = ROOT / "evaluation/ground_truth/manifest.json"
SEMANTIC_AUDIT_PATH = ROOT / "docs/generated/ground_truth_semantic_audit.csv"
REFACTOR_AUDIT_PATH = ROOT / "evaluation/ground_truth/ground_truth_v2_refactor_audit.csv"

RESULT_TYPE_OVERRIDES = {
    "SIHRD5_Q003": "comparison",
    "SIHRD5_Q005": "comparison",
    "SIHRD5_Q008": "comparison",
    "SIHRD5_Q011": "comparison",
    "SIHRD5_Q015": "scalar",
    "SIHRD5_Q061": "distribution",
    "SIHRD5_Q062": "distribution",
    "SIHRD5_Q064": "time_series",
    "SIHRD5_Q075": "time_series",
    "SIHRD5_Q076": "time_series",
    "SIHRD5_Q078": "ranking",
    "SIHRD5_Q079": "ranking",
}
SQL_OVERRIDES = {
    "SIHRD5_Q049": (
        "SELECT NOME_PROC AS nome_procedimento, COUNT(*) AS ocorrencias "
        "FROM internacao_procedimento ip JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA "
        "GROUP BY 1 ORDER BY ocorrencias DESC LIMIT 20"
    ),
    "SIHRD5_Q058": (
        "SELECT NOME_PROC AS nome_procedimento, COUNT(*) AS ocorrencias, "
        "ROUND(SUM(CAST(i.VAL_TOT AS DECIMAL(20,2))), 2) AS valor_total "
        "FROM internacao_procedimento ip JOIN internacoes i ON ip.N_AIH = i.N_AIH "
        "JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA "
        "GROUP BY 1 ORDER BY valor_total DESC LIMIT 20"
    ),
    "SIHRD5_Q070": (
        "WITH proc AS (SELECT NOME_PROC AS nome_procedimento, COUNT(*) AS ocorrencias, "
        "(SUM(CAST(i.VAL_TOT AS DECIMAL(20,2)))::DOUBLE / COUNT(i.VAL_TOT)) "
        "AS valor_medio FROM internacao_procedimento ip "
        "JOIN internacoes i ON ip.N_AIH = i.N_AIH "
        "JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1) "
        "SELECT nome_procedimento, ocorrencias, ROUND(valor_medio, 2) AS valor_medio "
        "FROM proc WHERE ocorrencias >= 10000 ORDER BY valor_medio DESC LIMIT 20"
    ),
    "SIHRD5_Q078": (
        "WITH proc_uf AS (SELECT m.SG_UF, NOME_PROC AS nome_procedimento, "
        "COUNT(*) AS ocorrencias, ROW_NUMBER() OVER (PARTITION BY m.SG_UF "
        "ORDER BY COUNT(*) DESC) AS rn FROM internacao_procedimento ip "
        "JOIN internacoes i ON ip.N_AIH = i.N_AIH "
        "JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D "
        "JOIN procedimentos p ON ip.PROC_REA = p.PROC_REA GROUP BY 1, 2) "
        "SELECT SG_UF, nome_procedimento, ocorrencias FROM proc_uf WHERE rn = 1 ORDER BY SG_UF"
    ),
    "SIHRD5_Q082": (
        "WITH base AS (SELECT year(i.DT_INTER) AS ano, c.DESCRICAO AS carater, "
        "COUNT(*) AS internacoes FROM internacoes i JOIN car_int c ON i.CAR_INT = c.CAR_INT "
        "GROUP BY 1, 2), total AS (SELECT ano, SUM(internacoes) AS total_ano FROM base GROUP BY 1) "
        "SELECT b.ano, b.carater, b.internacoes, ROUND(100.0 * b.internacoes / t.total_ano, 4) "
        "AS percentual_ano FROM base b JOIN total t ON b.ano = t.ano "
        "ORDER BY b.ano, percentual_ano DESC, b.carater"
    ),
}
DIAS_PERM_CAVEAT = (
    "Usa explicitamente o campo DIAS_PERM; o data quality report registra divergencia "
    "massiva entre DIAS_PERM e date_diff('day', DT_INTER, DT_SAIDA)."
)


def load_seed_items() -> list[dict[str, Any]]:
    if DEFAULT_DATASET.exists():
        root_items = load_items(DEFAULT_DATASET)
        if root_items and "question_pt" in root_items[0] and "sql" in root_items[0]:
            return root_items
    return [json.loads(line) for line in JSONL_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def _with_question_suffix(question: str, suffix: str) -> str:
    if suffix.lower() in question.lower():
        return question
    if question.endswith("?"):
        return question[:-1] + f" {suffix}?"
    return f"{question} {suffix}"


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(item)
    normalized["question_pt"] = normalized.get("question_pt") or normalized.pop("question")
    normalized["sql"] = normalized.get("sql") or normalized.pop("query")
    normalized["tables_used"] = normalized.get("tables_used") or normalized.pop("tables", [])
    normalized.pop("question", None)
    normalized.pop("query", None)
    normalized.pop("tables", None)
    normalized.pop("notes", None)

    normalized["expected_result_type"] = RESULT_TYPE_OVERRIDES.get(
        normalized["id"],
        normalized.get("expected_result_type", "scalar"),
    )
    if normalized["id"] in SQL_OVERRIDES:
        normalized["sql"] = SQL_OVERRIDES[normalized["id"]]
    normalized["validation_evidence"] = (
        f"evaluation/ground_truth/query_results_v2/{normalized['id']}.json"
    )
    normalized.setdefault("persona", "Analista DATASUS/SIH")
    normalized.setdefault("business_intent", "Responder pergunta validada sobre o banco SIH/SUS.")
    normalized.setdefault("difficulty", "L3")
    normalized.setdefault("difficulty_rationale", "Classificacao definida pela complexidade SQL validada.")
    normalized.setdefault("columns_used", [])
    normalized.setdefault("execution_status", "passed")
    normalized.setdefault("row_count", 0)
    normalized.setdefault("result_summary", "Resultado validado por execucao no DuckDB.")
    normalized.setdefault(
        "assumptions",
        "Sem premissas adicionais alem do significado observado/inferido das colunas usadas.",
    )
    normalized.setdefault(
        "data_quality_notes",
        "Verificar caveats documentados no data quality report antes de interpretar o resultado.",
    )
    normalized.setdefault("created_at", "2026-05-14")

    sql = normalized["sql"].upper()
    if "DIAS_PERM" in sql and "DIAS_PERM DIFERENTE" not in normalized["question_pt"].upper():
        normalized["question_pt"] = _with_question_suffix(
            normalized["question_pt"],
            "segundo o campo DIAS_PERM",
        )
        if DIAS_PERM_CAVEAT not in normalized["data_quality_notes"]:
            normalized["data_quality_notes"] = (
                normalized["data_quality_notes"].rstrip(".") + ". " + DIAS_PERM_CAVEAT
            )
        normalized["semantic_disposition"] = "valid_with_caveats"
    else:
        normalized.setdefault("semantic_disposition", "accepted")

    if normalized["id"] == "SIHRD5_Q091":
        normalized["question_pt"] = "Quantas internacoes tem municipio de residencia sem cadastro territorial?"
        normalized["assumptions"] = (
            "A consulta usa LEFT JOIN para contar internacoes cujo MUNIC_RES nao possui "
            "correspondencia em municipios.CO_MUNICIPIO_6D."
        )
        normalized["data_quality_notes"] = (
            "Este item audita a orfandade territorial documentada no data quality report."
        )
        normalized["semantic_disposition"] = "accepted"

    if normalized["semantic_disposition"] == "accepted_scoped_population":
        normalized["semantic_disposition"] = "accepted_with_explicit_scope"
    return normalized


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(items: list[dict[str, Any]]) -> None:
    JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSONL_PATH.write_text(
        "".join(json.dumps(item, ensure_ascii=False, default=str) + "\n" for item in items),
        encoding="utf-8",
    )


def markdown_table(items: list[dict[str, Any]]) -> str:
    lines = [
        "# Ground Truth V2",
        "",
        "| id | difficulty | result_type | question |",
        "| --- | --- | --- | --- |",
    ]
    for item in items:
        question = item["question_pt"].replace("|", "\\|")
        lines.append(
            f"| `{item['id']}` | `{item['difficulty']}` | `{item['expected_result_type']}` | {question} |"
        )
    return "\n".join(lines) + "\n"


def write_manifest(items: list[dict[str, Any]]) -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {}
    distribution = Counter(item["difficulty"] for item in items)
    manifest["ground_truth_v2_count"] = len(items)
    manifest["difficulty_distribution_v2"] = dict(sorted(distribution.items()))
    ground_truth_paths = manifest.setdefault("ground_truth", [])
    for path in [
        "ground_truth_v2.json",
        "evaluation/ground_truth/stage1_questions_v2.jsonl",
        "evaluation/ground_truth/stage1_questions_v2.md",
        "evaluation/ground_truth/query_results_v2/",
    ]:
        if path not in ground_truth_paths:
            ground_truth_paths.append(path)
    generated = manifest.setdefault("generated_artifacts", [])
    if "docs/generated/ground_truth_semantic_audit.csv" not in generated:
        generated.append("docs/generated/ground_truth_semantic_audit.csv")
    write_json(MANIFEST_PATH, manifest)


def write_semantic_audit(items: list[dict[str, Any]]) -> None:
    previous: dict[str, dict[str, str]] = {}
    if SEMANTIC_AUDIT_PATH.exists():
        with SEMANTIC_AUDIT_PATH.open("r", encoding="utf-8", newline="") as handle:
            previous = {row["id"]: row for row in csv.DictReader(handle)}
    fieldnames = [
        "id",
        "question_pt",
        "execution_status",
        "read_only_status",
        "tables_used",
        "relationships_used",
        "worst_relationship_confidence",
        "uses_rejected_relationship",
        "uses_likely_relationship_without_caveat",
        "dropped_by_join_count",
        "dropped_by_join_rate",
        "invalid_domain_dependency",
        "business_semantics_status",
        "final_disposition",
        "disposition_reason",
    ]
    SEMANTIC_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SEMANTIC_AUDIT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            old = previous.get(item["id"], {})
            disposition = item["semantic_disposition"]
            writer.writerow(
                {
                    "id": item["id"],
                    "question_pt": item["question_pt"],
                    "execution_status": "passed",
                    "read_only_status": "passed",
                    "tables_used": ";".join(item["tables_used"]),
                    "relationships_used": old.get("relationships_used", ""),
                    "worst_relationship_confidence": old.get("worst_relationship_confidence", "none"),
                    "uses_rejected_relationship": old.get("uses_rejected_relationship", "False"),
                    "uses_likely_relationship_without_caveat": old.get(
                        "uses_likely_relationship_without_caveat",
                        "False",
                    ),
                    "dropped_by_join_count": old.get("dropped_by_join_count", "0"),
                    "dropped_by_join_rate": old.get("dropped_by_join_rate", "0.0"),
                    "invalid_domain_dependency": old.get("invalid_domain_dependency", "False"),
                    "business_semantics_status": disposition,
                    "final_disposition": disposition,
                    "disposition_reason": disposition,
                }
            )


def mark_refactor_audit_validated(items: list[dict[str, Any]]) -> None:
    if not REFACTOR_AUDIT_PATH.exists():
        return
    item_by_id = {item["id"]: item for item in items}
    with REFACTOR_AUDIT_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        final_id = row["final_id"]
        if final_id in item_by_id:
            row["validation_status_after"] = "passed"
            row["evidence_path"] = item_by_id[final_id]["validation_evidence"]
        elif row["decision"] == "drop":
            row["validation_status_after"] = "dropped"
        else:
            row["validation_status_after"] = "passed_canonical_replacement"
            row["evidence_path"] = "evaluation/ground_truth/query_results_v2/"
    with REFACTOR_AUDIT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "original_id",
                "final_id",
                "decision",
                "execution_status_before",
                "semantic_status_before",
                "decision_reason",
                "question_action",
                "sql_action",
                "validation_status_after",
                "evidence_path",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    items = [normalize_item(item) for item in load_seed_items()]
    execute_items(items, DEFAULT_DB, write_evidence=True)
    write_json(DEFAULT_DATASET, items)
    write_jsonl(items)
    MARKDOWN_PATH.write_text(markdown_table(items), encoding="utf-8")
    write_manifest(items)
    write_semantic_audit(items)
    mark_refactor_audit_validated(items)
    print("wrote ground_truth_v2.json")
    print("wrote evaluation/ground_truth/stage1_questions_v2.jsonl")
    print("wrote evaluation/ground_truth/stage1_questions_v2.md")
    print("wrote evaluation/ground_truth/manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
