"""Simple i18n helpers."""

from __future__ import annotations


def tr(text: str, lang: str) -> str:
    """Return language specific part of a 'de / en' string."""
    if " / " in text:
        left, right = text.split(" / ", 1)
        return left.strip() if lang == "de" else right.strip()
    return text
