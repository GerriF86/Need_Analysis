from __future__ import annotations

from typing import Any, Dict


def generate_boolean_search(fields: Dict[str, Any]) -> str:
    """Return a basic Boolean search string for job ads."""

    skills = fields.get("must_have_skills", [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]

    city = fields.get("city", "")
    job_title = fields.get("job_title", "")

    if not skills or not job_title:
        return "# Nicht genug Daten für Boolean-String"

    skill_part = " OR ".join([f'"{skill}"' for skill in skills])
    city_part = f" AND {city}" if city else ""
    query = f'({skill_part}) AND "{job_title}"{city_part}'
    return query
