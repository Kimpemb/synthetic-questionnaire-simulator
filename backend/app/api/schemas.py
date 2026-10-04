from pydantic import BaseModel, Field

from app.domain.models import GenerationStrategy


class SimulationRequest(BaseModel):
    respondent_count: int = Field(
        ge=1,
        le=100_000,
    )
    generation_strategy: GenerationStrategy = (
        GenerationStrategy.RANDOM
    )
    max_generation_attempts: int = Field(
        default=3,
        ge=1,
    )
    seed: int | None = None
    respondent_profile: str | dict | None = None


class SimulationSummary(BaseModel):
    status: str
    total_requested: int
    total_completed: int
    total_failed: int


class SimulationResponse(BaseModel):
    simulation: SimulationSummary
    results: list[dict]
