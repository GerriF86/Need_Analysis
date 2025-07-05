"""Client for interacting with the ESCO REST API."""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Union

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://ec.europa.eu/esco/api"


def search_skills(query: str, *, language: str = "en", limit: int = 10) -> List[str]:
    """Search skills in ESCO and return a list of titles.

    Args:
        query: Text query for the search endpoint.
        language: ISO language code, defaults to "en".
        limit: Maximum number of results to return.

    Returns:
        List of skill titles.
    """
    params: Dict[str, Union[str, int]] = {
        "text": query,
        "language": language,
        "type": "skill",
        "limit": limit,
    }
    try:
        response = requests.get(f"{BASE_URL}/search", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("_embedded", {}).get("results", [])
        return [r.get("title") for r in results if r.get("title")]
    except Exception as exc:  # pragma: no cover - network
        logger.warning("ESCO API request failed: %s", exc)
        return []


def _find_occupation_uri(job_title: str, *, language: str) -> Optional[str]:
    """Return the ESCO URI for the given ``job_title`` if found."""

    params: Dict[str, Union[str, int]] = {
        "text": job_title,
        "language": language,
        "type": "occupation",
        "limit": 1,
        "full": "true",
    }
    response = requests.get(f"{BASE_URL}/search", params=params, timeout=10)
    response.raise_for_status()
    results = response.json().get("_embedded", {}).get("results", [])
    if not results:
        return None
    return results[0].get("uri")


def get_skills_for_job_title(
    job_title: str, *, language: str = "en", limit: int = 10
) -> List[str]:
    """Return essential skills for ``job_title`` from ESCO."""

    try:
        occ_uri = _find_occupation_uri(job_title, language=language)
        if not occ_uri:
            return []
        params: Dict[str, Union[str, int]] = {
            "uri": occ_uri,
            "relation": "hasEssentialSkill",
            "language": language,
            "limit": limit,
            "full": "false",
        }
        resp = requests.get(f"{BASE_URL}/resource/related", params=params, timeout=10)
        resp.raise_for_status()
        skills = resp.json().get("_embedded", {}).get("hasEssentialSkill", [])
        return [s.get("title") for s in skills if s.get("title")]
    except Exception as exc:  # pragma: no cover - network
        logger.warning("ESCO API request failed: %s", exc)
        return []


def get_tasks_for_job_title(
    job_title: str, *, language: str = "en", limit: int = 10
) -> List[str]:
    """Return a list of typical tasks for ``job_title`` from ESCO."""

    try:
        occ_uri = _find_occupation_uri(job_title, language=language)
        if not occ_uri:
            return []
        params: Dict[str, Union[str, int]] = {
            "uri": occ_uri,
            "language": language,
        }
        resp = requests.get(
            f"{BASE_URL}/resource/occupation", params=params, timeout=10
        )
        resp.raise_for_status()
        desc = resp.json().get("description", {}).get(language, {}).get("literal", "")
        if not desc:
            return []
        sentences = [s.strip() for s in desc.split(".") if s.strip()]
        return sentences[:limit]
    except Exception as exc:  # pragma: no cover - network
        logger.warning("ESCO API request failed: %s", exc)
        return []
