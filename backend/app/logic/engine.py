from typing import Any

from app.domain.models import Question
from app.logic.evaluator import ExpressionEvaluator


class LogicEngine:
    def __init__(
        self,
        evaluator: ExpressionEvaluator | None = None,
    ):
        self._evaluator = evaluator or ExpressionEvaluator()

    def is_relevant(
        self,
        question: Question,
        answers: dict[str, Any],
    ) -> bool:
        if question.relevance is None:
            return True

        return self._evaluator.evaluate(
            question.relevance.expression,
            answers,
        )