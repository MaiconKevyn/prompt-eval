from __future__ import annotations

import re
import unicodedata


def normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9_]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(value: str) -> set[str]:
    return {token for token in normalize_text(value).split() if len(token) > 2}

