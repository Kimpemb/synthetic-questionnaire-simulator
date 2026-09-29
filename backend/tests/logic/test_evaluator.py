from app.logic.evaluator import ExpressionEvaluator


def test_evaluates_string_equality():
    evaluator = ExpressionEvaluator()

    answers = {"sex": "female"}

    assert evaluator.evaluate(
        "${sex} = 'female'",
        answers,
    ) is True


def test_evaluates_string_inequality():
    evaluator = ExpressionEvaluator()

    answers = {"sex": "male"}

    assert evaluator.evaluate(
        "${sex} != 'female'",
        answers,
    ) is True


def test_evaluates_numeric_comparison():
    evaluator = ExpressionEvaluator()

    answers = {"age": 25}

    assert evaluator.evaluate(
        "${age} >= 18",
        answers,
    ) is True


def test_evaluates_and_expression():
    evaluator = ExpressionEvaluator()

    answers = {
        "age": 25,
        "student": True,
    }

    assert evaluator.evaluate(
        "${age} >= 18 and ${student} = true",
        answers,
    ) is True


def test_evaluates_or_expression():
    evaluator = ExpressionEvaluator()

    answers = {"sex": "male"}

    assert evaluator.evaluate(
        "${sex} = 'female' or ${sex} = 'male'",
        answers,
    ) is True


def test_missing_reference_returns_false():
    evaluator = ExpressionEvaluator()

    answers = {}

    assert evaluator.evaluate(
        "${sex} = 'female'",
        answers,
    ) is False