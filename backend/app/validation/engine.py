from typing import Any

from app.domain.models import (
    Question,
    QuestionType,
    ValidationError,
    ValidationErrorType,
    ValidationResult,
)
from app.logic.evaluator import ExpressionEvaluator


class ValidationEngine:
    def __init__(
        self,
        evaluator: ExpressionEvaluator | None = None,
    ):
        self._evaluator = evaluator or ExpressionEvaluator()

    def validate(
        self,
        question: Question,
        value: Any,
        answers: dict[str, Any] | None = None,
    ) -> ValidationResult:
        errors = []
        answers = answers or {}

        required_error = self._validate_required(
            question,
            value,
        )

        if required_error:
            errors.append(required_error)
            return ValidationResult(
                valid=False,
                errors=errors,
            )

        if self._is_empty(value):
            return ValidationResult(valid=True)

        type_error = self._validate_type(
            question,
            value,
        )

        if type_error:
            errors.append(type_error)
            return ValidationResult(
                valid=False,
                errors=errors,
            )

        choice_error = self._validate_choices(
            question,
            value,
        )

        if choice_error:
            errors.append(choice_error)

        constraint_error = self._validate_constraint(
            question,
            value,
            answers,
        )

        if constraint_error:
            errors.append(constraint_error)

        return ValidationResult(
            valid=not errors,
            errors=errors,
        )

    def _validate_required(
        self,
        question: Question,
        value: Any,
    ) -> ValidationError | None:
        if not question.required:
            return None

        if self._is_empty(value):
            return ValidationError(
                question=question.name,
                type=ValidationErrorType.REQUIRED,
                message="This question is required.",
                value=value,
            )

        return None

    def _validate_type(
        self,
        question: Question,
        value: Any,
    ) -> ValidationError | None:
        valid = True

        if question.type == QuestionType.INTEGER:
            valid = (
                isinstance(value, int)
                and not isinstance(value, bool)
            )

        elif question.type == QuestionType.DECIMAL:
            valid = (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
            )

        elif question.type == QuestionType.TEXT:
            valid = isinstance(value, str)

        elif question.type == QuestionType.BOOLEAN:
            valid = isinstance(value, bool)

        elif question.type == QuestionType.SELECT_ONE:
            valid = isinstance(value, str)

        elif question.type == QuestionType.SELECT_MULTIPLE:
            valid = (
                isinstance(value, list)
                and all(
                    isinstance(item, str)
                    for item in value
                )
            )

        if valid:
            return None

        return ValidationError(
            question=question.name,
            type=ValidationErrorType.TYPE,
            message=(
                f"Invalid value type for "
                f"question '{question.name}'."
            ),
            value=value,
        )

    def _validate_choices(
        self,
        question: Question,
        value: Any,
    ) -> ValidationError | None:
        if question.type not in {
            QuestionType.SELECT_ONE,
            QuestionType.SELECT_MULTIPLE,
        }:
            return None

        allowed_values = {
            choice.value
            for choice in question.choices
        }

        values = (
            [value]
            if question.type == QuestionType.SELECT_ONE
            else value
        )

        invalid_values = [
            item
            for item in values
            if item not in allowed_values
        ]

        if not invalid_values:
            return None

        return ValidationError(
            question=question.name,
            type=ValidationErrorType.CHOICE,
            message=(
                f"Invalid choice(s): "
                f"{invalid_values}"
            ),
            value=value,
        )

    def _validate_constraint(
        self,
        question: Question,
        value: Any,
        answers: dict[str, Any],
    ) -> ValidationError | None:
        if question.constraint is None:
            return None

        evaluation_answers = {
            **answers,
            question.name: value,
        }

        is_valid = self._evaluator.evaluate(
            question.constraint.expression,
            evaluation_answers,
            current_value=value,
        )

        if is_valid:
            return None

        message = (
            question.constraint.message
            or f"Value violates constraint for "
            f"question '{question.name}'."
        )

        return ValidationError(
            question=question.name,
            type=ValidationErrorType.CONSTRAINT,
            message=message,
            value=value,
        )

    def _is_empty(self, value: Any) -> bool:
        return value is None or value == ""