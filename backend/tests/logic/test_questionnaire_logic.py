from pathlib import Path

from app.logic.engine import LogicEngine
from app.parser.xlsform_parser import XLSFormParser


FIXTURE = (
    Path(__file__).parents[1]
    / "forms"
    / "questionnaire_fixture.xlsx"
)


def get_question(form, name):
    return next(
        question
        for question in form.questions
        if question.name == name
    )


def test_food_frequency_relevance():
    form = XLSFormParser().parse(FIXTURE)
    engine = LogicEngine()

    question = get_question(
        form,
        "food_frequency",
    )

    assert engine.is_relevant(
        question,
        {"tried_food_from_social_media": "yes"},
    ) is True

    assert engine.is_relevant(
        question,
        {"tried_food_from_social_media": "no"},
    ) is False


def test_vigorous_work_relevance():
    form = XLSFormParser().parse(FIXTURE)
    engine = LogicEngine()

    question = get_question(
        form,
        "vigorous_work_days",
    )

    assert engine.is_relevant(
        question,
        {"vigorous_work_activity": "yes"},
    ) is True

    assert engine.is_relevant(
        question,
        {"vigorous_work_activity": "no"},
    ) is False


def test_moderate_work_relevance():
    form = XLSFormParser().parse(FIXTURE)
    engine = LogicEngine()

    question = get_question(
        form,
        "moderate_work_days",
    )

    assert engine.is_relevant(
        question,
        {"moderate_work_activity": "yes"},
    ) is True

    assert engine.is_relevant(
        question,
        {"moderate_work_activity": "no"},
    ) is False


def test_walk_cycle_relevance():
    form = XLSFormParser().parse(FIXTURE)
    engine = LogicEngine()

    question = get_question(
        form,
        "walk_cycle_days",
    )

    assert engine.is_relevant(
        question,
        {"walk_or_cycle": "yes"},
    ) is True

    assert engine.is_relevant(
        question,
        {"walk_or_cycle": "no"},
    ) is False