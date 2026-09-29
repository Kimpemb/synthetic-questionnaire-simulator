from pathlib import Path

from app.parser.xlsform_parser import XLSFormParser
from app.domain.models import Form, QuestionType


FIXTURE = Path(__file__).parent.parent / "forms" / "questionnaire_fixture.xlsx"


def test_parser_returns_form():
    parser = XLSFormParser()

    form = parser.parse(FIXTURE)

    assert isinstance(form, Form)

def test_parser_reads_form_metadata():
    parser = XLSFormParser()

    form = parser.parse(FIXTURE)

    assert form.id
    assert form.title
    assert form.metadata

def test_parser_reads_questions():
    parser = XLSFormParser()

    form = parser.parse(FIXTURE)

    assert len(form.questions) > 0
    assert form.questions[0].name
    assert form.questions[0].label


def test_parser_maps_question_type():
    parser = XLSFormParser()

    form = parser.parse(FIXTURE)

    age_question = next(
        question for question in form.questions if question.name == "age"
    )

    assert age_question.type == QuestionType.INTEGER
    assert age_question.required is True

def test_parser_reads_question_choices():
    parser = XLSFormParser()

    form = parser.parse(FIXTURE)

    sex_question = next(
        question for question in form.questions if question.name == "sex"
    )

    assert sex_question.type == QuestionType.SELECT_ONE
    assert len(sex_question.choices) == 2


def test_parser_reads_relevance_and_constraint():
    parser = XLSFormParser()

    form = parser.parse(FIXTURE)

    food_frequency = next(
        question for question in form.questions
        if question.name == "food_frequency"
    )

    assert food_frequency.relevance is not None
    assert food_frequency.relevance.expression
    assert food_frequency.constraint is not None
    assert food_frequency.constraint.expression