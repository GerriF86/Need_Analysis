from utils.openai_client import (
    call_extract_fields_function_calling,
    call_extract_fields_responses_api,
)


def extract_job_fields(text, language="de", mode="Function Calling (ChatCompletion)"):
    """
    text: Raw Jobad
    language: "de" or "en"
    mode: Option 1 (Function Calling), Option 2 (Responses API)
    """
    if not text:
        return {}
    if mode.startswith("Function Calling"):
        return call_extract_fields_function_calling(text, language)
    else:
        return call_extract_fields_responses_api(text, language)
