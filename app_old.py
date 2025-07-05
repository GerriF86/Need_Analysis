import os
import re
import json
import asyncio
from typing import Dict, List, Tuple

import streamlit as st
import requests
from bs4 import BeautifulSoup

# Optional PDF extraction dependency
try:
    import pdfplumber
except ImportError:  # pragma: no cover
    pdfplumber = None

"""Vacalyser – Recruitment Need Analysis Wizard (v0.2)
-------------------------------------------------------
Adds:
• Confidence meter for every autofilled field.
• Manual overwrite (always possible via text inputs).
• Async OpenAI call so UI stays responsive.
• st.cache_data caching for heavy I/O & extraction.
"""

###########################################################################
# --------------------------- CONFIGURATION ----------------------------- #
###########################################################################

KEYS: List[str] = [
    "job_title",
    "company",
    "location",
    "email",
    "department",
    "team",
    "tasks",
    "skills",
    "benefits",
]

REGEX_PATTERNS: Dict[str, str] = {
    "email": r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}",
    "location": r"\b(?:Berlin|Munich|Frankfurt|Hamburg|Stuttgart|Cologne)\b",
}

OPENAI_MODEL = "gpt-4o-mini"
LLM_CONFIDENCE = 0.7  # default confid­ence when GPT fills a value
REGEX_CONFIDENCE = 0.9  # default confid­ence for regex hits
TITLE_HEURISTIC_CONFIDENCE = 0.6

###########################################################################
# ---------------------------- UTILITIES -------------------------------- #
###########################################################################

@st.cache_data(show_spinner="Fetching URL …", ttl=86_400)
def load_text_from_url(url: str) -> str:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        st.error(f"Failed to fetch URL: {exc}")
        return ""
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.get_text(separator=" ")


def load_text_from_upload(file) -> str:
    """File object → plain text. Not cached because `file` isn’t hashable."""
    if file.type == "application/pdf":
        if pdfplumber is None:
            st.error("📄 pdfplumber missing. 👉 pip install pdfplumber")
            return ""
        with pdfplumber.open(file) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
            return "\n".join(pages)
    return file.read().decode("utf-8", errors="ignore")


def regex_extract(text: str) -> Tuple[Dict[str, str], Dict[str, float]]:
    data, conf = {}, {}
    for key, pattern in REGEX_PATTERNS.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            data[key] = match.group(0).strip()
            conf[key] = REGEX_CONFIDENCE

    # Title heuristic
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    for line in lines[:20]:
        if 3 < len(line.split()) <= 10 and line.istitle():
            data.setdefault("job_title", line)
            conf.setdefault("job_title", TITLE_HEURISTIC_CONFIDENCE)
            break
    return data, conf


async def _llm_extract_async(text: str, missing_keys: List[str]) -> Dict[str, str]:
    import openai
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.warning("OPENAI_API_KEY not set – skipping LLM fallback 💤")
        return {}

    openai.api_key = api_key
    system = (
        "You are a data‑extraction function. Return a JSON object with ONLY the keys: "
        + ", ".join(missing_keys)
    )
    user = "Extract the requested information from the following job advert.\n\n" + text[:12000]

    try:
        response = await openai.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=0,
            max_tokens=300,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return json.loads(response.choices[0].message.content)
    except Exception as exc:  # pragma: no cover
        st.error(f"LLM extraction failed: {exc}")
        return {}


@st.cache_data(show_spinner="🔎 Extracting …", ttl=86_400)
def extract_structured_data(text: str) -> Tuple[Dict[str, str], Dict[str, float]]:
    """Regex first, async LLM for the rest, plus confidence map."""
    data, conf = regex_extract(text)
    missing = [k for k in KEYS if k not in data]
    if missing:
        llm_data = asyncio.run(_llm_extract_async(text, missing_keys=missing))
        for k, v in llm_data.items():
            if v:
                data[k] = v
                conf[k] = LLM_CONFIDENCE
    return data, conf

###########################################################################
# -------------------------- WIZARD HELPERS ----------------------------- #
###########################################################################

STEP_TITLES = [
    "Source", "Company", "Department & Team", "Tasks & Responsibilities", "Skills", "Benefits", "Recruitment Process", "Summary",
]
TOTAL_STEPS = len(STEP_TITLES)


def goto(step: int):
    st.session_state["step"] = step
    st.rerun()

###########################################################################
# ----------------------------- COMPONENTS ------------------------------ #
###########################################################################

def draw_confidence(key: str):
    conf = st.session_state.get("confidence", {}).get(key, 0.0)
    if conf:
        st.metric("Confidence", f"{conf*100:.0f}%")
    else:
        st.caption("no confidence yet")

##########################
# ----- Step screens ----
##########################

