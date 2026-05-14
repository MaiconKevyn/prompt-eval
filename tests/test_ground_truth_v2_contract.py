from scripts.validate_ground_truth_v2_json import collect_static_sql_errors


def test_rejects_legacy_municipio_columns():
    sql = "SELECT m.nome FROM municipios m WHERE m.estado = 'RS'"

    errors = collect_static_sql_errors(sql)

    assert "m.nome" in errors
    assert "m.estado" in errors


def test_rejects_missing_atendimentos_table():
    sql = "SELECT COUNT(*) FROM atendimentos"

    assert "atendimentos" in collect_static_sql_errors(sql)


def test_accepts_current_municipio_columns():
    sql = "SELECT m.NO_MUNICIPIO FROM municipios m WHERE m.SG_UF = 'RS'"

    assert collect_static_sql_errors(sql) == []
