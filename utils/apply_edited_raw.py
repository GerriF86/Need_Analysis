"""Allow user to edit the raw extracted text and re-parse it."""
from typing import Dict

import streamlit as st

from utils.utils_jobinfo import basic_field_extraction


def apply_edited_raw(prefix: str = "edit_") -> None:
    """Merge new values from edited raw text into session state.

    Args:
        prefix: Key prefix used by `display_fields_editable` (defaults to "edit_").
    """
    raw_key = f"{prefix}parsed_data_raw"
    raw = st.session_state.get(raw_key)
    if not raw:
        return

    extracted: Dict[str, str] = basic_field_extraction(raw)
    job_fields: Dict[str, str] = st.session_state.get("job_fields", {})

    # merge (preserve non-empty existing values)
    for k, v in extracted.items():
        if v and not job_fields.get(k):
            job_fields[k] = v

    st.session_state["job_fields"] = job_fields
