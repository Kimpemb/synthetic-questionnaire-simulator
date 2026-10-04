from pathlib import Path

from app.domain.models import SimulationStatus
from app.generation.random import RandomAnswerGenerator
from app.parser.xlsform_parser import XLSFormParser
from app.simulation.engine import SimulationEngine
from app.simulation.respondent import RespondentGenerator


FIXTURE_PATH = (
    Path(__file__).parents[1]
    / "forms"
    / "questionnaire_fixture.xlsx"
)


def test_simulation_traverses_real_questionnaire():
    form = XLSFormParser().parse(FIXTURE_PATH)

    respondent = RespondentGenerator(
        seed=42
    ).generate()

    engine = SimulationEngine(
        answer_generator=RandomAnswerGenerator(
            seed=42
        )
    )

    result = engine.simulate(
        form,
        respondent,
    )

    assert result.status == SimulationStatus.COMPLETED
    assert result.respondent_id == respondent.id

    assert result.answers
    assert result.visited_questions

    assert (
        len(result.answers)
        == len(result.visited_questions)
    )

    assert not set(
        result.answers
    ).intersection(
        result.skipped_questions
    )