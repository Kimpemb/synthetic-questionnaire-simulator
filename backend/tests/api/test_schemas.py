import pytest
from pydantic import ValidationError

from app.api.schemas import SimulationRequest
from app.domain.models import GenerationStrategy


def test_simulation_request_accepts_valid_data():
    request = SimulationRequest(
        respondent_count=100,
        generation_strategy=GenerationStrategy.RANDOM,
        max_generation_attempts=3,
        seed=42,
    )

    assert request.respondent_count == 100
    assert request.generation_strategy == GenerationStrategy.RANDOM
    assert request.max_generation_attempts == 3
    assert request.seed == 42


def test_simulation_request_defaults_generation_strategy():
    request = SimulationRequest(
        respondent_count=10,
    )

    assert (
        request.generation_strategy
        == GenerationStrategy.RANDOM
    )


def test_simulation_request_rejects_zero_respondents():
    with pytest.raises(ValidationError):
        SimulationRequest(
            respondent_count=0,
        )


def test_simulation_request_rejects_negative_attempts():
    with pytest.raises(ValidationError):
        SimulationRequest(
            respondent_count=10,
            max_generation_attempts=0,
        )


def test_simulation_request_rejects_excessive_respondents():
    with pytest.raises(ValidationError):
        SimulationRequest(
            respondent_count=100_001,
        )
