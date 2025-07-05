from functions.processors import (
    update_bonus_scheme,
    update_commission_structure,
    update_publication_channels,
    update_translation_required,
)


def test_update_bonus_scheme():
    state = {"job_level": "Senior"}
    update_bonus_scheme(state)
    assert state["bonus_scheme"] == "Eligible for an annual performance bonus."


def test_update_commission_structure():
    state = {"job_title": "Sales Manager"}
    update_commission_structure(state)
    assert "Commission" in state["commission_structure"]


def test_update_publication_channels():
    state = {"remote_work_policy": "Hybrid"}
    update_publication_channels(state)
    assert state["desired_publication_channels"].startswith("LinkedIn")


def test_update_translation_required():
    state = {
        "language_requirements": "English, German",
        "language_of_ad": "English",
    }
    update_translation_required(state)
    assert state["translation_required"] == "No"
