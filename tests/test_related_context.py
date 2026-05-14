from pathlib import Path

from health_system_chatbot.audit import append_audit_record, find_related_audit_context
from health_system_chatbot.config import ChatbotConfig


def test_find_related_audit_context_returns_recent_overlapping_questions(tmp_path: Path):
    config = ChatbotConfig(
        project_root=tmp_path,
        db_path=tmp_path / "test.duckdb",
        openai_api_key=None,
        audit_log_path=tmp_path / "audit.jsonl",
    )
    append_audit_record(
        config,
        {
            "question": "Quantas mortes ocorreram em Porto Alegre?",
            "answer_status": "answered",
            "answer": {
                "result_summary": "total_mortes=10",
                "caveats": ["Usa municipio de residencia."],
                "sql": "SELECT 10",
            },
        },
    )
    append_audit_record(
        config,
        {
            "question": "Qual foi o valor total em Sao Paulo?",
            "answer_status": "answered",
            "answer": {"result_summary": "valor_total=20"},
        },
    )

    related = find_related_audit_context(
        config,
        "Quais diagnosticos tiveram mortes em Porto Alegre?",
    )

    assert len(related) == 1
    assert related[0]["question"] == "Quantas mortes ocorreram em Porto Alegre?"
    assert related[0]["result_summary"] == "total_mortes=10"
    assert related[0]["caveats"] == ["Usa municipio de residencia."]
