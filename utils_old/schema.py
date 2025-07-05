"""Vacalyser – canonical wizard schema.

This file defines:
1. WizardStep enum (order matters)
2. STEP_KEYS: mapping WizardStep -> list[str] (UI order)
3. ALL_KEYS: flattened list for convenience
4. FIELD_META: UI metadata for every key (widget, label, options, etc.)

All other modules (forms.py, hooks.py, downstream tools) must import from this
single source of truth to stay in sync.
"""
from __future__ import annotations

import datetime
from enum import Enum
from typing import Any, Dict, List

# --------------------------------------------------------------------------- #
# 1) Wizard steps (render order)
# --------------------------------------------------------------------------- #
class WizardStep(str, Enum):
    BASIC = "BASIC"
    COMPANY = "COMPANY"
    DEPARTMENT = "DEPARTMENT"
    ROLE = "ROLE"  # advanced role meta (dates, KPIs, etc.)
    TASKS = "TASKS"
    SKILLS = "SKILLS"
    COMP_BENEFITS = "COMP_BENEFITS"  # salary & benefits
    RECRUITMENT = "RECRUITMENT"      # hiring process
    PUBLICATION = "PUBLICATION"      # language & publication


# --------------------------------------------------------------------------- #
# 2) Keys per step – **UI sequence** inside each expander
# --------------------------------------------------------------------------- #
STEP_KEYS: Dict[WizardStep, List[str]] = {
    WizardStep.BASIC: [
        "job_title",
        "input_url",
        "uploaded_file",
        "job_type",
        "contract_type",
        "job_level",
        "role_description",
        "role_type",
        "date_of_employment_start",
    ],
    WizardStep.COMPANY: [
        "company_name",
        "city",
        "headquarters_location",
        "company_website",
    ],
    WizardStep.DEPARTMENT: [
        "brand_name",
        "team_structure",
        "reports_to",
        "supervises",
    ],
    WizardStep.ROLE: [  # optional / advanced
        "role_performance_metrics",
        "role_priority_projects",
        "travel_requirements",
        "work_schedule",
        "role_keywords",
        "decision_making_authority",
    ],
    WizardStep.TASKS: [
        "task_list",
        "key_responsibilities",
        "technical_tasks",
        "managerial_tasks",
        "administrative_tasks",
        "customer_facing_tasks",
        "internal_reporting_tasks",
        "performance_tasks",
        "innovation_tasks",
        "task_prioritization",
    ],
    WizardStep.SKILLS: [
        "must_have_skills",
        "hard_skills",
        "soft_skills",
        "nice_to_have_skills",
        "certifications_required",
        "language_requirements",
        "tool_proficiency",
        "technical_stack",
        "domain_expertise",
        "leadership_competencies",
        "industry_experience",
        "analytical_skills",
        "communication_skills",
        "project_management_skills",
        "soft_requirement_details",
        "visa_sponsorship",
    ],
    WizardStep.COMP_BENEFITS: [
        "salary_range",
        "currency",
        "pay_frequency",
        "bonus_scheme",
        "commission_structure",
        "vacation_days",
        "remote_work_policy",
        "flexible_hours",
        "relocation_assistance",
        "childcare_support",
    ],
    WizardStep.RECRUITMENT: [
        "recruitment_contact_email",
        "recruitment_steps",
        "recruitment_timeline",
        "number_of_interviews",
        "interview_format",
        "assessment_tests",
        "onboarding_process_overview",
        "recruitment_contact_phone",
        "application_instructions",
    ],
    WizardStep.PUBLICATION: [
        "language_of_ad",
        "translation_required",
        "desired_publication_channels",
    ],
}

# convenience flattened list
ALL_KEYS: List[str] = [k for group in STEP_KEYS.values() for k in group]


