import re

from typing import Any


class ExpressionEvaluator:
    REFERENCE_PATTERN = re.compile(r"\$\{(\w+)\}")

    def evaluate(
        self,
        expression: str,
        answers: dict[str, Any],
        current_value: Any = None,
    ) -> bool:
        expression = expression.strip()

        if not expression:
            return False

        try:
            return self._evaluate_expression(
                expression,
                answers,
                current_value,
            )
        except (ValueError, TypeError, KeyError):
            return False

    def _evaluate_expression(
        self,
        expression: str,
        answers: dict[str, Any],
        current_value: Any = None,
    ) -> bool:
        or_parts = self._split_operator(
            expression,
            " or ",
        )

        if len(or_parts) > 1:
            return any(
                self._evaluate_expression(
                    part,
                    answers,
                    current_value,
                )
                for part in or_parts
            )

        and_parts = self._split_operator(
            expression,
            " and ",
        )

        if len(and_parts) > 1:
            return all(
                self._evaluate_expression(
                    part,
                    answers,
                    current_value,
                )
                for part in and_parts
            )

        return self._evaluate_comparison(
            expression,
            answers,
            current_value,
        )

    def _evaluate_comparison(
        self,
        expression: str,
        answers: dict[str, Any],
        current_value: Any = None,
    ) -> bool:
        match = re.match(
            r"^\s*(\$\{\w+\}|\.)\s*(>=|<=|!=|==|=|>|<)\s*(.+?)\s*$",
            expression,
        )

        if not match:
            raise ValueError(
                f"Unsupported expression: {expression}"
            )

        reference, operator, raw_value = match.groups()

        if reference == ".":
            actual_value = current_value
        else:
            question_name = self._extract_reference(
                reference
            )

            if question_name not in answers:
                return False

            actual_value = answers[question_name]

        if self.REFERENCE_PATTERN.fullmatch(
            raw_value.strip()
        ):
            expected_question = self._extract_reference(
                raw_value.strip()
            )

            if expected_question not in answers:
                return False

            expected_value = answers[expected_question]
        else:
            expected_value = self._parse_value(
                raw_value
            )

        return self._compare(
            actual_value,
            operator,
            expected_value,
        )

    def _extract_reference(
        self,
        reference: str,
    ) -> str:
        match = self.REFERENCE_PATTERN.fullmatch(
            reference
        )

        if not match:
            raise ValueError(
                f"Invalid reference: {reference}"
            )

        return match.group(1)

    def _parse_value(self, value: str) -> Any:
        value = value.strip()

        if (
            len(value) >= 2
            and value[0] == "'"
            and value[-1] == "'"
        ):
            return value[1:-1]

        if (
            len(value) >= 2
            and value[0] == '"'
            and value[-1] == '"'
        ):
            return value[1:-1]

        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            return value

    def _compare(
        self,
        actual: Any,
        operator: str,
        expected: Any,
    ) -> bool:
        if operator in {"=", "=="}:
            return actual == expected

        if operator == "!=":
            return actual != expected

        if operator == ">":
            return actual > expected

        if operator == "<":
            return actual < expected

        if operator == ">=":
            return actual >= expected

        if operator == "<=":
            return actual <= expected

        raise ValueError(
            f"Unsupported operator: {operator}"
        )

    def _split_operator(
        self,
        expression: str,
        operator: str,
    ) -> list[str]:
        return expression.split(operator)