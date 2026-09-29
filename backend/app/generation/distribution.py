import random


class DistributionAnswerGenerator:
    def __init__(
        self,
        distribution: dict[str, float],
        seed: int | None = None,
    ):
        self._validate_distribution(distribution)

        self._distribution = distribution
        self._random = random.Random(seed)

    def generate(self):
        values = list(self._distribution.keys())
        probabilities = list(self._distribution.values())

        return self._random.choices(
            values,
            weights=probabilities,
            k=1,
        )[0]

    def _validate_distribution(
        self,
        distribution: dict[str, float],
    ):
        if not distribution:
            raise ValueError(
                "Distribution cannot be empty"
            )

        if any(
            probability < 0
            for probability in distribution.values()
        ):
            raise ValueError(
                "Distribution cannot contain negative probabilities"
            )

        if not self._sums_to_one(distribution):
            raise ValueError(
                "Distribution probabilities must sum to 1"
            )

    def _sums_to_one(
        self,
        distribution: dict[str, float],
    ) -> bool:
        return abs(
            sum(distribution.values()) - 1.0
        ) < 1e-9