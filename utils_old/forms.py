from __future__ import annotations
import streamlit as st
from utils.schema import FIELD_META

def render_widget(key: str) -> None:
    """Render a Streamlit widget whose spec is defined in FIELD_META."""
    meta = FIELD_META[key]
    label = meta["label"]
    widget = meta["widget"]
    options = meta.get("options", None)
    default = st.session_state.get(key, "")
    match widget:
        case "text_input":
            st.text_input(label, value=default, key=key)
        case "text_area":
            st.text_area(label, value=default, key=key, height=160)
        case "number_input":
            st.number_input(label, value=float(default) if default else 0.0, key=key)
        case "selectbox":
            st.selectbox(
                label,
                options,
                index=options.index(default) if default in options else 0,
                key=key,
            )
        case "multiselect":
            st.multiselect(label, options, default=default if default else [], key=key)
        case "checkbox":
            st.checkbox(label, value=bool(default), key=key)
        case "date_input":
            st.date_input(label, value=default if default else None, key=key)
        case "file_uploader":
            st.file_uploader(label, type=["pdf", "docx", "txt"], key=key)
        case _:
            st.write(f"⚠️ Unknown widget type for {key}: {widget}")
