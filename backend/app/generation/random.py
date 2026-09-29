import random

from app.domain.models import Question, QuestionType
from app.generation.base import AnswerGenerator


class RandomAnswerGenerator(AnswerGenerator):
    def __init__(self, seed: int | None = None):
        self._random = random.Random(seed)

    def generate(self, question: Question):
        if question.type == QuestionType.TEXT:
            return "Sample response"

        if question.type == QuestionType.INTEGER:
            return self._random.randint(0, 100)

        if question.type == QuestionType.DECIMAL:
            return round(self._random.uniform(0, 100), 2)

        if question.type == QuestionType.BOOLEAN:
            return self._random.choice([True, False])

        if question.type == QuestionType.SELECT_ONE:
            return self._generate_select_one(question)

        if question.type == QuestionType.SELECT_MULTIPLE:
            return self._generate_select_multiple(question)

        raise ValueError(
            f"Unsupported question type: {question.type}"
        )

    def _generate_select_one(self, question: Question):
        if not question.choices:
            raise ValueError(
                f"Question '{question.name}' has no choices"
            )

        choice = self._random.choice(question.choices)

        return choice.value

    def _generate_select_multiple(self, question: Question):
        if not question.choices:
            raise ValueError(
                f"Question '{question.name}' has no choices"
            )

        selected_count = self._random.randint(
            1,
            len(question.choices),
        )

        selected = self._random.sample(
            question.choices,
            selected_count,
        )

        return [choice.value for choice in selected]