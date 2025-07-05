from functions.field_extraction import extract_job_fields
from utils import openai_client


def test_extract_job_fields_dispatch(monkeypatch):
    called = {}

    monkeypatch.setattr(
        openai_client,
        "call_extract_fields_function_calling",
        lambda text, language="de": called.setdefault("fc", (text, language)) or {"ok": True},
    )
    monkeypatch.setattr(
        openai_client,
        "call_extract_fields_responses_api",
        lambda text, language="de": called.setdefault("res", (text, language)) or {"ok": True},
    )

    extract_job_fields("Hello", language="en", mode="Function Calling (ChatCompletion)")
    assert called["fc"] == ("Hello", "en")

    extract_job_fields("Hallo", language="de", mode="Some Other Mode")
    assert called["res"] == ("Hallo", "de")

    assert extract_job_fields("") == {}
