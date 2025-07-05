"""Update Streamlit session state from an edited **parsed_data_raw** block.

This helper is meant to be imported in *app.py* right after the call that renders
`display_fields_editable()` (or wherever you place the free‑text editor).  It
re‑runs the existing regex pipeline from *basic_field_extraction()* on the
current contents of the textarea with the Streamlit key `edit_parsed_data_raw`
and merges the resulting field dictionary back into *st.session_state['job_fields']*.

Because it re‑uses *basic_field_extraction* you only have to maintain a single
extraction logic.  If you later switch to spaCy, GPT, etc. you can do so inside
*basic_field_extraction* without touching this glue code.
"""

from __future__ import annotations

import streamlit as st

from utils.utils_jobinfo import basic_field_extraction, save_fields_to_session


def apply_edited_raw(prefix: str = "edit_") -> None:
    """Detect a change in the editable *parsed_data_raw* textarea and update fields.

    Parameters
    ----------
    prefix:
        The key prefix used by ``display_fields_editable``.  By default the
        function creates widgets whose keys start with ``"edit_"``.
    """
    raw_key = f"{prefix}parsed_data_raw"
    # Nothing to do if the widget hasn't been rendered yet
    if raw_key not in st.session_state:
        return

    # Retrieve the latest user input
    edited_raw: str = st.session_state.get(raw_key, "").strip()
    if not edited_raw:
        return  # user cleared the field – don't overwrite existing data

    # Run the same extraction logic that we already use for fresh uploads/URLs
    new_fields = basic_field_extraction(edited_raw)

    # Merge: keep existing non‑empty values that the user might have refined
    current = st.session_state.get("job_fields", {})
    for k, v in new_fields.items():
        if v and not current.get(k):
            current[k] = v

    save_fields_to_session(current)


# --- Usage example ---------------------------------------------------------
#
# display_fields_editable()  # renders the editable widgets
# apply_edited_raw()        # call right afterwards (or behind a "Übernehmen" button)
# --------------------------------------------------------------------------
