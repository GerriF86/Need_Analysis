from unittest.mock import Mock, patch

from utils import esco_client


def test_get_skills_for_job_title():
    search_resp = {"_embedded": {"results": [{"uri": "http://example.com/occ"}]}}
    related_resp = {
        "_embedded": {"hasEssentialSkill": [{"title": "Skill A"}, {"title": "Skill B"}]}
    }
    with patch("utils.esco_client.requests.get") as mock_get:
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: search_resp),
            Mock(status_code=200, json=lambda: related_resp),
        ]
        skills = esco_client.get_skills_for_job_title("Data Scientist")
    assert skills == ["Skill A", "Skill B"]


def test_get_tasks_for_job_title():
    search_resp = {"_embedded": {"results": [{"uri": "http://example.com/occ"}]}}
    occupation_resp = {"description": {"en": {"literal": "Task one. Task two. Other."}}}
    with patch("utils.esco_client.requests.get") as mock_get:
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: search_resp),
            Mock(status_code=200, json=lambda: occupation_resp),
        ]
        tasks = esco_client.get_tasks_for_job_title("Data Scientist")
    assert tasks == ["Task one", "Task two", "Other"][:3]
