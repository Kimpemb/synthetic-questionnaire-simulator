from app.domain.models import (
    BatchSimulationResult,
    Form,
    GenerationStrategy,
    SimulationConfig,
    SimulationResult,
    SimulationStatus,
)
from app.simulation.engine import SimulationEngine
from app.simulation.respondent import RespondentGenerator


class BatchSimulationEngine:
    def __init__(
        self,
        simulation_engine: SimulationEngine,
    ):
        self._simulation_engine = simulation_engine

    def simulate(
        self,
        form: Form,
        config: SimulationConfig,
    ) -> BatchSimulationResult:
        if config.respondent_count < 1:
            raise ValueError(
                "respondent_count must be at least 1"
            )

        if (
            config.generation_strategy
            != GenerationStrategy.RANDOM
        ):
            raise ValueError(
                "Only RANDOM generation strategy is supported"
            )

        respondent_generator = RespondentGenerator(
            seed=config.seed
        )

        results: list[SimulationResult] = []

        for _ in range(config.respondent_count):
            respondent = respondent_generator.generate(
                profile=config.respondent_profile
            )

            result = self._simulation_engine.simulate(
                form,
                respondent,
            )

            results.append(result)

        total_completed = sum(
            result.status == SimulationStatus.COMPLETED
            for result in results
        )

        total_failed = sum(
            result.status == SimulationStatus.FAILED
            for result in results
        )

        if total_completed == config.respondent_count:
            status = SimulationStatus.COMPLETED
        elif total_completed == 0:
            status = SimulationStatus.FAILED
        else:
            status = SimulationStatus.PARTIAL

        return BatchSimulationResult(
            results=results,
            status=status,
            total_requested=config.respondent_count,
            total_completed=total_completed,
            total_failed=total_failed,
        )
