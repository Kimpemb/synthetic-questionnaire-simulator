from app.domain.models import (
    BatchSimulationResult,
    Form,
    Question,
    QuestionType,
    SimulationResult,
    SimulationStatus,
)
from app.output.csv import CSVOutputGenerator


def create_form():
    return Form(
        id="test-form",
        title="Test Form",
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
            ),
            SimulationResult(
                respondent_id="respondent-2",
                answers={
                    "age": 25,
                },
                status=SimulationStatus.COMPLETED,
            ),
        ],
        status=SimulationStatus.COMPLETED,
        total_requested=2,
        total_completed=2,
        total_failed=0,
    )


def test_csv_output_contains_expected_headers():
    output = CSVOutputGenerator().generate(
        create_form(),
        create_result(),
    )

    lines = output.splitlines()

    assert lines[0] == "respondent_id,age,name"


def test_csv_output_contains_one_row_per_respondent():
    output = CSVOutputGenerator().generate(
        create_form(),
        create_result(),
    )

    lines = output.splitlines()

    assert len(lines) == 3


def test_csv_output_contains_answers():
    output = CSVOutputGenerator().generate(
        create_form(),
        create_result(),
    )

    lines = output.splitlines()

    assert "respondent-1,20,Alice" in lines
    assert "respondent-2,25," in lines


def test_csv_output_uses_empty_value_for_missing_answer():
    output = CSVOutputGenerator().generate(
        create_form(),
        create_result(),
    )

    lines = output.splitlines()

    assert lines[2] == "respondent-2,25,"

def test_csv_output_escapes_special_characters():
    form = Form(
        id="test-form",
        title="Test Form",
        questions=[
            Question(
                name="response",
                type=QuestionType.TEXT,
                label="Response",
            )
        ],
    )

    result = BatchSimulationResult(
        results=[
            SimulationResult(
                respondent_id="respondent-1",
                answers={
                    "response": 'Hello, "world"\nNew line',
                },
                status=SimulationStatus.COMPLETED,
            )
        ],
        status=SimulationStatus.COMPLETED,
        total_requested=1,
        total_completed=1,
        total_failed=0,
    )

    output = CSVOutputGenerator().generate(
        form,
        result,
    )

    lines = output.splitlines()

    assert lines[0] == "respondent_id,response"
    assert '"Hello, ""world""' in output
    assert "New line" in output
