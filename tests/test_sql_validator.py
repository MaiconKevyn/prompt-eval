from health_system_chatbot.artifacts import load_stage1_context
from health_system_chatbot.models import SqlPlan
from health_system_chatbot.sql_validator import validate_sql


def test_blocks_mutating_sql():
    ctx = load_stage1_context()

    result = validate_sql("DROP TABLE internacoes", ctx)

    assert not result.is_valid
    assert any("DROP" in error for error in result.errors)


def test_allows_simple_select():
    ctx = load_stage1_context()

    result = validate_sql("SELECT COUNT(*) AS total FROM internacoes", ctx)

    assert result.is_valid
    assert result.safe_sql == "SELECT COUNT(*) AS total FROM internacoes"


def test_blocks_rejected_relationship_for_business_query():
    ctx = load_stage1_context()
    sql = (
        "SELECT r.DESCRICAO, COUNT(*) "
        "FROM internacoes i JOIN raca_cor r ON i.RACA_COR = r.RACA_COR "
        "GROUP BY 1"
    )

    result = validate_sql(sql, ctx, question="Quantas internacoes por raca cor?")

    assert not result.is_valid
    assert any("Rejected relationship" in error for error in result.errors)


def test_likely_municipality_join_requires_mapped_scope_or_left_join():
    ctx = load_stage1_context()
    sql = (
        "SELECT m.SG_UF, COUNT(*) "
        "FROM internacoes i JOIN municipios m ON i.MUNIC_RES = m.CO_MUNICIPIO_6D "
        "GROUP BY 1"
    )

    invalid = validate_sql(sql, ctx, question="Internacoes por UF de residencia")
    assert not invalid.is_valid

    plan = SqlPlan(
        question="Internacoes por UF de residencia mapeada",
        sql=sql,
        caveats=["Resultado restrito a internacoes com municipio de residencia mapeado."],
    )
    valid = validate_sql(sql, ctx, question=plan.question, plan=plan)
    assert valid.is_valid


def test_rejects_text_literal_filter_on_numeric_municipality_code():
    ctx = load_stage1_context()
    sql = (
        "SELECT COUNT(*) "
        "FROM internacoes i JOIN hospital h ON i.CNES = h.CNES "
        "WHERE h.MUNIC_MOV = 'Porto Alegre'"
    )

    result = validate_sql(sql, ctx, question="Mortes em Porto Alegre")

    assert not result.is_valid
    assert any("hospital.MUNIC_MOV" in error for error in result.errors)
    assert any("text literal" in error for error in result.errors)
