"""Simple helper for 'de / en' split labels."""


def tr(text: str, lang: str) -> str:
    """Return the language-specific part of a 'de / en' combined string.

    Args:
        text: String containing German and English parts separated by " / ".
        lang: Target language code ("de" or "en").
    """
    parts = text.split(" / ")
    return parts[0] if lang == "de" else (parts[1] if len(parts) > 1 else text)
