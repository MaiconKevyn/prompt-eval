from fastapi.testclient import TestClient

from health_system_chatbot.api import create_app
from health_system_chatbot.models import ChatbotAnswer


class FakeChatService:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def ask(self, question: str, *, show_sql: bool, allow_llm: bool) -> ChatbotAnswer:
        self.calls.append(
            {
                "question": question,
                "show_sql": show_sql,
                "allow_llm": allow_llm,
            }
        )
        return ChatbotAnswer(
            answer_pt="Resposta: total=10",
            sql="SELECT 10 AS total",
            result_summary="total=10",
            caveats=["Usa dados locais."],
            evidence={"row_count": 1},
            developer_context={"technical_summary": "total=10"},
            status="answered",
        )


def test_chat_endpoint_delegates_question_to_chat_service():
    service = FakeChatService()
    client = TestClient(create_app(chat_service=service))

    response = client.post(
        "/api/chat",
        json={
            "question": "Quantas internacoes existem?",
            "show_sql": True,
            "allow_llm": False,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer_pt": "Resposta: total=10",
        "sql": "SELECT 10 AS total",
        "result_summary": "total=10",
        "caveats": ["Usa dados locais."],
        "evidence": {"row_count": 1},
        "developer_context": {"technical_summary": "total=10"},
        "status": "answered",
    }
    assert service.calls == [
        {
            "question": "Quantas internacoes existem?",
            "show_sql": True,
            "allow_llm": False,
        }
    ]


def test_chat_endpoint_rejects_blank_question():
    service = FakeChatService()
    client = TestClient(create_app(chat_service=service))

    response = client.post("/api/chat", json={"question": "   "})

    assert response.status_code == 422
    assert service.calls == []


def test_frontend_is_served_from_root():
    client = TestClient(create_app(chat_service=FakeChatService()))

    response = client.get("/")

    assert response.status_code == 200
    assert 'id="chat-form"' in response.text
    assert 'fetch("/api/chat"' in response.text
    assert "developer_context" in response.text
    assert "Detalhe tecnico" in response.text


def test_frontend_sends_message_with_enter_and_keeps_shift_enter_for_newlines():
    client = TestClient(create_app(chat_service=FakeChatService()))

    response = client.get("/")

    assert response.status_code == 200
    assert 'questionInput.addEventListener("keydown"' in response.text
    assert 'event.key === "Enter"' in response.text
    assert "!event.shiftKey" in response.text
    assert "form.requestSubmit()" in response.text
