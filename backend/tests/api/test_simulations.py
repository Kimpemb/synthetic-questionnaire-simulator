from pathlib import Path

from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)

FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "forms"
    / "questionnaire_fixture.xlsx"
)


def test_run_simulation():
    with FIXTURE.open("rb") as file:
        response = client.post(
            "/simulations/run",
            files={
                "file": (
                    "questionnaire_fixture.xlsx",
                    file,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
            data={
                "respondent_count": "5",
                "max_generation_attempts": "100",
                "seed": "42",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["simulation"]["status"] == "completed"
    assert data["simulation"]["total_requested"] == 5
    assert data["simulation"]["total_completed"] == 5
    assert data["simulation"]["total_failed"] == 0

    assert len(data["results"]) == 5

    for result in data["results"]:
        assert result["status"] == "completed"
        assert result["respondent_id"]
        assert result["answers"]
        assert result["visited_questions"]
