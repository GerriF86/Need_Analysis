from enum import Enum
from typing import Any

# --------------------------------------------------------------------------- #
#                               Field-Metadata                                #
# --------------------------------------------------------------------------- #
# Beispiel – ergänze / ändere nach Bedarf:
field_map: dict[str, dict[str, Any]] = {
    "job_title": {
        "label": "Jobtitel",
        "widget": "text_input",
        "step": "BASIC",
    },
    "company_name": {
        "label": "Unternehmen",
        "widget": "text_input",
        "step": "BASIC",
    },
    # ...
}


class WizardStep(Enum):
    """Wizard steps for vacancy data collection."""

    BASIC = "basic"
    DETAILS = "details"
    BENEFITS = "benefits"
    POSTING = "posting"


def get_fields_for_step(step: "WizardStep"):
    """Return list of field-meta dictionaries for a given step."""
    return [{"key": name, **meta} for name, meta in field_map.items() if meta["step"] == step.value]


def get_fields_by_group(step: "WizardStep", prio_max: int | None = None) -> dict[str, list[dict]]:
    """Return fields by (single) group – kept for backward compat."""
    fields = [
        {"key": name, **meta}
        for name, meta in field_map.items()
        if meta["step"] == step.value
        and (prio_max is None or meta.get("prio", prio_max) <= prio_max)
    ]
    return {"Fields": fields}
