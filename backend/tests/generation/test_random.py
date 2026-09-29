from app.domain.models import Choice, Question, QuestionType
from app.generation.random import RandomAnswerGenerator


def test_generates_text_answer():
    generator = RandomAnswerGenerator(seed=42)

    question = Question(
        name="name",
        type=QuestionType.TEXT,
        label="What is your name?",
    )

    answer = generator.generate(question)

    assert isinstance(answer, str)
    assert answer


def test_generates_integer_answer():
    generator = RandomAnswerGenerator(seed=42)

    question = Question(
        name="age",
        type=QuestionType.INTEGER,
        label="How old are you?",
    )

    answer = generator.generate(question)

    assert isinstance(answer, int)


def test_generates_decimal_answer():
    generator = RandomAnswerGenerator(seed=42)

    question = Question(
        name="height",
        type=QuestionType.DECIMAL,
        label="Height?",
    )

    answer = generator.generate(question)

    assert isinstance(answer, float)


def test_generates_boolean_answer():
    generator = RandomAnswerGenerator(seed=42)

    question = Question(
        name="student",
        type=QuestionType.BOOLEAN,
        label="Are you a student?",
    )

    answer = generator.generate(question)

    assert isinstance(answer, bool)


def test_generates_select_one_from_choices():
    generator = RandomAnswerGenerator(seed=42)

    question = Question(
        name="sex",
        type=QuestionType.SELECT_ONE,
        label="Sex",
        choices=[
            Choice(value="male", label="Male"),
            Choice(value="female", label="Female"),
        ],
    )

    answer = generator.generate(question)

    assert answer in {"male", "female"}


def test_generates_select_multiple_from_choices():
    generator = RandomAnswerGenerator(seed=42)

    question = Question(
        name="platforms",
        type=QuestionType.SELECT_MULTIPLE,
        label="Platforms",
        choices=[
            Choice(value="facebook", label="Facebook"),
            Choice(value="instagram", label="Instagram"),
            Choice(value="tiktok", label="TikTok"),
        ],
    )

    answer = generator.generate(question)

    assert isinstance(answer, list)
    assert all(
        value in {"facebook", "instagram", "tiktok"}
        for value in answer
    )


def test_select_one_without_choices_raises_error():
    generator = RandomAnswerGenerator(seed=42)

    question = Question(
        name="sex",
        type=QuestionType.SELECT_ONE,
        label="Sex",
    )

    try:
        generator.generate(question)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "has no choices" in str(error)


def test_unsupported_question_type_raises_error():
    generator = RandomAnswerGenerator(seed=42)

    question = Question(
        name="date",
        type=QuestionType.DATE,
        label="Date",
    )

    try:
        generator.generate(question)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "Unsupported question type" in str(error)