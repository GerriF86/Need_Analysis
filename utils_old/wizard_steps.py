"""Streamlit wizard steps for job data collection."""

from __future__ import annotations

import streamlit as st

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

import datetime

from utils.utils_jobinfo import (
    display_fields_summary,
    basic_field_extraction,
    extract_text,
    save_fields_to_session,
)
from utils.i18n import tr
from utils.esco_client import (
    search_skills,
    get_skills_for_job_title,
    get_tasks_for_job_title,
)
import requests


def wizard_step_1_basic() -> None:
    """Step 1: capture basic job data."""
    lang = st.session_state.get("lang", "de")
    st.header(tr("1. Grunddaten / Basic Data", lang))
    st.subheader(
        tr(
            "Das Tool hilft Linemanagern, Informationsverluste im Recruiting zu vermeiden und den besten Kandidaten langfristig zu binden. / "
            "The tool helps line managers avoid losing information in recruiting and retain the best candidates long-term.",
            lang,
        )
    )
    fields = st.session_state.get("job_fields", {})
    job_title = st.text_input(
        tr("Jobtitel / Job Title *", lang),
        fields.get("job_title", ""),
    )
    if fields:
        display_fields_summary()

    if not job_title:
        st.warning(tr("Bitte Jobtitel eingeben. / Please enter job title.", lang))

    uploaded_file = st.file_uploader(
        tr(
            "W\u00e4hle eine Datei (PDF, DOCX, TXT) / Choose a file (PDF, DOCX, TXT)",
            lang,
        ),
        type=["pdf", "docx", "txt"],
    )
    url_input = st.text_input(tr("...oder gib eine URL ein / ...or enter a URL", lang))

    if uploaded_file or url_input:
        if (
            uploaded_file
            and "last_uploaded" not in st.session_state
            or (
                uploaded_file
                and uploaded_file.name != st.session_state.get("last_uploaded", None)
            )
        ):
            text = extract_text(uploaded_file)
            fields_update = basic_field_extraction(text)
            fields_update["uploaded_file"] = uploaded_file.name
            save_fields_to_session(fields_update)
            st.session_state["last_uploaded"] = uploaded_file.name

        if url_input and url_input != st.session_state.get("last_url", ""):
            try:  # pragma: no cover - network
                response = requests.get(url_input, timeout=10)
                response.raise_for_status()
                text = response.text
                fields_update = basic_field_extraction(text)
                fields_update["input_url"] = url_input
                save_fields_to_session(fields_update)
                st.session_state["last_url"] = url_input
            except Exception as exc:  # pragma: no cover - network
                st.error(f"Fehler beim Laden der URL: {exc}")

    fields["job_title"] = job_title
    st.session_state["job_fields"] = fields


def wizard_step_2_company() -> None:
    """Step 2: company information."""
    lang = st.session_state.get("lang", "de")
    fields = st.session_state.get("job_fields", {})
    st.header(
        tr(
            f"2. Unternehmensdaten / Company Info – {fields.get('company_name', '')}",
            lang,
        )
    )
    st.subheader(
        tr(
            "Transparente Unternehmensinfos erleichtern Kandidaten die Entscheidung. / Transparent company info helps candidates decide.",
            lang,
        )
    )
    display_fields_summary()
    fields["company_name"] = st.text_input(
        tr("Unternehmen / Company Name *", lang), fields.get("company_name", "")
    )
    fields["city"] = st.text_input(tr("Stadt / City *", lang), fields.get("city", ""))
    with st.expander(tr("Weitere Angaben / More", lang)):
        fields["headquarters_location"] = st.text_input(
            tr("Hauptsitz / Headquarters Location", lang),
            fields.get("headquarters_location", ""),
        )
        fields["company_website"] = st.text_input(
            tr("Unternehmenswebsite / Company Website", lang),
            fields.get("company_website", ""),
        )
    st.session_state["job_fields"] = fields


