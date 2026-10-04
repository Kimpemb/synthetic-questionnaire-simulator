from pathlib import Path

from fastapi.testclient import TestClient

from unittest.mock import patch

from app.api.main import app


client = TestClient(app)

FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "forms"
    / "questionnaire_fixture.xlsx"
)


def test_parse_form():
    with FIXTURE.open("rb") as file:
        response = client.post(
            "/forms/parse",
            files={
                "file": (
                    "questionnaire_fixture.xlsx",
                    file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "questionnaire_fixture"
    assert data["title"] == "Test Questionnaire Fixture"

    assert len(data["questions"]) > 0

    question_names = {
        question["name"]
        for question in data["questions"]
    }

    assert "age" in question_names
    assert "sex" in question_names
    assert "tried_food_from_social_media" in question_names
    assert "food_frequency" in question_names

def test_parse_form_cleans_up_temporary_file():
    with patch(
        "app.api.routes.forms.os.unlink"
    ) as unlink:
        with FIXTURE.open("rb") as file:
            response = client.post(
                "/forms/parse",
                files={
                    "file": (
                        "questionnaire_fixture.xlsx",
                        file,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                },
            )

    assert response.status_code == 200
    unlink.assert_called_once()