def step_source():
    st.subheader("📥 Provide Job Ad Source")
    mode = st.radio("Select input mode", ["Upload file", "Paste URL"], horizontal=True)

    raw_text = ""
    if mode == "Upload file":
        file = st.file_uploader("Upload a PDF or text file", type=["pdf", "txt"], accept_multiple_files=False)
        if file and st.button("Extract ➡️"):
            raw_text = load_text_from_upload(file)
    else:
        url = st.text_input("Job ad URL")
        if url and st.button("Extract ➡️"):
            raw_text = load_text_from_url(url)

    if raw_text:
        st.session_state["raw_text"] = raw_text
        data, conf = extract_structured_data(raw_text)
        st.session_state["extracted"] = data
        st.session_state["confidence"] = conf
        st.session_state["wizard_data"] = {}  # reset
        st.success("Extraction complete! Proceed to Company step.")
        goto(1)


def step_company():
    st.subheader("🏢 Company Information")
    extracted = st.session_state.get("extracted", {})
    confidence = st.session_state.get("confidence", {})

    col1, col2 = st.columns([3, 1])
    with col1:
        company = st.text_input("Company name", value=extracted.get("company", ""))
    with col2:
        draw_confidence("company")

    col1, col2 = st.columns([3, 1])
    with col1:
        location = st.text_input("Location", value=extracted.get("location", ""))
    with col2:
        draw_confidence("location")

    if st.button("Next ➡️"):
        st.session_state["wizard_data"]["company"] = {
            "company": company,
            "location": location,
        }
        goto(2)
    if st.button("⬅️ Back"):
        goto(0)


def step_department_team():
    st.subheader("👥 Department & Team")
    extracted = st.session_state.get("extracted", {})

    col1, col2 = st.columns([3, 1])
    with col1:
        department = st.text_input("Department", value=extracted.get("department", ""))
    with col2:
        draw_confidence("department")

    col1, col2 = st.columns([3, 1])
    with col1:
        team = st.text_input("Team", value=extracted.get("team", ""))
    with col2:
        draw_confidence("team")

    if st.button("Next ➡️"):
        st.session_state["wizard_data"]["department_team"] = {
            "department": department,
            "team": team,
        }
        goto(3)
    if st.button("⬅️ Back"):
        goto(1)


def step_tasks():
    st.subheader("📝 Tasks & Responsibilities")
    extracted = st.session_state.get("extracted", {})
    confidence = st.session_state.get("confidence", {})

    tasks = st.text_area("Describe the main tasks …", value=extracted.get("tasks", ""), height=150)
    draw_confidence("tasks")

    if st.button("Next ➡️"):
        st.session_state["wizard_data"]["tasks"] = tasks
        goto(4)
    if st.button("⬅️ Back"):
        goto(2)


def step_skills():
    st.subheader("💡 Skills")
    extracted = st.session_state.get("extracted", {})
    skills = st.text_area("List the required skills …", value=extracted.get("skills", ""), height=150)
    draw_confidence("skills")

    if st.button("Next ➡️"):
        st.session_state["wizard_data"]["skills"] = skills
        goto(5)
    if st.button("⬅️ Back"):
        goto(3)


def step_benefits():
    st.subheader("🎁 Benefits")
    extracted = st.session_state.get("extracted", {})
    benefits = st.text_area("Describe benefits …", value=extracted.get("benefits", ""), height=150)
    draw_confidence("benefits")

    if st.button("Next ➡️"):
        st.session_state["wizard_data"]["benefits"] = benefits
        goto(6)
    if st.button("⬅️ Back"):
        goto(4)


def step_process():
    st.subheader("🚀 Recruitment Process")
    process = st.text_area("Outline the recruitment steps …", height=150)

    if st.button("Next ➡️"):
        st.session_state["wizard_data"]["process"] = process
        goto(7)
    if st.button("⬅️ Back"):
        goto(5)


def step_summary():
    st.subheader("📊 Summary – Review & Export")
    wizard_data = st.session_state.get("wizard_data", {})
    st.json(wizard_data, expanded=False)

    if st.button("⬅️ Back"):
        goto(6)

    if st.button("Download JSON"):
        st.download_button(
            label="Download", data=json.dumps(wizard_data, indent=2), mime="application/json", file_name="recruitment_need.json",
        )

###########################################################################
# ----------------------------- MAIN ------------------------------------ #
###########################################################################

def main():
    st.set_page_config(page_title="Vacalyser – Recruitment Need Wizard", page_icon="📋", layout="centered")
    st.title("Vacalyser · Recruitment Need Analysis Wizard 🧙‍♂️")
    st.markdown("AI‑assisted form filling with confidence scores and full manual control.")

    st.session_state.setdefault("step", 0)
    current = st.session_state["step"]
    st.progress((current + 1) / TOTAL_STEPS, text=f"Step {current + 1} / {TOTAL_STEPS}: {STEP_TITLES[current]}")

    {0: step_source, 1: step_company, 2: step_department_team, 3: step_tasks, 4: step_skills, 5: step_benefits, 6: step_process, 7: step_summary}[current]()


if __name__ == "__main__":
    main()
