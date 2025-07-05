# utils/keys.py

"""
Canonical list of every wizard field, grouped by step.
The two symbols used below:
★ = mandatory field   ◆ = recommended    ⬚ = optional
(Only informative – they’re all strings in the lists.)
"""


STEP_KEYS: dict[int, list[str]] = {
    1: [  # Step 1: Basic Data
        "job_title",  # ★
        "input_url",  # ⬚
        "uploaded_file",  # ⬚
        "parsed_data_raw",  # ⬚ (internal raw text storage)
    ],
    2: [  # Step 2: Company Info
        "company_name",  # ★
        "city",  # ★
        "headquarters_location",  # ◆
        "company_website",  # ⬚
    ],
    3: [  # Step 3: Department and Team Info
        "brand_name",  # ⬚
        "team_structure",  # ⬚
    ],
    4: [  # Step 4: Role Definition
        "date_of_employment_start",  # ⬚
        "job_type",  # ★
        "contract_type",  # ★
        "job_level",  # ★
        "role_description",  # ★
        "role_type",  # ★
        "reports_to",  # ◆
        "supervises",  # ◆
        "role_performance_metrics",  # ⬚
        "role_priority_projects",  # ⬚
        "travel_requirements",  # ⬚
        "work_schedule",  # ⬚
        "role_keywords",  # ⬚
        "decision_making_authority",  # ⬚
    ],
    5: [  # Step 5: Tasks & Responsibilities
        "task_list",  # ★
        "key_responsibilities",  # ◆
        "technical_tasks",  # ⬚
        "managerial_tasks",  # ⬚
        "administrative_tasks",  # ⬚
        "customer_facing_tasks",  # ⬚
        "internal_reporting_tasks",  # ⬚
        "performance_tasks",  # ⬚
        "innovation_tasks",  # ⬚
        "task_prioritization",  # ⬚
    ],
    6: [  # Step 6: Skills & Competencies
        "must_have_skills",  # ★
        "hard_skills",  # ◆
        "soft_skills",  # ◆
        "nice_to_have_skills",  # ⬚
        "certifications_required",  # ⬚
        "language_requirements",  # ⬚
        "tool_proficiency",  # ⬚
        "technical_stack",  # ⬚
        "domain_expertise",  # ⬚
        "leadership_competencies",  # ⬚
        "industry_experience",  # ⬚
        "analytical_skills",  # ⬚
        "communication_skills",  # ⬚
        "project_management_skills",  # ⬚
        "soft_requirement_details",  # ⬚
        "visa_sponsorship",  # ⬚
    ],
    7: [  # Step 7: Compensation & Benefits
        "salary_range",  # ★
        "currency",  # ★
        "pay_frequency",  # ★
        "bonus_scheme",  # ◆
        "commission_structure",  # ◆
        "vacation_days",  # ◆
        "remote_work_policy",  # ◆
        "flexible_hours",  # ◆
        "relocation_assistance",  # ⬚
        "childcare_support",  # ⬚
    ],
    8: [  # Step 8: Recruitment Process
        "recruitment_contact_email",  # ★
        "recruitment_steps",  # ◆
        "recruitment_timeline",  # ⬚
        "number_of_interviews",  # ⬚
        "interview_format",  # ⬚
        "assessment_tests",  # ⬚
        "onboarding_process_overview",  # ⬚
        "recruitment_contact_phone",  # ⬚
        "application_instructions",  # ⬚
    ],
    9: [  # Step 9: Language & Publication
        "language_of_ad",  # ★
        "translation_required",  # ◆
        "desired_publication_channels",  # ⬚
    ],
}

# Fields generated or used internally (not shown in UI steps)
GENERATED_KEYS: list[str] = [
    "generated_job_ad",
    "generated_interview_prep",
    "generated_email_template",
    "target_group_analysis",
    "generated_boolean_query",
]

# Flattened list of all user-facing field keys for convenience
ALL_STEP_KEYS: list[str] = [key for step in STEP_KEYS.values() for key in step]
