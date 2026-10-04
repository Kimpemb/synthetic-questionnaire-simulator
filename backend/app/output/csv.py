import csv
from io import StringIO
from typing import Any

from app.domain.models import BatchSimulationResult, Form
from app.output.base import OutputGenerator


class CSVOutputGenerator(OutputGenerator):
    def generate(
        self,
        form: Form,
        result: BatchSimulationResult,
    ) -> str:
        output = StringIO()

        fieldnames = [
            "respondent_id",
            *[
                question.name
                for question in form.questions
            ],
        ]

        writer = csv.DictWriter(
            output,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for simulation_result in result.results:
            row: dict[str, Any] = {
                "respondent_id": (
                    simulation_result.respondent_id
                )
            }

            for question in form.questions:
                row[question.name] = (
                    simulation_result.answers.get(
                        question.name,
                        "",
                    )
                )

            writer.writerow(row)

        return output.getvalue()
