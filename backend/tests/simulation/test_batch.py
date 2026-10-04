from app.domain.models import (
    Form,
    GenerationStrategy,
    Question,
    QuestionType,
    SimulationConfig,
    SimulationResult,
    SimulationStatus,
)
from app.generation.random import RandomAnswerGenerator
from app.simulation.batch import BatchSimulationEngine
from app.simulation.engine import SimulationEngine
 


def create_form():
    return Form(
        id="test-form",
        title="Test Form",
        questions=[
            Question(
                name="age",
                type=QuestionType.INTEGER,
                label="Age",
            )
        ],
    )


def create_engine():
    return SimulationEngine(
        answer_generator=RandomAnswerGenerator(seed=42),
        max_generation_attempts=3,
    )


def create_config(count=5):
    return SimulationConfig(
        respondent_count=count,
        generation_strategy=GenerationStrategy.RANDOM,
        max_generation_attempts=3,
        seed=42,
    )


def test_batch_simulation_completes_all_respondents():
    engine = BatchSimulationEngine(
        simulation_engine=create_engine(),
         
    )

    result = engine.simulate(
        create_form(),
        create_config(count=5),
    )

    assert result.status == SimulationStatus.COMPLETED
    assert result.total_requested == 5
    assert result.total_completed == 5
    assert result.total_failed == 0
    assert len(result.results) == 5


def test_batch_simulation_preserves_failed_results():
    class FailingSimulationEngine:
        def simulate(self, form, respondent):
            return SimulationResult(
                respondent_id=respondent.id,
                answers={},
                status=SimulationStatus.FAILED,
            )

    engine = BatchSimulationEngine(
        simulation_engine=FailingSimulationEngine(),
         
    )

    result = engine.simulate(
        create_form(),
        create_config(count=3),
    )

    assert result.status == SimulationStatus.FAILED
    assert result.total_requested == 3
    assert result.total_completed == 0
    assert result.total_failed == 3
    assert len(result.results) == 3


def test_batch_simulation_rejects_unsupported_strategy():
    engine = BatchSimulationEngine(
        simulation_engine=create_engine(),
         
    )

    config = SimulationConfig(
        respondent_count=5,
        generation_strategy=GenerationStrategy.PERSONA,
        max_generation_attempts=3,
    )

    try:
        engine.simulate(create_form(), config)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == (
            "Only RANDOM generation strategy is supported"
        )


def test_batch_simulation_reports_partial_when_some_fail():
    class PartiallyFailingSimulationEngine:
        def __init__(self):
            self._count = 0

        def simulate(self, form, respondent):
            self._count += 1

            status = (
                SimulationStatus.COMPLETED
                if self._count <= 2
                else SimulationStatus.FAILED
            )

            return SimulationResult(
                respondent_id=respondent.id,
                answers={},
                status=status,
            )

    engine = BatchSimulationEngine(
        simulation_engine=PartiallyFailingSimulationEngine(),
         
    )

    result = engine.simulate(
        create_form(),
        create_config(count=4),
    )

    assert result.status == SimulationStatus.PARTIAL
    assert result.total_requested == 4
    assert result.total_completed == 2
    assert result.total_failed == 2
    assert len(result.results) == 4

def test_batch_simulation_is_reproducible_with_same_seed():
    config = create_config(count=5)
    form = create_form()

    first_engine = BatchSimulationEngine(
        simulation_engine=create_engine(),
    )

    second_engine = BatchSimulationEngine(
        simulation_engine=create_engine(),
    )

    first_result = first_engine.simulate(form, config)
    second_result = second_engine.simulate(form, config)

    assert first_result.status == second_result.status
    assert first_result.total_requested == second_result.total_requested
    assert first_result.total_completed == second_result.total_completed
    assert first_result.total_failed == second_result.total_failed

    first_respondent_ids = [
        result.respondent_id
        for result in first_result.results
    ]

    second_respondent_ids = [
        result.respondent_id
        for result in second_result.results
    ]

    assert first_respondent_ids == second_respondent_ids

    assert [
        result.answers
        for result in first_result.results
    ] == [
        result.answers
        for result in second_result.results
    ]
