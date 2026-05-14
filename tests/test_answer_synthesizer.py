from health_system_chatbot.answer_synthesizer import synthesize_answer
from health_system_chatbot.models import (
    ExecutionResult,
    QuestionIntent,
    RetrievedContext,
    SqlPlan,
    ValidationResult,
)


def test_answer_includes_metric_basis_and_caveats():
    intent = QuestionIntent(
        status="answerable",
        reason="ok",
        normalized_question="valor total",
        required_caveats=["Declarar coluna financeira."],
    )
    plan = SqlPlan(
        question="Qual e o valor total?",
        sql="SELECT SUM(VAL_TOT) AS valor_total FROM internacoes",
        metric_basis=["VAL_TOT"],
        caveats=["VAL_TOT foi usado."],
    )
    validation = ValidationResult(is_valid=True, severity="info", safe_sql=plan.sql)
    execution = ExecutionResult(
        sql=plan.sql,
        columns=["valor_total"],
        rows=[{"valor_total": 10.0}],
        row_count=1,
        result_hash="abc",
    )

    answer = synthesize_answer(
        question=plan.question,
        intent=intent,
        plan=plan,
        validation=validation,
        execution=execution,
    )

    assert answer.status == "answered"
    assert "VAL_TOT" in answer.answer_pt
    assert "Declarar coluna financeira." in answer.answer_pt


def test_answer_pt_is_user_friendly_while_dev_context_keeps_artifacts():
    intent = QuestionIntent(
        status="answerable",
        reason="ok",
        normalized_question="diagnosticos porto alegre",
    )
    plan = SqlPlan(
        question="Quais diagnosticos tiveram mais mortes?",
        sql="SELECT DIAG_PRINC, DESCRICAO, total_mortes FROM ranking",
        metric_basis=["count of hospitalizations with death"],
        date_basis="internacoes.DT_INTER",
        geography_basis="residence",
        caveats=["Considera municipio de residencia."],
    )
    validation = ValidationResult(is_valid=True, severity="info", safe_sql=plan.sql)
    execution = ExecutionResult(
        sql=plan.sql,
        columns=["DIAG_PRINC", "DESCRICAO", "total_mortes"],
        rows=[
            {"DIAG_PRINC": "A419", "DESCRICAO": "Septicemia NE", "total_mortes": 146},
            {
                "DIAG_PRINC": "P220",
                "DESCRICAO": "Sindr da angustia respirat do recem-nascido",
                "total_mortes": 205,
            },
        ],
        row_count=2,
        result_hash="abc",
    )
    context = RetrievedContext(
        tables=["internacoes", "municipios", "cid"],
        columns=["internacoes.DIAG_PRINC", "municipios.NO_MUNICIPIO", "cid.DESCRICAO"],
        retrieval_mode="schema_keyword",
    )

    answer = synthesize_answer(
        question=plan.question,
        intent=intent,
        plan=plan,
        validation=validation,
        execution=execution,
        context=context,
        related_context=[
            {
                "question": "Pergunta anterior sobre Porto Alegre",
                "answer_status": "answered",
                "result_summary": "Resumo anterior",
            }
        ],
        show_sql=True,
    )

    assert "Sindr da angustia respirat do recem-nascido (P220): 205 mortes" in answer.answer_pt
    assert "Septicemia NE (A419): 146 mortes" in answer.answer_pt
    assert answer.answer_pt.index("P220") < answer.answer_pt.index("A419")
    assert "Primeira linha" not in answer.answer_pt
    assert answer.result_summary.startswith("A consulta retornou 2 linhas")
    assert answer.sql == plan.sql
    assert answer.developer_context["retrieved_tables"] == ["internacoes", "municipios", "cid"]
    assert answer.developer_context["related_context"][0]["question"] == (
        "Pergunta anterior sobre Porto Alegre"
    )
