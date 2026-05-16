import health_system_chatbot.answer_synthesizer as synth_module
from health_system_chatbot.answer_synthesizer import NaturalAnswer, synthesize_answer
from health_system_chatbot.config import ChatbotConfig
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
        show_debug=True,
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


def test_no_debug_hides_developer_context_and_technical_payload():
    intent = QuestionIntent(status="answerable", reason="ok", normalized_question="total")
    plan = SqlPlan(question="Total?", sql="SELECT 10 AS total")
    validation = ValidationResult(is_valid=True, severity="info", safe_sql=plan.sql)
    execution = ExecutionResult(
        sql=plan.sql,
        columns=["total"],
        rows=[{"total": 10}],
        row_count=1,
        result_hash="abc",
    )

    answer = synthesize_answer(
        question=plan.question,
        intent=intent,
        plan=plan,
        validation=validation,
        execution=execution,
        show_sql=True,
        show_debug=False,
        allow_llm=False,
    )

    assert answer.answer_pt
    assert answer.sql == plan.sql
    assert answer.result_summary == ""
    assert answer.caveats == []
    assert answer.developer_context == {}
    assert answer.evidence == {}


def test_llm_natural_answer_uses_configured_model(monkeypatch, tmp_path):
    class FakeLlm:
        def structured_predict(self, model, prompt, **kwargs):
            assert model is NaturalAnswer
            assert "Pergunta original" in getattr(prompt, "template", str(prompt))
            assert kwargs["question"] == "Total?"
            return NaturalAnswer(answer_pt="Resposta natural gerada pelo modelo.")

    captured = {}

    def fake_build_openai_llm(config):
        captured["model"] = config.llm_model
        return FakeLlm()

    monkeypatch.setattr(synth_module, "build_openai_llm", fake_build_openai_llm)
    config = ChatbotConfig(
        project_root=tmp_path,
        db_path=tmp_path / "test.duckdb",
        openai_api_key="test",
        llm_model="gpt-test",
    )
    intent = QuestionIntent(status="answerable", reason="ok", normalized_question="total")
    plan = SqlPlan(
        question="Total?",
        sql="SELECT 10 AS total",
        metric_basis=["COUNT"],
        date_basis="internacoes.DT_SAIDA",
    )
    validation = ValidationResult(is_valid=True, severity="info", safe_sql=plan.sql)
    execution = ExecutionResult(
        sql=plan.sql,
        columns=["total"],
        rows=[{"total": 10}],
        row_count=1,
        result_hash="abc",
    )

    answer = synthesize_answer(
        question=plan.question,
        intent=intent,
        plan=plan,
        validation=validation,
        execution=execution,
        config=config,
        allow_llm=True,
        show_debug=True,
    )

    assert captured["model"] == "gpt-test"
    assert answer.answer_pt == "Resposta natural gerada pelo modelo."
    assert "natural_answer_warning" not in answer.developer_context
