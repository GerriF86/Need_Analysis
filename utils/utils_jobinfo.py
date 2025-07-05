"""PDF / URL → plain text, plus simple regex-based field extraction."""
from __future__ import annotations

import io
import re
from typing import Dict, List

import fitz  # PyMuPDF
import streamlit as st

# --------------------------------------------------------------------------- #
#                           Text / PDF → Plain Text                           #
# --------------------------------------------------------------------------- #
def extract_text(file) -> str:  # noqa: WPS110  (file ok)
    """Return text from uploaded PDF/DOCX/TXT file."""
    filename = file.name.lower()
    if filename.endswith(".pdf"):
        with fitz.open(stream=file.getbuffer(), filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)
    return io.TextIOWrapper(file, encoding="utf-8", errors="ignore").read()


# --------------------------------------------------------------------------- #
#                      Very simple regex-based field extraction               #
# --------------------------------------------------------------------------- #
TITLE_RE = re.compile(r"(?i)^(?:job(?:titel)?|position)\s*:?\s*(.+)$", re.M)
COMPANY_RE = re.compile(r"(?i)^(?:unternehmen|company)\s*:?\s*(.+)$", re.M)
CITY_RE = re.compile(r"(?i)^(?:ort|standort|city|location)\s*:?\s*(.+)$", re.M)


def _rx(pattern: re.Pattern[str], text: str) -> str:
    m = pattern.search(text)
    return (m.group(1).strip() if m else "")[:120]  # truncate


def basic_field_extraction(text: str) -> Dict[str, str]:
    """Return dict with minimal fields extracted via regex.

    Any missing keys from `keys.ALL_STEP_KEYS` are included with empty
    strings so that Streamlit widgets can be pre-populated consistently.

    Note:
        Regex-based extraction may miss or misidentify fields if job ads use
        uncommon wording. Consider LLM-based parsing for higher recall.
    """
    fields = {
        "job_title": _rx(TITLE_RE, text),
        "company_name": _rx(COMPANY_RE, text),
        "city": _rx(CITY_RE, text),
    }
    return fields


# --------------------------------------------------------------------------- #
#                            Utility – Preview box                            #
# --------------------------------------------------------------------------- #
def display_fields_summary() -> None:
    """Render a Markdown list of the currently stored fields."""
    fields: Dict[str, str] = st.session_state.get("job_fields", {})
    for key, value in fields.items():
        if not value or key == "parsed_data_raw":
            continue
        safe = value.replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(f"- **{key.replace('_', ' ').title()}**<br>{safe}", unsafe_allow_html=True)
