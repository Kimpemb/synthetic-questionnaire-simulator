from app.domain.models import (
    Constraint,
    Question,
    QuestionType,
)
from app.validation.engine import ValidationEngine


def test_constraint_accepts_valid_value():
    question = Question(
        name="age",
        type=QuestionType.INTEGER,
        label="Age",
        constraint=Constraint(
            expression="${age} >= 15 and ${age} <= 100"
        ),
    )

    result = ValidationEngine().validate(
        question,
        25,
    )

    assert result.valid
    assert result.errors == []


def test_constraint_rejects_value_below_minimum():
    question = Question(
        name="age",
        type=QuestionType.INTEGER,
        label="Age",
        constraint=Constraint(
            expression="${age} >= 15 and ${age} <= 100"
        ),
    )

    result = ValidationEngine().validate(
        question,
        12,
    )

    assert not result.valid
    assert result.errors[0].type.value == "constraint"


def test_constraint_rejects_value_above_maximum():
    question = Question(
        name="age",
        type=QuestionType.INTEGER,
        label="Age",
        constraint=Constraint(
            expression="${age} >= 15 and ${age} <= 100"
        ),
    )

    result = ValidationEngine().validate(
        question,
        101,
    )

    assert not result.valid
    assert result.errors[0].type.value == "constraint"


def test_constraint_accepts_zero_for_non_negative_value():
    question = Question(
        name="social_media_days",
        type=QuestionType.INTEGER,
        label="Social media days",
        constraint=Constraint(
            expression="${social_media_days} >= 0 and ${social_media_days} <= 7"
        ),
    )

    result = ValidationEngine().validate(
        question,
        0,
    )

    assert result.valid


def test_constraint_rejects_negative_value():
    question = Question(
        name="social_media_days",
        type=QuestionType.INTEGER,
        label="Social media days",
        constraint=Constraint(
            expression="${social_media_days} >= 0 and ${social_media_days} <= 7"
        ),
    )

    result = ValidationEngine().validate(
        question,
        -1,
    )

    assert not result.valid
    assert result.errors[0].type.value == "constraint"