# --------------------------------------------------------------------------- #
# 3) UI metadata – ONE dict entry per key
# Only minimal fields are required: label & widget.  Add options/help as needed.
# --------------------------------------------------------------------------- #
FIELD_META: Dict[str, Dict[str, Any]] = {
    # BASIC ------------------------------------------------------------------
    "job_title": {
        "label": "Jobtitel / Job Title",
        "widget": "text_input",
        "required": True,
    },
    "input_url": {
        "label": "JD‑URL / Job Description URL",
        "widget": "text_input",
    },
    "uploaded_file": {
        "label": "Upload JD (PDF/DOCX/TXT)",
        "widget": "file_uploader",
    },
    "job_type": {
        "label": "Beschäftigungsart / Employment Type",
        "widget": "selectbox",
        "options": [
            "Vollzeit (Full‑time)",
            "Teilzeit (Part‑time)",
            "Freelance",
            "Werkstudent",
        ],
    },
    "contract_type": {
        "label": "Vertragsart / Contract Type",
        "widget": "selectbox",
        "options": [
            "Unbefristet (Permanent)",
            "Befristet (Fixed‑term)",
            "Praktikum (Internship)",
            "Freier Mitarbeiter (Contract)",
        ],
    },
    "job_level": {
        "label": "Karrierestufe / Seniority Level",
        "widget": "selectbox",
        "options": [
            "Einsteiger (Entry)",
            "Junior",
            "Mid‑Level",
            "Senior",
            "Lead",
            "Direktor (Director)",
        ],
    },
    "role_description": {
        "label": "Rollenbeschreibung / Role Description",
        "widget": "text_area",
        "required": True,
    },
    "role_type": {
        "label": "Rollentyp / Role Type",
        "widget": "multiselect",
        "options": [
            "Technisch",
            "Führungsposition",
            "Administrativ",
        ],
    },
    "date_of_employment_start": {
        "label": "Startdatum / Start Date",
        "widget": "date_input",
        "default": datetime.date.today,
    },

    # COMPANY ---------------------------------------------------------------
    "company_name": {"label": "Unternehmensname / Company Name", "widget": "text_input"},
    "city": {"label": "Stadt / City", "widget": "text_input"},
    "headquarters_location": {"label": "Hauptsitz / Headquarters", "widget": "text_input"},
    "company_website": {"label": "Website / Company URL", "widget": "text_input"},

    # DEPARTMENT ------------------------------------------------------------
    "brand_name": {"label": "Marke / Brand", "widget": "text_input"},
    "team_structure": {"label": "Teamstruktur / Team Structure", "widget": "text_area"},
    "reports_to": {"label": "Berichtet an / Reports To", "widget": "text_input"},
    "supervises": {"label": "Führt Aufsicht über / Supervises", "widget": "text_input"},

    # ROLE (advanced) -------------------------------------------------------
    "role_performance_metrics": {"label": "KPIs / Performance Metrics", "widget": "text_area"},
    "role_priority_projects": {"label": "Priority Projects", "widget": "text_area"},
    "travel_requirements": {"label": "Reisebereitschaft / Travel", "widget": "text_input"},
    "work_schedule": {"label": "Arbeitszeiten / Work Schedule", "widget": "text_input"},
    "role_keywords": {"label": "Keywords", "widget": "text_input"},
    "decision_making_authority": {"label": "Entscheidungskompetenz / Authority", "widget": "text_input"},

    # TASKS -----------------------------------------------------------------
    "task_list": {"label": "Aufgabenliste / Task List", "widget": "text_area", "required": True},
    "key_responsibilities": {"label": "Key Responsibilities", "widget": "text_area"},
    "technical_tasks": {"label": "Technische Aufgaben", "widget": "text_area"},
    "managerial_tasks": {"label": "Management‑Aufgaben", "widget": "text_area"},
    "administrative_tasks": {"label": "Administrative Aufgaben", "widget": "text_area"},
    "customer_facing_tasks": {"label": "Kundenkontakt‑Aufgaben", "widget": "text_area"},
    "internal_reporting_tasks": {"label": "Reporting intern", "widget": "text_area"},
    "performance_tasks": {"label": "Performance‑Aufgaben", "widget": "text_area"},
    "innovation_tasks": {"label": "Innovations‑Aufgaben", "widget": "text_area"},
    "task_prioritization": {"label": "Aufgabenpriorisierung", "widget": "text_area"},

    # SKILLS ----------------------------------------------------------------
    "must_have_skills": {"label": "Must‑have Skills", "widget": "text_area", "required": True},
    "hard_skills": {"label": "Hard Skills", "widget": "text_area"},
    "soft_skills": {"label": "Soft Skills", "widget": "text_area"},
    "nice_to_have_skills": {"label": "Nice‑to‑have Skills", "widget": "text_area"},
    "certifications_required": {"label": "Zertifikate", "widget": "text_input"},
    "language_requirements": {"label": "Sprachkenntnisse", "widget": "text_input"},
    "tool_proficiency": {"label": "Tool‑Proficiency", "widget": "text_input"},
    "technical_stack": {"label": "Technischer Stack", "widget": "text_input"},
    "domain_expertise": {"label": "Fachexpertise", "widget": "text_area"},
    "leadership_competencies": {"label": "Leadership‑Kompetenzen", "widget": "text_area"},
    "industry_experience": {"label": "Branchenerfahrung", "widget": "text_area"},
    "analytical_skills": {"label": "Analytische Fähigkeiten", "widget": "text_area"},
    "communication_skills": {"label": "Kommunikationsfähigkeiten", "widget": "text_area"},
    "project_management_skills": {"label": "Projektmanagement‑Skills", "widget": "text_area"},
    "soft_requirement_details": {"label": "Soft‑Req Details", "widget": "text_area"},
    "visa_sponsorship": {"label": "Visa Sponsorship", "widget": "text_input"},

    # COMPENSATION & BENEFITS ----------------------------------------------
    "salary_range": {"label": "Gehaltsrange", "widget": "text_input", "required": True},
    "currency": {
        "label": "Währung / Currency",
        "widget": "selectbox",
        "options": ["EUR", "USD", "GBP", "CHF", "Other"],
    },
    "pay_frequency": {
        "label": "Pay Frequency",
        "widget": "selectbox",
        "options": ["Monatlich", "Jährlich", "Wöchentlich"],
    },
    "bonus_scheme": {"label": "Bonusregelung", "widget": "text_area"},
    "commission_structure": {"label": "Provision", "widget": "text_area"},
    "vacation_days": {"label": "Urlaubstage", "widget": "number_input"},
    "remote_work_policy": {
        "label": "Remote Work",
        "widget": "selectbox",
        "options": ["None", "Hybrid", "Fully Remote"],
    },
    "flexible_hours": {"label": "Gleitzeit", "widget": "checkbox"},
    "relocation_assistance": {"label": "Umzugshilfe", "widget": "checkbox"},
    "childcare_support": {"label": "Kinderbetreuung", "widget": "checkbox"},

    # RECRUITMENT PROCESS ---------------------------------------------------
    "recruitment_contact_email": {"label": "Kontakt‑Email", "widget": "text_input", "required": True},
    "recruitment_steps": {"label": "Recruitment Steps", "widget": "text_area"},
    "recruitment_timeline": {"label": "Zeitleiste", "widget": "text_input"},
    "number_of_interviews": {"label": "# Interviews", "widget": "number_input"},
    "interview_format": {"label": "Interviewformat", "widget": "text_input"},
    "assessment_tests": {"label": "Assessment‑Tests", "widget": "text_input"},
    "onboarding_process_overview": {"label": "Onboarding Prozess", "widget": "text_area"},
    "recruitment_contact_phone": {"label": "Kontakt‑Telefon", "widget": "text_input"},
    "application_instructions": {"label": "Bewerbungsanweisungen", "widget": "text_area"},

    # PUBLICATION -----------------------------------------------------------
    "language_of_ad": {
        "label": "Anzeige-Sprache",
        "widget": "selectbox",
        "options": ["Deutsch", "English"],
    },
    "translation_required": {"label": "Übersetzung benötigt?", "widget": "checkbox"},
    "desired_publication_channels": {
        "label": "Publikationskanäle",
        "widget": "multiselect",
        "options": ["LinkedIn", "Indeed", "Company Website", "Internal Portal", "Others"],
    },
}

# Sanity‑check at import time -------------------------------------------------
_missing = [k for k in ALL_KEYS if k not in FIELD_META]
if _missing:
    raise ValueError(f"FIELD_META is missing definitions for: {_missing}")

del _missing

def get_fields_for_step(step: WizardStep):
    return [
        {
            "key": name,
            **meta
        }
        for name, meta in field_map.items()
        if meta.get("step") == step
    ]


def get_fields():
    return list(field_map.keys())

def get_fields_by_group(step: WizardStep, prio_max: int = None):
    """Returns a dict: group name -> list of field dicts (including 'key')."""
    groups = {}
    for name, meta in field_map.items():
        if meta.get("step") != step:
            continue
        if prio_max is not None and meta.get("prio", 3) > prio_max:
            continue
        group = meta.get("group", "General")  # fallback group name
        if group not in groups:
            groups[group] = []
        groups[group].append({"key": name, **meta})
    return groups