def wizard_step_3_department() -> None:
    """Step 3: department and team."""
    lang = st.session_state.get("lang", "de")
    fields = st.session_state.get("job_fields", {})
    st.header(tr("3. Abteilung & Team / Department and Team Info", lang))
    display_fields_summary()
    col1, col2 = st.columns(2)
    with col1:
        fields["brand_name"] = st.text_input(
            tr("Markenname / Brand Name", lang), fields.get("brand_name", "")
        )
    with col2:
        fields["team_structure"] = st.text_area(
            tr("Teamstruktur / Team Structure", lang), fields.get("team_structure", "")
        )
    st.session_state["job_fields"] = fields


def wizard_step_4_role() -> None:
    """Step 4: role definition."""
    lang = st.session_state.get("lang", "de")
    fields = st.session_state.get("job_fields", {})
    st.header(tr("4. Rollen-Definition / Role Definition", lang))
    display_fields_summary()
    fields["job_type"] = st.selectbox(
        tr("Jobart / Job Type *", lang),
        [
            tr("Vollzeit / Full-Time", lang),
            tr("Teilzeit / Part-Time", lang),
            tr("Praktikum / Internship", lang),
            "Freelance",
        ],
        index=0,
    )
    fields["contract_type"] = st.selectbox(
        tr("Vertragstyp / Contract Type *", lang),
        [
            tr("Unbefristet / Permanent", lang),
            tr("Befristet / Fixed-term", lang),
            tr("Werkvertrag / Contract for Work", lang),
        ],
        index=0,
    )
    fields["job_level"] = st.selectbox(
        tr("Karrierelevel / Job Level *", lang),
        ["Junior", "Mid", "Senior", "Lead", "Management"],
        index=0,
    )
    fields["role_description"] = st.text_area(
        tr("Rollenbeschreibung / Role Description *", lang),
        fields.get("role_description", ""),
    )
    fields["role_type"] = st.text_input(
        tr("Rollentyp / Role Type *", lang), fields.get("role_type", "")
    )
    col1, col2 = st.columns(2)
    with col1:
        start_value = fields.get("date_of_employment_start")
        if isinstance(start_value, str):
            try:
                start_value = datetime.datetime.fromisoformat(start_value).date()
            except ValueError:
                start_value = datetime.date.today()
        elif not isinstance(start_value, datetime.date):
            start_value = datetime.date.today()
        fields["date_of_employment_start"] = st.date_input(
            tr("Startdatum / Start Date", lang),
            start_value,
        )
        fields["role_performance_metrics"] = st.text_area(
            tr("Leistungskennzahlen / Performance Metrics", lang),
            fields.get("role_performance_metrics", ""),
        )
        fields["role_priority_projects"] = st.text_area(
            tr("Prioritätsprojekte / Priority Projects", lang),
            fields.get("role_priority_projects", ""),
        )
        fields["travel_requirements"] = st.text_input(
            tr("Reisebereitschaft / Travel Requirements", lang),
            fields.get("travel_requirements", ""),
        )
    with col2:
        fields["work_schedule"] = st.text_input(
            tr("Arbeitszeiten / Work Schedule", lang),
            fields.get("work_schedule", ""),
        )
        fields["role_keywords"] = st.text_input(
            tr("Schlüsselwörter / Role Keywords", lang),
            fields.get("role_keywords", ""),
        )
        fields["decision_making_authority"] = st.text_input(
            tr("Entscheidungskompetenz / Decision Making Authority", lang),
            fields.get("decision_making_authority", ""),
        )
    with st.expander(tr("Fortgeschritten / Advanced", lang), expanded=False):
        fields["reports_to"] = st.text_input(
            tr("Berichtet an / Reports To", lang), fields.get("reports_to", "")
        )
        fields["supervises"] = st.text_input(
            tr("Führungsspanne / Supervises", lang), fields.get("supervises", "")
        )
    st.session_state["job_fields"] = fields


