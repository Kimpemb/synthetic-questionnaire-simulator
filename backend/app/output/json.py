import json
from typing import Any

from app.domain.models import BatchSimulationResult, Form
from app.output.base import OutputGenerator


class JSONOutputGenerator(OutputGenerator):
    def generate(
        self,
        form: Form,
        result: BatchSimulationResult,
    ) -> str:
        output: dict[str, Any] = {
            "form": {
                "id": form.id,
                "title": form.title,
                "version": form.version,
            },
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

        return json.dumps(
            output,
            indent=2,
            ensure_ascii=False,
        )
