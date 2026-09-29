import pytest

from app.generation.distribution import DistributionAnswerGenerator


def test_generates_value_from_distribution():
    generator = DistributionAnswerGenerator(
        distribution={
            "male": 0.5,
            "female": 0.5,
        },
        seed=42,
    )

    answer = generator.generate()

    assert answer in {"male", "female"}


def test_same_seed_produces_same_answer():
    distribution = {
        "male": 0.5,
        "female": 0.5,
    }

    generator_one = DistributionAnswerGenerator(
        distribution=distribution,
        seed=42,
    )

    generator_two = DistributionAnswerGenerator(
        distribution=distribution,
        seed=42,
    )

    assert generator_one.generate() == generator_two.generate()


def test_rejects_empty_distribution():
    with pytest.raises(ValueError, match="cannot be empty"):
        DistributionAnswerGenerator(
            distribution={},
            seed=42,
        )


def test_rejects_negative_probability():
    with pytest.raises(ValueError, match="negative"):
        DistributionAnswerGenerator(
            distribution={
                "male": -0.1,
                "female": 1.1,
            },
            seed=42,
        )


def test_rejects_distribution_that_does_not_sum_to_one():
    with pytest.raises(ValueError, match="sum to 1"):
        DistributionAnswerGenerator(
            distribution={
                "male": 0.3,
                "female": 0.3,
            },
            seed=42,
        )