def wizard_step_5_tasks() -> None:
    """Step 5: tasks and responsibilities."""
    lang = st.session_state.get("lang", "de")
    fields = st.session_state.get("job_fields", {})
    if fields.get("job_title") and not fields.get("task_list"):
        tasks = get_tasks_for_job_title(fields["job_title"], language=lang, limit=5)
        if tasks:
            fields["task_list"] = "\n".join(tasks)
            st.info(tr("Aufgaben von ESCO importiert", lang))
        update_task_list(fields)
    st.header(tr("5. Aufgaben & Verantwortlichkeiten / Tasks & Responsibilities", lang))
    display_fields_summary()
    fields["task_list"] = st.text_area(
        tr("Aufgabenliste / Task List *", lang), fields.get("task_list", "")
    )
    with st.expander(tr("Hauptverantwortlichkeiten / Key Responsibilities", lang)):
        fields["key_responsibilities"] = st.text_area(
            tr("Key Responsibilities", lang), fields.get("key_responsibilities", "")
        )
    col1, col2 = st.columns(2)
    with col1:
        fields["technical_tasks"] = st.text_area(
            tr("Technische Aufgaben / Technical Tasks", lang),
            fields.get("technical_tasks", ""),
        )
        fields["managerial_tasks"] = st.text_area(
            tr("Managementaufgaben / Managerial Tasks", lang),
            fields.get("managerial_tasks", ""),
        )
        fields["administrative_tasks"] = st.text_area(
            tr("Administrative Aufgaben / Administrative Tasks", lang),
            fields.get("administrative_tasks", ""),
        )
        fields["customer_facing_tasks"] = st.text_area(
            tr("Kundenkontakt / Customer Facing Tasks", lang),
            fields.get("customer_facing_tasks", ""),
        )
    with col2:
        fields["internal_reporting_tasks"] = st.text_area(
            tr("Reporting intern / Internal Reporting Tasks", lang),
            fields.get("internal_reporting_tasks", ""),
        )
        fields["performance_tasks"] = st.text_area(
            tr("Performance-Aufgaben / Performance Tasks", lang),
            fields.get("performance_tasks", ""),
        )
        fields["innovation_tasks"] = st.text_area(
            tr("Innovationsaufgaben / Innovation Tasks", lang),
            fields.get("innovation_tasks", ""),
        )
        fields["task_prioritization"] = st.text_area(
            tr("Aufgabenpriorisierung / Task Prioritization", lang),
            fields.get("task_prioritization", ""),
        )
    st.session_state["job_fields"] = fields


