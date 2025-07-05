"""High-level wrapper for OpenAI-basierte Feld-Extraktion."""
from typing import Dict

from utils import openai_client


def extract_job_fields(  # noqa: WPS231 (OK – viele Parameter nötig)
    text: str,
    *,
    language: str = "de",
    mode: str = "Function Calling (ChatCompletion)",
) -> Dict[str, str]:
    """Extract structured job fields from raw ad text via OpenAI.

    Args:
        text: Raw job ad text (plain / HTML / PDF-to-text).
        language: Target language code ("de" or "en").
        mode: "Function Calling (ChatCompletion)" or fallback "Responses API".

    Returns:
        Dict – field → value (may be empty on error / low confidence).
    """
    if not text:
        return {}

    if mode.startswith("Function Calling"):
        return openai_client.call_extract_fields_function_calling(text, language=language)

    return openai_client.call_extract_fields_responses_api(text, language=language)
