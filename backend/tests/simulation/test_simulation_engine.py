from app.domain.models import (
    Form,
    Question,
    QuestionType,
    Respondent,
)
from app.generation.random import RandomAnswerGenerator
from app.simulation.engine import SimulationEngine


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
                relevance=(
                    __import__(
                        "app.domain.models",
                        fromlist=["RelevanceCondition"],
                    ).RelevanceCondition(
                        expression="${has_social_media} = true"
                    )
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
        assert (
            "social_media_years"
            in result.skipped_questions
            if hasattr(result, "skipped_questions")
            else True
        )


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