def wizard_step_6_skills() -> None:
    """Step 6: required skills."""
    lang = st.session_state.get("lang", "de")
    fields = st.session_state.get("job_fields", {})
    if fields.get("job_title") and not fields.get("must_have_skills"):
        skills = get_skills_for_job_title(fields["job_title"], language=lang, limit=5)
        if skills:
            fields["must_have_skills"] = ", ".join(skills)
            st.info(tr("Skills von ESCO importiert", lang))
        update_must_have_skills(fields)
    update_nice_to_have_skills(fields)
    st.header(tr("6. Skills & Kompetenzen / Skills & Competencies", lang))
    skill_query = st.text_input(
        tr("Skill bei ESCO suchen / Search skill in ESCO", lang)
    )
    if skill_query:
        suggestions = search_skills(skill_query, language=lang, limit=5)
        if suggestions:
            st.info(", ".join(suggestions))
        else:
            st.warning(tr("Keine Ergebnisse von ESCO", lang))
    display_fields_summary()
    fields["must_have_skills"] = st.text_area(
        tr("Must-have Skills *", lang), fields.get("must_have_skills", "")
    )
    with st.expander(tr("Empfohlene Skills", lang)):
        fields["hard_skills"] = st.text_area(
            tr("Hard Skills", lang), fields.get("hard_skills", "")
        )
        fields["soft_skills"] = st.text_area(
            tr("Soft Skills", lang), fields.get("soft_skills", "")
        )
    col1, col2 = st.columns(2)
    with col1:
        fields["nice_to_have_skills"] = st.text_area(
            tr("Nice-to-have Skills", lang), fields.get("nice_to_have_skills", "")
        )
        fields["certifications_required"] = st.text_area(
            tr("Zertifikate / Certifications Required", lang),
            fields.get("certifications_required", ""),
        )
        fields["language_requirements"] = st.text_area(
            tr("Sprachkenntnisse / Language Requirements", lang),
            fields.get("language_requirements", ""),
        )
        fields["tool_proficiency"] = st.text_area(
            tr("Toolkenntnisse / Tool Proficiency", lang),
            fields.get("tool_proficiency", ""),
        )
        fields["technical_stack"] = st.text_area(
            tr("Technischer Stack / Technical Stack", lang),
            fields.get("technical_stack", ""),
        )
    with col2:
        fields["domain_expertise"] = st.text_area(
            tr("Fachexpertise / Domain Expertise", lang),
            fields.get("domain_expertise", ""),
        )
        fields["leadership_competencies"] = st.text_area(
            tr("Leadership-Kompetenzen / Leadership Competencies", lang),
            fields.get("leadership_competencies", ""),
        )
        fields["industry_experience"] = st.text_area(
            tr("Branchenerfahrung / Industry Experience", lang),
            fields.get("industry_experience", ""),
        )
        fields["analytical_skills"] = st.text_area(
            tr("Analytische Fähigkeiten / Analytical Skills", lang),
            fields.get("analytical_skills", ""),
        )
        fields["communication_skills"] = st.text_area(
            tr("Kommunikationsfähigkeiten / Communication Skills", lang),
            fields.get("communication_skills", ""),
        )
        fields["project_management_skills"] = st.text_area(
            tr("Projektmanagement / Project Management Skills", lang),
            fields.get("project_management_skills", ""),
        )
        fields["soft_requirement_details"] = st.text_area(
            tr("Details zu Soft Requirements", lang),
            fields.get("soft_requirement_details", ""),
        )
        fields["visa_sponsorship"] = st.text_input(
            tr("Visa Sponsorship", lang), fields.get("visa_sponsorship", "")
        )
    st.session_state["job_fields"] = fields


def wizard_step_7_compensation() -> None:
    """Step 7: compensation and benefits."""
    lang = st.session_state.get("lang", "de")
    fields = st.session_state.get("job_fields", {})
    st.header(tr("7. Vergütung & Benefits / Compensation & Benefits", lang))
    display_fields_summary()
    update_salary_range(fields)
    update_bonus_scheme(fields)
    update_commission_structure(fields)
    update_publication_channels(fields)
    fields["salary_range"] = st.text_input(
        tr("Gehaltsrange / Salary Range *", lang), fields.get("salary_range", "")
    )
    fields["currency"] = st.selectbox(
        tr("Währung / Currency *", lang), ["EUR", "CHF", "GBP", "USD", "other"], index=0
    )
    fields["pay_frequency"] = st.selectbox(
        tr("Auszahlungsrhythmus / Pay Frequency *", lang),
        [
            tr("Monatlich / Monthly", lang),
            tr("Jährlich / Annually", lang),
            tr("Wöchentlich / Weekly", lang),
        ],
        index=0,
    )
    with st.expander(tr("Optionale Benefits", lang)):
        col1, col2 = st.columns(2)
        with col1:
            fields["bonus_scheme"] = st.text_area(
                tr("Bonusregelung / Bonus Scheme", lang), fields.get("bonus_scheme", "")
            )
            fields["commission_structure"] = st.text_area(
                tr("Provisionsmodell / Commission Structure", lang),
                fields.get("commission_structure", ""),
            )
            fields["vacation_days"] = st.text_input(
                tr("Urlaubstage / Vacation Days", lang), fields.get("vacation_days", "")
            )
            fields["remote_work_policy"] = st.text_area(
                tr("Remote-Regelung / Remote Work Policy", lang),
                fields.get("remote_work_policy", ""),
            )
            fields["flexible_hours"] = st.text_input(
                tr("Flexible Arbeitszeiten / Flexible Hours", lang),
                fields.get("flexible_hours", ""),
            )
    col1, col2 = st.columns(2)
    with col1:
        fields["relocation_assistance"] = st.text_area(
            tr("Umzugshilfe / Relocation Assistance", lang),
            fields.get("relocation_assistance", ""),
        )
    with col2:
        fields["childcare_support"] = st.text_area(
            tr("Kinderbetreuung / Childcare Support", lang),
            fields.get("childcare_support", ""),
        )
    st.session_state["job_fields"] = fields


