from app.domain.models import (
    Choice,
    Question,
    QuestionType,
)
from app.validation.engine import ValidationEngine


def test_valid_integer_passes():
    question = Question(
        name="age",
        type=QuestionType.INTEGER,
        label="Age",
    )

    result = ValidationEngine().validate(
        question,
        25,
    )

    assert result.valid
    assert result.errors == []


def test_invalid_integer_fails():
    question = Question(
        name="age",
        type=QuestionType.INTEGER,
        label="Age",
    )

    result = ValidationEngine().validate(
        question,
        "twenty-five",
    )

    assert not result.valid
    assert result.errors


def test_required_question_rejects_empty_value():
    question = Question(
        name="name",
        type=QuestionType.TEXT,
        label="Name",
        required=True,
    )

    result = ValidationEngine().validate(
        question,
        "",
    )

    assert not result.valid
    assert result.errors[0].type.value == "required"


def test_optional_question_accepts_empty_value():
    question = Question(
        name="name",
        type=QuestionType.TEXT,
        label="Name",
        required=False,
    )

    result = ValidationEngine().validate(
        question,
        "",
    )

    assert result.valid


def test_select_one_rejects_invalid_choice():
    question = Question(
        name="sex",
        type=QuestionType.SELECT_ONE,
        label="Sex",
        choices=[
            Choice(value="male", label="Male"),
            Choice(value="female", label="Female"),
        ],
    )

    result = ValidationEngine().validate(
        question,
        "unknown",
    )

    assert not result.valid
    assert result.errors[0].type.value == "choice"


def test_select_one_accepts_valid_choice():
    question = Question(
        name="sex",
        type=QuestionType.SELECT_ONE,
        label="Sex",
        choices=[
            Choice(value="male", label="Male"),
            Choice(value="female", label="Female"),
        ],
    )

    result = ValidationEngine().validate(
        question,
        "male",
    )

    assert result.valid


def test_select_multiple_rejects_invalid_choice():
    question = Question(
        name="platforms",
        type=QuestionType.SELECT_MULTIPLE,
        label="Platforms",
        choices=[
            Choice(value="facebook", label="Facebook"),
            Choice(value="twitter", label="Twitter"),
        ],
    )

    result = ValidationEngine().validate(
        question,
        ["facebook", "unknown"],
    )

    assert not result.valid
    assert result.errors[0].type.value == "choice"