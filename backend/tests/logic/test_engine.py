from app.domain.models import (
    Question,
    QuestionType,
    RelevanceCondition,
)
from app.logic.engine import LogicEngine


def test_question_without_relevance_is_relevant():
    engine = LogicEngine()

    question = Question(
        name="age",
        type=QuestionType.INTEGER,
        label="Age",
    )

    assert engine.is_relevant(
        question,
        {},
    ) is True


def test_question_is_relevant_when_condition_is_true():
    engine = LogicEngine()

    question = Question(
        name="food_frequency",
        type=QuestionType.SELECT_ONE,
        label="How often?",
        relevance=RelevanceCondition(
            expression="${tried_food_from_social_media} = 'yes'"
        ),
    )

    answers = {
        "tried_food_from_social_media": "yes",
    }

    assert engine.is_relevant(
        question,
        answers,
    ) is True


def test_question_is_not_relevant_when_condition_is_false():
    engine = LogicEngine()

    question = Question(
        name="food_frequency",
        type=QuestionType.SELECT_ONE,
        label="How often?",
        relevance=RelevanceCondition(
            expression="${tried_food_from_social_media} = 'yes'"
        ),
    )

    answers = {
        "tried_food_from_social_media": "no",
    }

    assert engine.is_relevant(
        question,
        answers,
    ) is False


def test_missing_reference_makes_question_not_relevant():
    engine = LogicEngine()

    question = Question(
        name="food_frequency",
        type=QuestionType.SELECT_ONE,
        label="How often?",
        relevance=RelevanceCondition(
            expression="${tried_food_from_social_media} = 'yes'"
        ),
    )

    assert engine.is_relevant(
        question,
        {},
    ) is False