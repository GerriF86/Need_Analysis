import datetime
from contextlib import nullcontext
from unittest.mock import patch

import streamlit as st

from wizard_steps import wizard_step_4_role


def test_wizard_step_4_role_defaults_today():
    st.session_state.clear()
    st.session_state["lang"] = "de"
    st.session_state["job_fields"] = {}

    today = datetime.date.today()
    with (
        patch("wizard_steps.st.header"),
        patch("wizard_steps.display_fields_summary"),
        patch("wizard_steps.st.selectbox", return_value=""),
        patch("wizard_steps.st.text_area", return_value=""),
        patch("wizard_steps.st.text_input", return_value=""),
        patch("wizard_steps.st.columns", return_value=(nullcontext(), nullcontext())),
        patch("wizard_steps.st.expander", return_value=nullcontext()),
        patch("wizard_steps.st.date_input", return_value=today) as mock_date,
    ):
        wizard_step_4_role()
        assert mock_date.call_args.args[1] == today
