from app.domain.models import (
    Constraint,
    Question,
    QuestionType,
)
from app.validation.engine import ValidationEngine


def test_cross_question_constraint_accepts_valid_answers():
    question = Question(
        name="end_age",
        type=QuestionType.INTEGER,
        label="End age",
        constraint=Constraint(
            expression="${start_age} <= ${end_age}"
        ),
    )

    result = ValidationEngine().validate(
        question,
        30,
        answers={
            "start_age": 25,
            "end_age": 30,
        },
    )

    assert result.valid
    assert result.errors == []


def test_cross_question_constraint_rejects_invalid_answers():
    question = Question(
        name="end_age",
        type=QuestionType.INTEGER,
        label="End age",
        constraint=Constraint(
            expression="${start_age} <= ${end_age}"
        ),
    )

    result = ValidationEngine().validate(
        question,
        20,
        answers={
            "start_age": 25,
            "end_age": 20,
        },
    )

    assert not result.valid
    assert result.errors[0].type.value == "constraint"


def test_cross_question_constraint_uses_current_value():
    question = Question(
        name="daily_hours",
        type=QuestionType.DECIMAL,
        label="Daily hours",
        constraint=Constraint(
            expression="${daily_hours} <= ${available_hours}"
        ),
    )

    result = ValidationEngine().validate(
        question,
        6.0,
        answers={
            "available_hours": 8.0,
        },
    )

    assert result.valid


def test_cross_question_constraint_rejects_when_current_value_exceeds_reference():
    question = Question(
        name="daily_hours",
        type=QuestionType.DECIMAL,
        label="Daily hours",
        constraint=Constraint(
            expression="${daily_hours} <= ${available_hours}"
        ),
    )

    result = ValidationEngine().validate(
        question,
        10.0,
        answers={
            "available_hours": 8.0,
        },
    )

    assert not result.valid
    assert result.errors[0].type.value == "constraint"