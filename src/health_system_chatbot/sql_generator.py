from __future__ import annotations

from llama_index.core import PromptTemplate

from .config import ChatbotConfig
from .llm import build_openai_llm
from .models import RetrievedContext, SqlPlan, Stage1Context
from .prompts import SQL_GENERATION_PROMPT
from .text import normalize_text


def _infer_grain(question: str, sql: str) -> str:
    text = normalize_text(f"{question} {sql}")
    if "internacao_procedimento" in text or "procedimento" in text:
        return "procedure_occurrence"
    if "hospital" in text or "cnes" in text:
        return "hospital"
    if "municipio" in text and "ano" in text:
        return "municipality_year"
    if "internacao" in text or "aih" in text:
        return "hospitalization"
    return "other"


def _infer_geography(question: str, sql: str) -> str:
    text = normalize_text(f"{question} {sql}")
    tokens = set(text.split())
    has_residence = "munic_res" in text or "residencia" in text
    has_hospital = "munic_mov" in text or "estabelecimento" in tokens or "hospital" in tokens
    if has_residence and has_hospital:
        return "mixed"
    if has_residence:
        return "residence"
    if has_hospital:
        return "hospital"
    return "none"


def _infer_metric_basis(sql: str) -> list[str]:
    upper = sql.upper()
    metrics = []
    for name in ("VAL_TOT", "VAL_SH", "VAL_SP", "VAL_UTI", "DIAS_PERM", "MORTE"):
        if name in upper:
            metrics.append(name)
    if "COUNT(" in upper:
        metrics.append("COUNT")
    return metrics


def _infer_date_basis(sql: str) -> str:
    upper = sql.upper()
    if "DT_INTER" in upper:
        return "DT_INTER"
    if "DT_SAIDA" in upper:
        return "DT_SAIDA"
    if "NU_ANO" in upper:
        return "NU_ANO"
    return "unknown"


def _context_to_prompt(context: RetrievedContext) -> str:
    policies = "\n".join(
        f"- {p.left} -> {p.right}: {p.confidence}, {p.accepted_usage_policy}, unmatched={p.unmatched_rows}"
        for p in context.join_policies[:12]
    )
    caveats = "\n".join(f"- {c}" for c in context.data_quality_caveats[:8])
    tables = "\n\n".join(context.table_context[:8])
    columns = "\n".join(f"- {column}" for column in context.columns[:160])
    return (
        f"Retrieval mode: {context.retrieval_mode}\n\n"
        f"Tabelas:\n{tables}\n\n"
        f"Colunas recuperadas:\n{columns}\n\n"
        f"Join policies:\n{policies}\n\n"
        f"Caveats:\n{caveats}"
    )


def generate_sql_plan(
    question: str,
    context: RetrievedContext,
    stage1_context: Stage1Context,
    config: ChatbotConfig,
    *,
    allow_llm: bool = True,
) -> SqlPlan:
    if not allow_llm:
        raise RuntimeError(
            "LLM generation is disabled. Runtime SQL generation no longer uses ground truth shortcuts."
        )

    llm = build_openai_llm(config)
    prompt = PromptTemplate(SQL_GENERATION_PROMPT)
    plan = llm.structured_predict(
        SqlPlan,
        prompt,
        question=question,
        context=_context_to_prompt(context),
    )
    if not plan.metric_basis:
        plan.metric_basis = _infer_metric_basis(plan.sql)
    if plan.date_basis in {"", "none"}:
        plan.date_basis = _infer_date_basis(plan.sql)
    plan.source = "llamaindex_openai"
    return plan
