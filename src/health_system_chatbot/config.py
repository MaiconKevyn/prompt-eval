from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


DEFAULT_LLM_MODEL = "gpt-4.1-mini"
DEFAULT_EMBED_MODEL = "text-embedding-3-small"


@dataclass(frozen=True)
class ChatbotConfig:
    project_root: Path
    db_path: Path
    openai_api_key: str | None
    llm_model: str = DEFAULT_LLM_MODEL
    embed_model: str = DEFAULT_EMBED_MODEL
    max_rows: int = 200
    query_timeout_seconds: int = 60
    index_dir: Path | None = None
    audit_log_path: Path | None = None

    @property
    def has_openai_key(self) -> bool:
        return bool(self.openai_api_key)

    def safe_summary(self) -> dict[str, object]:
        return {
            "project_root": str(self.project_root),
            "db_path": str(self.db_path),
            "db_exists": self.db_path.exists(),
            "openai_api_key_set": self.has_openai_key,
            "llm_model": self.llm_model,
            "embed_model": self.embed_model,
            "max_rows": self.max_rows,
            "query_timeout_seconds": self.query_timeout_seconds,
            "index_dir": str(self.index_dir or self.project_root / ".chatbot_index"),
            "audit_log_path": str(
                self.audit_log_path
                or self.project_root / "evaluation/chatbot/audit/chat_audit.jsonl"
            ),
        }


def find_project_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for path in [cur, *cur.parents]:
        if (path / "chat_goal.md").exists() or (path / "GOAL.md").exists():
            return path
    return cur


def _int_env(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc


def load_config(project_root: Path | None = None) -> ChatbotConfig:
    root = find_project_root(project_root)
    load_dotenv(root / ".env")

    db_path = Path(os.environ.get("CHATBOT_DB_PATH", "sihrd5.duckdb"))
    if not db_path.is_absolute():
        db_path = root / db_path

    index_dir = Path(os.environ.get("CHATBOT_INDEX_DIR", ".chatbot_index"))
    if not index_dir.is_absolute():
        index_dir = root / index_dir

    audit_log_path = Path(
        os.environ.get("CHATBOT_AUDIT_LOG_PATH", "evaluation/chatbot/audit/chat_audit.jsonl")
    )
    if not audit_log_path.is_absolute():
        audit_log_path = root / audit_log_path

    return ChatbotConfig(
        project_root=root,
        db_path=db_path,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        llm_model=os.environ.get("CHATBOT_LLM_MODEL", DEFAULT_LLM_MODEL),
        embed_model=os.environ.get("CHATBOT_EMBED_MODEL", DEFAULT_EMBED_MODEL),
        max_rows=_int_env("CHATBOT_MAX_ROWS", 200),
        query_timeout_seconds=_int_env("CHATBOT_QUERY_TIMEOUT_SECONDS", 60),
        index_dir=index_dir,
        audit_log_path=audit_log_path,
    )
