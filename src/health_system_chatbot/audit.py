from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import ChatbotConfig
from .text import tokenize


def default_audit_log_path(config: ChatbotConfig) -> Path:
    return config.audit_log_path or config.project_root / "evaluation/chatbot/audit/chat_audit.jsonl"


def append_audit_record(config: ChatbotConfig, record: dict[str, Any]) -> Path:
    path = default_audit_log_path(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "logged_at": datetime.now(timezone.utc).isoformat(),
        **record,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True, default=str))
        f.write("\n")
    return path


def read_audit_records(path: Path, *, limit: int | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    if limit is not None:
        return records[-limit:]
    return records


def find_related_audit_context(
    config: ChatbotConfig,
    question: str,
    *,
    limit: int = 3,
) -> list[dict[str, Any]]:
    question_tokens = tokenize(question)
    if not question_tokens:
        return []

    related: list[dict[str, Any]] = []
    for record in reversed(read_audit_records(default_audit_log_path(config))):
        previous_question = str(record.get("question") or "")
        previous_tokens = tokenize(previous_question)
        overlap = question_tokens & previous_tokens
        if len(overlap) < 2:
            continue

        answer = record.get("answer") if isinstance(record.get("answer"), dict) else {}
        related.append(
            {
                "question": previous_question,
                "answer_status": record.get("answer_status"),
                "result_summary": answer.get("result_summary", ""),
                "caveats": answer.get("caveats", []),
                "sql": answer.get("sql", ""),
            }
        )
        if len(related) >= limit:
            break
    return related
