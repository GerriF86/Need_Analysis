"""State-update helpers – generate placeholders / suggestions."""
from typing import Any


def update_task_list(state: dict[str, Any]) -> None:
    """Populate `task_list` with generic tasks based on the role.

    Args:
        state: Streamlit `st.session_state` dictionary.
    """
    if state.get("task_list"):
        return

    role = state.get("job_title", "").lower()
    if "developer" in role:
        state["task_list"] = [
            "Build new features",
            "Refactor legacy modules",
            "Write unit tests",
        ]
    elif "sales" in role:
        state["task_list"] = [
            "Prospect and qualify leads",
            "Prepare demos",
            "Negotiate contracts",
        ]


def update_must_have_skills(state: dict[str, Any]) -> None:
    """Fill `must_have_skills` with placeholder skills.

    Args:
        state: Streamlit `st.session_state`.
    """
    if state.get("must_have_skills"):
        return
    role = state.get("job_title", "").lower()
    if "python" in role:
        state["must_have_skills"] = ["Python 3.11", "AsyncIO", "pytest"]
    elif "sales" in role:
        state["must_have_skills"] = ["CRM", "Negotiation", "Lead generation"]


def update_nice_to_have_skills(state: dict[str, Any]) -> None:
    """Suggest complementary skills.

    Args:
        state: Streamlit `st.session_state`.
    """
    if state.get("nice_to_have_skills"):
        return
    state["nice_to_have_skills"] = ["Public speaking", "Problem-solving", "Data analysis"]


def update_salary_range(state: dict[str, Any]) -> None:
    """Provide a simple salary range estimate (EUR)."""
    if state.get("salary_min") or state.get("salary_max"):
        return
    state["salary_min"], state["salary_max"] = 60000, 80000


def update_publication_channels(state: dict[str, Any]) -> None:
    """Recommend publication channels for remote roles."""
    if state.get("publication_channels"):
        return
    channels = ["LinkedIn", "Indeed", "StepStone"]
    if state.get("is_remote"):
        channels.append("We Work Remotely")
    state["publication_channels"] = channels


def update_bonus_scheme(state: dict[str, Any]) -> None:
    """Add a bonus scheme suggestion for mid/senior roles."""
    if state.get("bonus_scheme"):
        return
    senior = any(word in state.get("job_title", "").lower() for word in ("senior", "lead"))
    if senior:
        state["bonus_scheme"] = "Annual performance bonus up to 15 % of salary."


def update_commission_structure(state: dict[str, Any]) -> None:
    """Suggest commission structure for sales roles."""
    if state.get("commission_structure"):
        return
    if "sales" in state.get("job_title", "").lower():
        state["commission_structure"] = "Quarterly quota with 8 % commission on gross profit."


def update_translation_required(state: dict[str, Any]) -> None:
    """Mark whether translation is needed (DE ⇄ EN)."""
    if state.get("translation_required") is not None:
        return
    lang = state.get("language", "de")
    state["translation_required"] = lang not in ("de", "en")