def wizard_step_8_recruitment() -> None:
    """Step 8: recruitment process."""
    lang = st.session_state.get("lang", "de")
    fields = st.session_state.get("job_fields", {})
    st.header(tr("8. Bewerbungsprozess / Recruitment Process", lang))
    display_fields_summary()
    fields["recruitment_contact_email"] = st.text_input(
        tr("Recruiting-Kontakt E-Mail * / Contact Email *", lang),
        fields.get("recruitment_contact_email", ""),
    )
    with st.expander(tr("Recruitment Steps", lang)):
        fields["recruitment_steps"] = st.text_area(
            tr("Prozessschritte / Recruitment Steps", lang),
            fields.get("recruitment_steps", ""),
        )
    col1, col2 = st.columns(2)
    with col1:
        fields["recruitment_timeline"] = st.text_input(
            tr("Zeitleiste / Recruitment Timeline", lang),
            fields.get("recruitment_timeline", ""),
        )
        fields["number_of_interviews"] = st.text_input(
            tr("Anzahl Interviews / Number of Interviews", lang),
            fields.get("number_of_interviews", ""),
        )
        fields["interview_format"] = st.text_input(
            tr("Interviewformat / Interview Format", lang),
            fields.get("interview_format", ""),
        )
        fields["assessment_tests"] = st.text_area(
            tr("Assessment-Tests", lang), fields.get("assessment_tests", "")
        )
    with col2:
        fields["onboarding_process_overview"] = st.text_area(
            tr("Onboarding-Prozess / Onboarding Process", lang),
            fields.get("onboarding_process_overview", ""),
        )
        fields["recruitment_contact_phone"] = st.text_input(
            tr("Telefon Recruiting-Kontakt / Contact Phone", lang),
            fields.get("recruitment_contact_phone", ""),
        )
        fields["application_instructions"] = st.text_area(
            tr("Bewerbungsanweisungen / Application Instructions", lang),
            fields.get("application_instructions", ""),
        )
    st.session_state["job_fields"] = fields


def wizard_step_9_publication() -> None:
    """Step 9: language and publication settings."""
    lang = st.session_state.get("lang", "de")
    fields = st.session_state.get("job_fields", {})
    update_publication_channels(fields)
    update_translation_required(fields)
    st.header(tr("9. Sprache & Veröffentlichung / Language & Publication", lang))
    display_fields_summary()
    fields["language_of_ad"] = st.selectbox(
        tr("Anzeigensprache / Ad Language", lang),
        ["Deutsch", "English"],
        index=0 if fields.get("language_of_ad", "Deutsch") == "Deutsch" else 1,
    )
    fields["desired_publication_channels"] = st.text_input(
        tr("Publikationskanäle / Publication Channels", lang),
        fields.get("desired_publication_channels", ""),
    )
    fields["translation_required"] = st.text_input(
        tr("Übersetzung nötig? / Translation Required?", lang),
        fields.get("translation_required", ""),
    )
    st.session_state["job_fields"] = fields
