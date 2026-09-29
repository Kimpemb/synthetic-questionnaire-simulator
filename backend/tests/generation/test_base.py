import pytest

from app.domain.models import Question, QuestionType
from app.generation.base import AnswerGenerator


class DummyGenerator(AnswerGenerator):
    def generate(self, question: Question):
        return "dummy"


def test_answer_generator_requires_generate_implementation():
    generator = DummyGenerator()

    question = Question(
        name="name",
        type=QuestionType.TEXT,
        label="What is your name?",
    )

    assert generator.generate(question) == "dummy"


def test_answer_generator_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        AnswerGenerator()