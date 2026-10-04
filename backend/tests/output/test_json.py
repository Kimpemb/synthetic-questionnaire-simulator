import json

from app.domain.models import (
    BatchSimulationResult,
    Form,
    Question,
    QuestionType,
    SimulationResult,
    SimulationStatus,
)
from app.output.json import JSONOutputGenerator


def create_form():
    return Form(
        id="test-form",
        title="Test Form",
        version="1.0",
        questions=[
            Question(
                name="age",
                type=QuestionType.INTEGER,
                label="Age",
            ),
            Question(
                name="name",
                type=QuestionType.TEXT,
                label="Name",
            ),
        ],
    )


def create_result():
    return BatchSimulationResult(
        results=[
            SimulationResult(
                respondent_id="respondent-1",
                answers={
                    "age": 20,
                    "name": "Alice",
                },
                status=SimulationStatus.COMPLETED,
                visited_questions=[
                    "age",
                    "name",
                ],
            )
        ],
        status=SimulationStatus.COMPLETED,
        total_requested=1,
        total_completed=1,
        total_failed=0,
    )


def test_json_output_is_valid_json():
    output = JSONOutputGenerator().generate(
        create_form(),
        create_result(),
    )

    parsed = json.loads(output)

    assert isinstance(parsed, dict)


def test_json_output_contains_form_metadata():
    output = JSONOutputGenerator().generate(
        create_form(),
        create_result(),
    )

    parsed = json.loads(output)

    assert parsed["form"]["id"] == "test-form"
    assert parsed["form"]["title"] == "Test Form"
    assert parsed["form"]["version"] == "1.0"


def test_json_output_contains_simulation_summary():
    output = JSONOutputGenerator().generate(
        create_form(),
        create_result(),
    )

    parsed = json.loads(output)

    assert parsed["simulation"]["status"] == "completed"
    assert parsed["simulation"]["total_requested"] == 1
    assert parsed["simulation"]["total_completed"] == 1
    assert parsed["simulation"]["total_failed"] == 0


def test_json_output_contains_results():
    output = JSONOutputGenerator().generate(
        create_form(),
        create_result(),
    )

    parsed = json.loads(output)

    assert len(parsed["results"]) == 1

    result = parsed["results"][0]

    assert result["respondent_id"] == "respondent-1"
    assert result["status"] == "completed"
    assert result["answers"] == {
        "age": 20,
        "name": "Alice",
    }
    assert result["visited_questions"] == [
        "age",
        "name",
    ]
    assert result["skipped_questions"] == []
