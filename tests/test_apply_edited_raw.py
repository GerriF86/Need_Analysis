import streamlit as st

from utils.apply_edited_raw import apply_edited_raw


def test_apply_edited_raw_merges_fields():
    st.session_state.clear()
    st.session_state["job_fields"] = {"job_title": "Original", "company_name": ""}
    st.session_state["edit_parsed_data_raw"] = "Jobtitel: NewTitle\nUnternehmen: NewCompany"

    apply_edited_raw()

    fields = st.session_state["job_fields"]
    assert fields["job_title"] == "Original"          # existing value preserved
    assert fields["company_name"] == "NewCompany"     # empty → updated


def test_apply_edited_raw_no_override():
    st.session_state.clear()
    st.session_state["job_fields"] = {"job_title": "", "city": "OldCity"}
    st.session_state["edit_parsed_data_raw"] = "Jobtitel: NewTitle\nOrt: NewCity"

    apply_edited_raw()

    fields = st.session_state["job_fields"]
    assert fields["city"] == "OldCity"                # existing value preserved
    assert fields["job_title"] == "NewTitle"          # empty → updated
