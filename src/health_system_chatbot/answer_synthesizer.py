from __future__ import annotations

import json
from typing import Any

from llama_index.core import PromptTemplate
from pydantic import BaseModel

from .config import ChatbotConfig
from .llm import build_openai_llm
from .models import (
    ChatbotAnswer,
    ExecutionResult,
    QuestionIntent,
    RetrievedContext,
    SqlPlan,
    ValidationResult,
)
from .prompts import NATURAL_ANSWER_PROMPT
from .text import normalize_text


class NaturalAnswer(BaseModel):
    answer_pt: str


def _format_value(value: object) -> str:
    if isinstance(value, float):
        return f"{value:,.4f}".rstrip("0").rstrip(".")
    return str(value)


def _summarize_result(result: ExecutionResult) -> str:
    if not result.rows:
        return "A consulta executou, mas nao retornou linhas."
    if len(result.rows) == 1:
        row = result.rows[0]
        return ", ".join(f"{key}={_format_value(value)}" for key, value in row.items())
    first = result.rows[0]
    preview = ", ".join(f"{key}={_format_value(value)}" for key, value in first.items())
    suffix = " O resultado foi truncado." if result.truncated else ""
    return f"A consulta retornou {result.row_count} linhas. Primeira linha: {preview}.{suffix}"


def _humanize_key(key: str) -> str:
    labels = {
        "DIAG_PRINC": "diagnostico",
        "DESCRICAO": "descricao",
        "total_mortes": "mortes",
        "mortes": "mortes",
        "internacoes": "internacoes",
        "valor_total": "valor total",
    }
    return labels.get(key, key.replace("_", " ").lower())


def _count_column(row: dict[str, Any]) -> str | None:
    for candidate in ("total_mortes", "mortes", "obitos", "internacoes", "total"):
        if candidate in row:
            return candidate
    for key, value in row.items():
        if isinstance(value, int | float) and key.upper() not in {"DIAG_PRINC", "CID"}:
            return key
    return None


def _row_to_user_phrase(row: dict[str, Any]) -> str:
    count_key = _count_column(row)
    count_value = row.get(count_key) if count_key else None
    description = row.get("DESCRICAO") or row.get("descricao") or row.get("NO_MUNICIPIO")
    code = row.get("DIAG_PRINC") or row.get("CID")

    if description and code and count_key:
        count_label = _humanize_key(count_key)
        return f"{description} ({code}): {_format_value(count_value)} {count_label}"
    if description and count_key:
        count_label = _humanize_key(count_key)
        return f"{description}: {_format_value(count_value)} {count_label}"

    return ", ".join(
        f"{_humanize_key(key)}={_format_value(value)}" for key, value in row.items()
    )


def _should_rank_by_count(question: str) -> bool:
    text = normalize_text(question)
    return any(token in text.split() for token in ("mais", "maior", "maiores", "top", "ranking"))


