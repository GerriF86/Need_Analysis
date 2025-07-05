from functions.boolean_search import generate_boolean_search


def test_generate_boolean_search_with_list():
    fields = {
        "must_have_skills": ["Python", "SQL"],
        "city": "Berlin",
        "job_title": "Data Scientist",
    }
    result = generate_boolean_search(fields)
    assert result == '("Python" OR "SQL") AND "Data Scientist" AND Berlin'


def test_generate_boolean_search_with_string():
    fields = {
        "must_have_skills": "Python, SQL",
        "city": "Berlin",
        "job_title": "Data Scientist",
    }
    result = generate_boolean_search(fields)
    assert result == '("Python" OR "SQL") AND "Data Scientist" AND Berlin'


def test_generate_boolean_search_without_city():
    fields = {
        "must_have_skills": ["Python", "SQL"],
        "job_title": "Data Scientist",
    }
    result = generate_boolean_search(fields)
    assert result == '("Python" OR "SQL") AND "Data Scientist"'


def test_generate_boolean_search_missing_data():
    fields = {"city": "Berlin"}
    result = generate_boolean_search(fields)
    assert result.startswith("# Nicht genug Daten")
