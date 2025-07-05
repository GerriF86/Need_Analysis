"""Side-effect helpers that pre- or post-process session_state values."""
from __future__ import annotations
import streamlit as st
import datetime

# your existing helpers
from functions.processors import (
    update_bonus_scheme,
    update_commission_structure,
    update_must_have_skills,
    update_nice_to_have_skills,
    update_publication_channels,
    update_salary_range,
    update_task_list,
    update_translation_required,
)

from utils.esco_client import (
    get_skills_for_job_title,
    get_tasks_for_job_title,
)
from utils.i18n import tr
from utils.schema import WizardStep


def _ensure_default_dates() -> None:
    """Guard against None/str ↔️ date mismatches."""
    key = "date_of_employment_start"
    val = st.session_state.get(key)
    if isinstance(val, str):
        try:
            st.session_state[key] = datetime.date.fromisoformat(val)
        except ValueError:
            st.session_state[key] = datetime.date.today()
    elif val is None:
        st.session_state[key] = datetime.date.today()


# --------------------------------------------------------------------------- #
# Map each step to a list of side-effect functions that mutate session_state.
# Each function must accept **no arguments** and read / write st.session_state
# on its own (wrap your existing ones with small lambdas if needed).
# --------------------------------------------------------------------------- #
PRE_HOOKS: dict[WizardStep, list[callable]] = {
    WizardStep.TASKS: [
        lambda: update_task_list(st.session_state),
        lambda: _prefill_esco_tasks(),
    ],
    WizardStep.SKILLS: [
        lambda: update_must_have_skills(st.session_state),
        lambda: update_nice_to_have_skills(st.session_state),
        lambda: _prefill_esco_skills(),
    ],
    WizardStep.COMP_BENEFITS: [
        lambda: update_salary_range(st.session_state),
        lambda: update_bonus_scheme(st.session_state),
        lambda: update_commission_structure(st.session_state),
    ],
    WizardStep.RECRUITMENT: [
        lambda: update_publication_channels(st.session_state),
        lambda: update_translation_required(st.session_state),
    ],
    WizardStep.BASIC: [_ensure_default_dates],
}


# ---------- helper wrappers for ESCO auto-prefill -------------------------- #
def _prefill_esco_tasks() -> None:
    title = st.session_state.get("job_title")
    if title and not st.session_state.get("task_list"):
        tasks = get_tasks_for_job_title(title, language=st.session_state.get("lang", "de"), limit=5)
        if tasks:
            st.session_state["task_list"] = "\n".join(tasks)
            st.info(tr("Aufgaben von ESCO importiert", st.session_state.get("lang", "de")))


def _prefill_esco_skills() -> None:
    title = st.session_state.get("job_title")
    if title and not st.session_state.get("must_have_skills"):
        skills = get_skills_for_job_title(title, language=st.session_state.get("lang", "de"), limit=5)
        if skills:
            st.session_state["must_have_skills"] = ", ".join(skills)
            st.info(tr("Skills von ESCO importiert", st.session_state.get("lang", "de")))