def _presentation_rows(question: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not _should_rank_by_count(question):
        return rows
    sortable = []
    for row in rows:
        count_key = _count_column(row)
        count_value = row.get(count_key) if count_key else None
        if not isinstance(count_value, int | float):
            return rows
        sortable.append((count_value, row))
    return [row for _, row in sorted(sortable, key=lambda item: item[0], reverse=True)]


def _geography_label(value: str) -> str:
    return {
        "residence": "municipio de residencia",
        "hospital": "municipio do hospital/atendimento",
        "mixed": "geografia mista",
        "none": "sem recorte geografico explicito",
    }.get(value, value)


def _build_user_answer(
    *,
    question: str,
    plan: SqlPlan,
    execution: ExecutionResult,
    caveats: list[str],
    related_context: list[dict[str, Any]],
) -> str:
    presentation_rows = _presentation_rows(question, execution.rows)

    if not presentation_rows:
        answer = (
            f"Para a pergunta '{question}', a consulta executou com sucesso, "
            "mas nao encontrou linhas para os filtros usados."
        )
    elif len(presentation_rows) == 1:
        answer = (
            f"Para a pergunta '{question}', o resultado calculado foi: "
            f"{_row_to_user_phrase(presentation_rows[0])}."
        )
    else:
        rows = [
            f"{idx}. {_row_to_user_phrase(row)}"
            for idx, row in enumerate(presentation_rows, start=1)
        ]
        answer = (
            f"Para a pergunta '{question}', os resultados retornados foram: "
            + "; ".join(rows)
            + "."
        )

    context_parts = []
    if plan.metric_basis:
        context_parts.append(f"metrica: {', '.join(plan.metric_basis)}")
    if plan.date_basis and plan.date_basis not in {"unknown", "none"}:
        context_parts.append(f"base temporal: {plan.date_basis}")
    if plan.geography_basis != "none":
        context_parts.append(f"geografia: {_geography_label(plan.geography_basis)}")
    if context_parts:
        answer += " A leitura considera " + "; ".join(context_parts) + "."

    if related_context:
        answer += (
            " Tambem considerei contexto anterior relacionado registrado no audit log "
            "para manter continuidade da analise."
        )

    if caveats:
        answer += " Observacoes: " + " ".join(caveats)

    return answer


def _build_developer_context(
    *,
    plan: SqlPlan,
    validation: ValidationResult,
    execution: ExecutionResult,
    context: RetrievedContext | None,
    related_context: list[dict[str, Any]],
    caveats: list[str],
) -> dict[str, Any]:
    return {
        "technical_summary": _summarize_result(execution),
        "metric_basis": plan.metric_basis,
        "date_basis": plan.date_basis,
        "geography_basis": plan.geography_basis,
        "join_assumptions": plan.join_assumptions,
        "retrieved_tables": context.tables if context else [],
        "retrieval_mode": context.retrieval_mode if context else "",
        "warnings": validation.warnings,
        "caveats": caveats,
        "related_context": related_context,
    }


def _compact_result_rows(rows: list[dict[str, Any]], *, limit: int = 8) -> list[dict[str, Any]]:
    return rows[:limit]


def _natural_answer_context(
    *,
    question: str,
    plan: SqlPlan,
    validation: ValidationResult,
    execution: ExecutionResult,
    result_summary: str,
    caveats: list[str],
    related_context: list[dict[str, Any]],
) -> dict[str, str]:
    return {
        "question": question,
        "sql": execution.sql,
        "result_summary": result_summary,
        "result_rows": json.dumps(
            _compact_result_rows(execution.rows),
            ensure_ascii=False,
            default=str,
        ),
        "plan": json.dumps(
            {
                "metric_basis": plan.metric_basis,
                "date_basis": plan.date_basis,
                "geography_basis": plan.geography_basis,
                "grain": plan.grain,
                "join_assumptions": plan.join_assumptions,
                "caveats": plan.caveats,
            },
            ensure_ascii=False,
            default=str,
        ),
        "validation": json.dumps(
            {
                "warnings": validation.warnings,
                "severity": validation.severity,
            },
            ensure_ascii=False,
            default=str,
        ),
        "caveats": json.dumps(caveats, ensure_ascii=False, default=str),
        "related_context": json.dumps(
            [
                {
                    "question": item.get("question"),
                    "answer_status": item.get("answer_status"),
                    "result_summary": item.get("result_summary"),
                    "caveats": item.get("caveats", []),
                }
                for item in related_context[:3]
            ],
            ensure_ascii=False,
            default=str,
        ),
    }


def _build_llm_user_answer(
    *,
    question: str,
    plan: SqlPlan,
    validation: ValidationResult,
    execution: ExecutionResult,
    result_summary: str,
    caveats: list[str],
    related_context: list[dict[str, Any]],
    config: ChatbotConfig | None,
    allow_llm: bool,
) -> tuple[str, str | None]:
    fallback = _build_user_answer(
        question=question,
        plan=plan,
        execution=execution,
        caveats=caveats,
        related_context=related_context,
    )
    if not allow_llm:
        return fallback, "Natural-language LLM synthesis disabled; used deterministic fallback."
    if config is None:
        return fallback, "Missing ChatbotConfig; used deterministic fallback."
    try:
        llm = build_openai_llm(config)
        answer = llm.structured_predict(
            NaturalAnswer,
            PromptTemplate(NATURAL_ANSWER_PROMPT),
            **_natural_answer_context(
                question=question,
                plan=plan,
                validation=validation,
                execution=execution,
                result_summary=result_summary,
                caveats=caveats,
                related_context=related_context,
            ),
        )
        answer_pt = answer.answer_pt.strip()
        if answer_pt:
            return answer_pt, None
        return fallback, "Natural-language LLM returned an empty answer; used deterministic fallback."
    except Exception as exc:
        return fallback, f"Natural-language LLM synthesis failed; used deterministic fallback: {exc}"


def _filter_debug_payload(answer: ChatbotAnswer, *, show_debug: bool) -> ChatbotAnswer:
    if show_debug:
        return answer
    return answer.model_copy(
        update={
            "result_summary": "",
            "caveats": [],
            "developer_context": {},
            "evidence": {},
        }
    )


def synthesize_answer(
    *,
    question: str,
    intent: QuestionIntent,
    plan: SqlPlan,
    validation: ValidationResult,
    execution: ExecutionResult,
    context: RetrievedContext | None = None,
    related_context: list[dict[str, Any]] | None = None,
    show_sql: bool = False,
    show_debug: bool = False,
    config: ChatbotConfig | None = None,
    allow_llm: bool = True,
) -> ChatbotAnswer:
    caveats = []
    caveats.extend(intent.required_caveats)
    caveats.extend(plan.caveats)
    caveats.extend(validation.warnings)
    caveats = [c for c in dict.fromkeys(caveats) if c]
    related_context = related_context or []

    result_summary = _summarize_result(execution)
    answer_pt, natural_answer_warning = _build_llm_user_answer(
        question=question,
        plan=plan,
        validation=validation,
        execution=execution,
        result_summary=result_summary,
        caveats=caveats,
        related_context=related_context,
        config=config,
        allow_llm=allow_llm,
    )
    developer_context = _build_developer_context(
        plan=plan,
        validation=validation,
        execution=execution,
        context=context,
        related_context=related_context,
        caveats=caveats,
    )
    if natural_answer_warning:
        developer_context["natural_answer_warning"] = natural_answer_warning

    answer = ChatbotAnswer(
        answer_pt=answer_pt,
        sql=execution.sql if show_sql else "",
        result_summary=result_summary,
        caveats=caveats,
        developer_context=developer_context,
        evidence={
            "result_hash": execution.result_hash,
            "elapsed_seconds": execution.elapsed_seconds,
            "row_count": execution.row_count,
            "truncated": execution.truncated,
            "plan_source": plan.source,
        },
        status="answered",
    )
    return _filter_debug_payload(answer, show_debug=show_debug)


def clarification_answer(intent: QuestionIntent, *, show_debug: bool = False) -> ChatbotAnswer:
    detail = " ".join(intent.ambiguities) if intent.ambiguities else intent.reason
    answer = ChatbotAnswer(
        answer_pt=f"Preciso de esclarecimento antes de consultar o banco. {detail}",
        status="clarified",
        caveats=intent.required_caveats,
        developer_context={"intent_reason": intent.reason},
        evidence={"intent_reason": intent.reason},
    )
    return _filter_debug_payload(answer, show_debug=show_debug)


def refused_answer(intent: QuestionIntent, *, show_debug: bool = False) -> ChatbotAnswer:
    answer = ChatbotAnswer(
        answer_pt=f"Nao vou executar SQL para essa pergunta. {intent.reason}",
        status="refused",
        caveats=intent.required_caveats,
        developer_context={"intent_reason": intent.reason},
        evidence={"intent_reason": intent.reason},
    )
    return _filter_debug_payload(answer, show_debug=show_debug)


def failed_answer(message: str, *, show_debug: bool = False) -> ChatbotAnswer:
    answer = ChatbotAnswer(
        answer_pt=f"Nao foi possivel responder com seguranca. {message}",
        status="failed",
        developer_context={"error": message},
        evidence={"error": message},
    )
    return _filter_debug_payload(answer, show_debug=show_debug)
