from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, Form, UploadFile

from app.api.schemas import SimulationRequest
from app.domain.models import SimulationConfig
from app.generation.random import RandomAnswerGenerator
from app.parser.xlsform_parser import XLSFormParser
from app.simulation.batch import BatchSimulationEngine
from app.simulation.engine import SimulationEngine


router = APIRouter(
    prefix="/simulations",
    tags=["simulations"],
)


@router.post("/run")
async def run_simulation(
    file: UploadFile = File(...),
    respondent_count: int = Form(...),
    max_generation_attempts: int = Form(3),
    seed: int | None = Form(None),
):
    request = SimulationRequest(
        respondent_count=respondent_count,
        max_generation_attempts=max_generation_attempts,
        seed=seed,
    )

    contents = await file.read()

    with NamedTemporaryFile(
        suffix=".xlsx",
        delete=False,
    ) as temporary_file:
        temporary_file.write(contents)
        temporary_path = temporary_file.name

    try:
        parser = XLSFormParser()
        form = parser.parse(temporary_path)
    finally:
        import os

        os.unlink(temporary_path)

    answer_generator = RandomAnswerGenerator(
        seed=request.seed
    )

    simulation_engine = SimulationEngine(
        answer_generator=answer_generator,
        max_generation_attempts=(
            request.max_generation_attempts
        ),
    )

    batch_engine = BatchSimulationEngine(
        simulation_engine=simulation_engine
    )

    config = SimulationConfig(
        respondent_count=request.respondent_count,
        generation_strategy=request.generation_strategy,
        max_generation_attempts=(
            request.max_generation_attempts
        ),
        seed=request.seed,
        respondent_profile=request.respondent_profile,
    )

    result = batch_engine.simulate(
        form=form,
        config=config,
    )

    return {
        "simulation": {
            "status": result.status.value,
            "total_requested": result.total_requested,
            "total_completed": result.total_completed,
            "total_failed": result.total_failed,
        },
        "results": [
            {
                "respondent_id": simulation_result.respondent_id,
                "status": simulation_result.status.value,
                "answers": simulation_result.answers,
                "visited_questions": (
                    simulation_result.visited_questions
                ),
                "skipped_questions": (
                    simulation_result.skipped_questions
                ),
            }
            for simulation_result in result.results
        ],
    }
