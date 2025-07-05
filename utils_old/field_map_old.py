from __future__ import annotations
from enum import Enum
from typing import Dict, List, Any


# -----------------------------------------------------------------------------
# 1) Wizard steps (the order matters for rendering & navigation)
# -----------------------------------------------------------------------------
class WizardStep(str, Enum):
    BASIC = "BASIC"
    COMPANY = "COMPANY"
    DEPARTMENT = "DEPARTMENT"
    ROLE = "ROLE"
    TASKS = "TASKS"
    SKILLS = "SKILLS"
    COMP_BENEFITS = "COMP_BENEFITS"
    RECRUITMENT = "RECRUITMENT"
    PUBLICATION = "PUBLICATION"


# -----------------------------------------------------------------------------
# 2) Flat canonical list of all keys PER STEP
#    – This is the contract every other module relies on.
# -----------------------------------------------------------------------------
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
    WizardStep.ROLE: [  # advanced / misc role meta
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

# Flattened list for quick membership tests
ALL_KEYS: List[str] = [k for keys in STEP_KEYS.values() for k in keys]

FIELD_META: Dict[str, Dict[str, Any]] = {
    # Step 1: Basic Data
    "job_title": {
        "step": WizardStep.BASIC,
        "widget": "text_input",
        "label": "Stellentitel / Job Title",
        "help": "Official role title for the position.",
        "required": True,
        "source": "extracted"
    },
    "input_url": {
        "step": WizardStep.BASIC,
        "widget": "text_input",
        "label": "JD-URL / Job Description URL",
        "help": "Optional URL of an online job description to import.",
        "required": False,
        "source": "user"
    },
    "uploaded_file": {
        "step": WizardStep.BASIC,
        "widget": "file_uploader",
        "label": "Stellenbeschreibung hochladen / Upload Job Description",
        "help": "Upload a PDF or DOCX of the job description for AI extraction.",
        "required": False,
        "source": "user"
    },

    # Step 2: Company Info
    "company_name": {
        "step": WizardStep.COMPANY,
        "widget": "text_input",
        "label": "Unternehmensname / Company Name",
        "help": "Name of the hiring company/organization.",
        "required": True,
        "source": "extracted"
    },
    "city": {
        "step": WizardStep.COMPANY,
        "widget": "text_input",
        "label": "Standort (Stadt) / Job Location (City)",
        "help": "Primary city or location for the job (leave blank if remote).",
        "required": True,
        "source": "extracted"
    },
    "headquarters_location": {
        "step": WizardStep.COMPANY,
        "widget": "text_input",
        "label": "Hauptsitz / Headquarters Location",
        "help": "Company headquarters (if different from job location).",
        "required": False,
        "source": "extracted"
    },
    "company_website": {
        "step": WizardStep.COMPANY,
        "widget": "text_input",
        "label": "Webseite / Company Website",
        "help": "Official website of the company (for reference or display).",
        "required": False,
        "source": "user"
    },

    # Step 3: Department and Team Info
    "brand_name": {
        "step": WizardStep.DEPARTMENT,
        "widget": "text_input",
        "label": "Marke/Abteilung / Brand or Department",
        "help": "Specific brand, division, or department (if applicable).",
        "required": False,
        "source": "user"
    },
    "team_structure": {
        "step": WizardStep.DEPARTMENT,
        "widget": "text_area",
        "label": "Team & Struktur / Team Structure",
        "help": "Brief description of the team and its structure (who the role reports to, team size, etc.).",
        "required": False,
        "source": "user"
    },
    "reports_to": {
        "step": WizardStep.DEPARTMENT,
        "widget": "text_input",
        "label": "Berichtet an / Reports To",
        "help": "The position or person this role reports to (e.g. Manager or Team Lead).",
        "required": False,
        "source": "user"
    },
    "supervises": {
        "step": WizardStep.DEPARTMENT,
        "widget": "text_input",
        "label": "Führt Aufsicht über / Supervises",
        "help": "If a managerial role, list positions or team this role oversees.",
        "required": False,
        "source": "user"
    },

    # Step 4: Role Definition
    "date_of_employment_start": {
        "step": WizardStep.BASIC,
        "widget": "date_input",
        "label": "Startdatum / Start Date",
        "help": "Planned start date of employment.",
        "required": False,
        "source": "extracted"
    },
    "job_type": {
        "step": WizardStep.BASIC,
        "widget": "selectbox",
        "label": "Beschäftigungsart / Employment Type",
        "options": ["Vollzeit (Full-time)", "Teilzeit (Part-time)", "Freelance", "Werkstudent (Working Student)"],
        "help": "Type of employment in terms of hours or commitment.",
        "required": True,
        "source": "extracted"
    },
    "contract_type": {
        "step": WizardStep.BENEFITS,
        "widget": "selectbox",
        "label": "Vertragsart / Contract Type",
        "options": ["Unbefristet (Permanent)", "Befristet (Temporary)", "Praktikum (Internship)", "Freier Mitarbeiter (Contract)"],
        "help": "Type of contract for the role.",
        "required": True,
        "source": "extracted"
    },
    "job_level": {
        "step": WizardStep.BASIC,
        "widget": "selectbox",
        "label": "Karrierestufe / Seniority Level",
        "options": ["Einsteiger (Entry)", "Junior", "Mid-Level", "Senior", "Lead", "Direktor (Director)"],
        "help": "Seniority or career level required for the role.",
        "required": True,
        "source": "extracted"
    },
    "role_description": {
        "step": WizardStep.BASIC,
        "widget": "text_area",
        "label": "Rollenbeschreibung / Role Description",
        "help": "Overview paragraph describing the role's purpose and impact.",
        "required": True,
        "source": "llm"
    },
    "role_type": {
        "step": WizardStep.BASIC,
        "widget": "multiselect",
        "label": "Rollentyp / Role Type",
        "options": ["Technisch (Technical)", "Führungsposition (Managerial)", "Administrativ (Administrative)"],
        "help": "Nature of the role (select one or multiple categories).",
        "required": True,
        "source": "extracted"
    },

    # Step 5: Tasks & Responsibilities
    "task_list": {
        "step": WizardStep.TASKS,
        "widget": "text_area",
        "label": "Aufgaben / Task List",
        "help": "List of main tasks and responsibilities (bullet points).",
        "required": True,
        "source": "extracted"
    },
    "key_responsibilities": {
        "step": WizardStep.TASKS,
        "widget": "text_area",
        "label": "Kernverantwortungen / Key Responsibilities",
        "help": "Key high-level responsibilities (if not evident from task list).",
        "required": False,
        "source": "user"
    },
    "technical_tasks": {
        "step": WizardStep.TASKS,
        "widget": "text_area",
        "label": "Technische Aufgaben / Technical Tasks",
        "help": "Specific technical duties (if applicable to the role).",
        "required": False,
        "source": "user"
    },
    "managerial_tasks": {
        "step": WizardStep.TASKS,
        "widget": "text_area",
        "label": "Leitungsaufgaben / Managerial Tasks",
        "help": "Managerial or leadership duties (for managerial roles).",
        "required": False,
        "source": "user"
    },
    "administrative_tasks": {
        "step": WizardStep.TASKS,
        "widget": "text_area",
        "label": "Administrative Aufgaben / Administrative Tasks",
        "help": "Administrative or support tasks (if applicable).",
        "required": False,
        "source": "user"
    },

    # Step 6: Skills & Competencies
    "must_have_skills": {
        "step": WizardStep.SKILLS,
        "widget": "text_area",
        "label": "Erforderliche Fähigkeiten / Must-have Skills",
        "help": "Essential skills and qualifications candidates must possess.",
        "required": True,
        "source": "extracted"
    },
    "hard_skills": {
        "step": WizardStep.SKILLS,
        "widget": "text_area",
        "label": "Fachliche Skills / Hard Skills",
        "help": "Technical or domain-specific skills required.",
        "required": False,
        "source": "user"
    },
    "soft_skills": {
        "step": WizardStep.SKILLS,
        "widget": "text_area",
        "label": "Soft Skills",
        "help": "Soft skills or personal competencies needed (communication, teamwork, etc.).",
        "required": False,
        "source": "user"
    },
    "nice_to_have_skills": {
        "step": WizardStep.SKILLS,
        "widget": "text_area",
        "label": "Pluspunkte / Nice-to-have Skills",
        "help": "Additional skills or experience that are beneficial but not mandatory.",
        "required": False,
        "source": "user"
    },
    "certifications_required": {
        "step": WizardStep.SKILLS,
        "widget": "text_input",
        "label": "Zertifikate / Required Certifications",
        "help": "Professional certifications or licenses required (if any).",
        "required": False,
        "source": "user"
    },
    "language_requirements": {
        "step": WizardStep.SKILLS,
        "widget": "text_input",
        "label": "Sprachkenntnisse / Language Requirements",
        "help": "Required language proficiencies for candidates (if any).",
        "required": False,
        "source": "user"
    },
    "tool_proficiency": {
        "step": WizardStep.SKILLS,
        "widget": "text_input",
        "label": "Toolkenntnisse / Tool Proficiency",
        "help": "Software or tool proficiencies needed (e.g. Excel, SAP, programming languages).",
        "required": False,
        "source": "user"
    },
    "technical_stack": {
        "step": WizardStep.SKILLS,
        "widget": "text_input",
        "label": "Tech-Stack / Technical Stack",
        "help": "Technologies and frameworks used (for tech roles, e.g. AWS, React, etc.).",
        "required": False,
        "source": "user"
    },

    # Step 7: Compensation & Benefits
    "salary_range": {
        "step": WizardStep.BENEFITS,
        "widget": "text_input",
        "label": "Gehaltsspanne / Salary Range",
        "help": "Expected salary range for the position (e.g. 50-60k).",
        "required": True,
        "source": "user"
    },
    "currency": {
        "step": WizardStep.BENEFITS,
        "widget": "selectbox",
        "label": "Währung / Currency",
        "options": ["EUR", "USD", "GBP", "CHF", "Other"],
        "help": "Currency of the salary (Euro, USD, etc.).",
        "required": True,
        "source": "user"
    },
    "pay_frequency": {
        "step": WizardStep.BENEFITS,
        "widget": "selectbox",
        "label": "Zahlungsfrequenz / Pay Frequency",
        "options": ["Jährlich (Yearly)", "Monatlich (Monthly)", "Stündlich (Hourly)"],
        "help": "Frequency of pay (annual salary, monthly, hourly rate, etc.).",
        "required": True,
        "source": "user"
    },
    "bonus_scheme": {
        "step": WizardStep.BENEFITS,
        "widget": "text_input",
        "label": "Bonusregelung / Bonus Scheme",
        "help": "Description of any bonus or incentive scheme (if applicable).",
        "required": False,
        "source": "user"
    },
    "commission_structure": {
        "step": WizardStep.BENEFITS,
        "widget": "text_input",
        "label": "Provision / Commission Structure",
        "help": "Details of commission (for sales roles, if applicable).",
        "required": False,
        "source": "user"
    },
    "vacation_days": {
        "step": WizardStep.BENEFITS,
        "widget": "number_input",
        "label": "Urlaubstage / Vacation Days",
        "help": "Number of annual vacation days offered.",
        "required": False,
        "source": "user"
    },
    "remote_work_policy": {
        "step": WizardStep.BENEFITS,
        "widget": "selectbox",
        "label": "Home-Office Möglichkeit / Remote Work",
        "options": ["Keine / None", "Teilweise remote / Hybrid", "Vollständig remote / Fully Remote"],
        "help": "Remote work options or policy (none, hybrid, or fully remote).",
        "required": False,
        "source": "user"
    },
    "flexible_hours": {
        "step": WizardStep.BENEFITS,
        "widget": "checkbox",
        "label": "Gleitzeit / Flexible Hours",
        "help": "Check if flexible working hours are offered.",
        "required": False,
        "source": "user"
    },
    "relocation_assistance": {
        "step": WizardStep.BENEFITS,
        "widget": "checkbox",
        "label": "Umzugsunterstützung / Relocation Assistance",
        "help": "Check if relocation support is provided for candidates.",
        "required": False,
        "source": "user"
    },
    "childcare_support": {
        "step": WizardStep.BENEFITS,
        "widget": "checkbox",
        "label": "Kinderbetreuung / Childcare Support",
        "help": "Check if childcare or family support benefits are offered.",
        "required": False,
        "source": "user"
    },

    # Step 8: Recruitment Process
    "recruitment_contact_email": {
        "step": WizardStep.INTERVIEW,
        "widget": "text_input",
        "label": "Kontakt E-Mail / Contact Email",
        "help": "Email address for applications or inquiries.",
        "required": True,
        "source": "user"
    },
    "recruitment_steps": {
        "step": WizardStep.INTERVIEW,
        "widget": "text_area",
        "label": "Bewerbungsprozess / Recruitment Steps",
        "help": "Outline of the recruitment process (interviews, tests, etc.).",
        "required": False,
        "source": "user"
    },
    "recruitment_timeline": {
        "step": WizardStep.INTERVIEW,
        "widget": "text_input",
        "label": "Einstellungszeitplan / Timeline",
        "help": "Estimated timeline for the hiring process (e.g. 4 weeks).",
        "required": False,
        "source": "user"
    },
    "number_of_interviews": {
        "step": WizardStep.INTERVIEW,
        "widget": "number_input",
        "label": "Anzahl Interviews / Number of Interviews",
        "help": "How many interview rounds are planned (if known).",
        "required": False,
        "source": "user"
    },
    "interview_format": {
        "step": WizardStep.INTERVIEW,
        "widget": "text_input",
        "label": "Interviewformat / Interview Format",
        "help": "Format of interviews (phone, video, on-site, etc.).",
        "required": False,
        "source": "user"
    },
    "assessment_tests": {
        "step": WizardStep.INTERVIEW,
        "widget": "text_input",
        "label": "Tests / Assessment Tests",
        "help": "Any assessment or coding tests involved in hiring.",
        "required": False,
        "source": "user"
    },
    "onboarding_process_overview": {
        "step": WizardStep.INTERVIEW,
        "widget": "text_area",
        "label": "Onboarding / Onboarding Process",
        "help": "Brief overview of the onboarding process for the new hire.",
        "required": False,
        "source": "user"
    },
    "recruitment_contact_phone": {
        "step": WizardStep.INTERVIEW,
        "widget": "text_input",
        "label": "Kontakt Telefon / Contact Phone",
        "help": "Contact phone number for queries (optional).",
        "required": False,
        "source": "user"
    },
    "application_instructions": {
        "step": WizardStep.INTERVIEW,
        "widget": "text_area",
        "label": "Bewerbungshinweise / Application Instructions",
        "help": "Specific instructions on how to apply (e.g. apply via company portal).",
        "required": False,
        "source": "user"
    },

    # Step 9: Language & Publication
    "language_of_ad": {
        "step": WizardStep.SUMMARY,
        "widget": "selectbox",
        "label": "Anzeigesprache / Advertisement Language",
        "options": ["Deutsch", "English"],
        "help": "Language of the job ad content to finalize.",
        "required": True,
        "source": "user"
    },
    "translation_required": {
        "step": WizardStep.SUMMARY,
        "widget": "checkbox",
        "label": "Übersetzung benötigt? / Translation needed?",
        "help": "Check if the job ad needs to be translated to another language.",
        "required": False,
        "source": "user"
    },
    "desired_publication_channels": {
        "step": WizardStep.SUMMARY,
        "widget": "multiselect",
        "label": "Veröffentlichungskanäle / Publication Channels",
        "options": ["LinkedIn", "Indeed", "Company Website", "Internal Portal", "Others"],
        "help": "Where the job ad will be published (for planning purposes).",
        "required": False,
        "source": "user"
    }
}

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
