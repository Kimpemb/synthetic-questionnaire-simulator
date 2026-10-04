from app.domain.models import (
    Constraint,
    Form,
    Question,
    QuestionType,
    RelevanceCondition,
    Respondent,
)

from app.generation.base import AnswerGenerator
from app.generation.random import RandomAnswerGenerator
from app.simulation.engine import SimulationEngine


class SequenceAnswerGenerator(AnswerGenerator):
    def __init__(self, answers):
        self._answers = iter(answers)

    def generate(self, question):
        return next(self._answers)


def test_simulation_answers_relevant_questions():
    form = Form(
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

    respondent = Respondent(id="respondent-1")

    engine = SimulationEngine(
        answer_generator=RandomAnswerGenerator(seed=42)
    )

    result = engine.simulate(form, respondent)

    assert result.status.value == "completed"
    assert "age" in result.answers
    assert "name" in result.answers


def test_simulation_skips_irrelevant_questions():
    form = Form(
        id="test-form",
        title="Test Form",
        questions=[
            Question(
                name="has_social_media",
                type=QuestionType.BOOLEAN,
                label="Uses social media",
            ),
            Question(
                name="social_media_years",
                type=QuestionType.INTEGER,
                label="Years using social media",
                relevance=RelevanceCondition(
                    expression="${has_social_media} = true"
                ),
            ),
        ],
    )

    respondent = Respondent(id="respondent-1")

    engine = SimulationEngine(
        answer_generator=RandomAnswerGenerator(seed=1)
    )

    result = engine.simulate(form, respondent)

    if result.answers["has_social_media"] is False:
        assert "social_media_years" not in result.answers
        assert "social_media_years" in result.skipped_questions


def test_simulation_preserves_question_order():
    form = Form(
        id="test-form",
        title="Test Form",
        questions=[
            Question(
                name="first",
                type=QuestionType.TEXT,
                label="First",
            ),
            Question(
                name="second",
                type=QuestionType.TEXT,
                label="Second",
            ),
            Question(
                name="third",
                type=QuestionType.TEXT,
                label="Third",
            ),
        ],
    )

    respondent = Respondent(id="respondent-1")

    engine = SimulationEngine(
        answer_generator=RandomAnswerGenerator(seed=42)
    )

    result = engine.simulate(form, respondent)

    assert list(result.answers.keys()) == [
        "first",
        "second",
        "third",
    ]


def test_simulation_regenerates_invalid_answer_until_valid():
    form = Form(
        id="test-form",
        title="Test Form",
        questions=[
            Question(
                name="age",
                type=QuestionType.INTEGER,
                label="Age",
                constraint=Constraint(
                    expression=". >= 15 and . <= 100"
                ),
            ),
        ],
    )

    respondent = Respondent(id="respondent-1")

    generator = SequenceAnswerGenerator(
        [10, 120, 25]
    )

    engine = SimulationEngine(
        answer_generator=generator,
        max_generation_attempts=3,
    )

    result = engine.simulate(form, respondent)

    assert result.status.value == "completed"
    assert result.answers["age"] == 25


def test_simulation_fails_after_max_generation_attempts():
    form = Form(
        id="test-form",
        title="Test Form",
        questions=[
            Question(
                name="age",
                type=QuestionType.INTEGER,
                label="Age",
                constraint=Constraint(
                    expression=". >= 15 and . <= 100"
                ),
            ),
        ],
    )

    respondent = Respondent(id="respondent-1")

    generator = SequenceAnswerGenerator(
        [10, 120, 5]
    )

    engine = SimulationEngine(
        answer_generator=generator,
        max_generation_attempts=3,
    )

    result = engine.simulate(form, respondent)

    assert result.status.value == "failed"
    assert result.validation is not None
    assert result.validation.valid is False
    assert result.answers == {}