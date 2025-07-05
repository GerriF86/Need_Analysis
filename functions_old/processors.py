"""State update helpers used across wizard steps."""

from __future__ import annotations

from typing import Any


def update_task_list(state: dict[str, Any]) -> None:
    """Populate ``task_list`` with generic tasks based on the role.

    Parameters
    ----------
    state:
        Session dictionary storing wizard fields.
    """
    if state.get("task_list"):
        return
    role = state.get("job_title") or state.get("role_description")
    if not role:
        return
    tasks = [f"{role} task {i}" for i in range(1, 6)]
    state["task_list"] = "\n".join(tasks)


def update_must_have_skills(state: dict[str, Any]) -> None:
    """Fill ``must_have_skills`` with placeholder skills."""
    if state.get("must_have_skills"):
        return
    role = state.get("job_title") or "role"
    skills = [f"{role} skill {i}" for i in range(1, 6)]
    state["must_have_skills"] = ", ".join(skills)


def update_nice_to_have_skills(state: dict[str, Any]) -> None:
    """Suggest three complementary skills."""
    if state.get("nice_to_have_skills"):
        return
    if not state.get("must_have_skills"):
        return
    extras = ["extra skill 1", "extra skill 2", "extra skill 3"]
    state["nice_to_have_skills"] = ", ".join(extras)


def update_salary_range(state: dict[str, Any]) -> None:
    """Provide a simple salary range estimate if missing."""
    current = str(state.get("salary_range", "")).strip().lower()
    if current and current != "competitive":
        return
    state["salary_range"] = "45000 – 55000 EUR"


def update_publication_channels(state: dict[str, Any]) -> None:
    """Recommend publication channels for remote roles."""
    policy = str(state.get("remote_work_policy", "")).lower()
    if policy in {"hybrid", "full remote"}:
        state["desired_publication_channels"] = "LinkedIn Remote Jobs; WeWorkRemotely"


def update_bonus_scheme(state: dict[str, Any]) -> None:
    """Add a bonus scheme suggestion for senior roles."""
    if state.get("bonus_scheme"):
        return
    level = str(state.get("job_level", "")).lower()
    if level in {"mid", "senior", "lead", "management"}:
        state["bonus_scheme"] = "Eligible for an annual performance bonus."


def update_commission_structure(state: dict[str, Any]) -> None:
    """Suggest commission structure for sales-related titles."""
    if state.get("commission_structure"):
        return
    title = str(state.get("job_title", "")).lower()
    sales_terms = [
        "sales",
        "business development",
        "account executive",
        "account manager",
    ]
    if any(term in title for term in sales_terms):
        state["commission_structure"] = "Commission based on sales performance."


def update_translation_required(state: dict[str, Any]) -> None:
    """Mark whether translation is needed based on language fields."""
    if not state.get("language_requirements"):
        return
    required = {
        lang.strip().lower()
        for lang in state["language_requirements"].split(",")
        if lang.strip()
    }
    ad_lang = str(state.get("language_of_ad", "English")).lower()
    if ad_lang and ad_lang not in required:
        state["translation_required"] = "Yes"
    else:
        state["translation_required"] = "No"
