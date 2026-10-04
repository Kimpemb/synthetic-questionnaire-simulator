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

def test_evaluates_reference_against_reference():
    evaluator = ExpressionEvaluator()

    assert evaluator.evaluate(
        "${start_age} <= ${end_age}",
        {
            "start_age": 25,
            "end_age": 30,
        },
    )


def test_rejects_reference_against_reference_when_false():
    evaluator = ExpressionEvaluator()

    assert not evaluator.evaluate(
        "${start_age} <= ${end_age}",
        {
            "start_age": 35,
            "end_age": 30,
        },
    )


def test_evaluates_current_value_against_reference():
    evaluator = ExpressionEvaluator()

    assert evaluator.evaluate(
        "${daily_hours} <= ${available_hours}",
        {
            "daily_hours": 6.0,
            "available_hours": 8.0,
        },
    )    

def test_evaluates_current_value_greater_than_or_equal():
    evaluator = ExpressionEvaluator()

    assert evaluator.evaluate(
        ". >= 15",
        {},
        current_value=81,
    )


def test_evaluates_current_value_range():
    evaluator = ExpressionEvaluator()

    assert evaluator.evaluate(
        ". >= 15 and . <= 100",
        {},
        current_value=81,
    )