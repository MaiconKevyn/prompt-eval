from health_system_chatbot.artifacts import load_stage1_context
from health_system_chatbot.schema_context import retrieve_context


def test_city_question_adds_municipality_dimension_for_hospital_geography():
    ctx = load_stage1_context()

    retrieved = retrieve_context(
        "Quais diagnosticos causaram mortes em Porto Alegre?",
        ctx,
        use_vector=False,
    )

    assert "municipios" in retrieved.tables
    assert "municipios.NO_MUNICIPIO" in retrieved.columns
    assert any(
        policy.left == "hospital.MUNIC_MOV"
        and policy.right == "municipios.CO_MUNICIPIO_6D"
        for policy in retrieved.join_policies
    )
