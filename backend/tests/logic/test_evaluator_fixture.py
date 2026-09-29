from app.logic.evaluator import ExpressionEvaluator


def test_evaluates_questionnaire_food_frequency_condition():
    evaluator = ExpressionEvaluator()

    answers = {
        "tried_food_from_social_media": "yes",
    }

    assert evaluator.evaluate(
        "${tried_food_from_social_media} = 'yes'",
        answers,
    ) is True


def test_skips_food_frequency_when_condition_is_false():
    evaluator = ExpressionEvaluator()

    answers = {
        "tried_food_from_social_media": "no",
    }

    assert evaluator.evaluate(
        "${tried_food_from_social_media} = 'yes'",
        answers,
    ) is False


def test_evaluates_vigorous_activity_condition():
    evaluator = ExpressionEvaluator()

    answers = {
        "vigorous_work_activity": "yes",
    }

    assert evaluator.evaluate(
        "${vigorous_work_activity} = 'yes'",
        answers,
    ) is True


def test_evaluates_numeric_activity_constraint():
    evaluator = ExpressionEvaluator()

    answers = {
        "vigorous_work_days": 4,
    }

    assert evaluator.evaluate(
        "${vigorous_work_days} >= 0 and ${vigorous_work_days} <= 7",
        answers,
    ) is True