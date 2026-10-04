from app.domain.models import (
    Form,
    Respondent,
    SimulationContext,
    SimulationResult,
    SimulationStatus,
)
from app.generation.base import AnswerGenerator
from app.logic.engine import LogicEngine
from app.validation.engine import ValidationEngine


class SimulationEngine:
    def __init__(
        self,
        answer_generator: AnswerGenerator,
        logic_engine: LogicEngine | None = None,
        validation_engine: ValidationEngine | None = None,
        max_generation_attempts: int = 3,
    ):
        if max_generation_attempts < 1:
            raise ValueError(
                "max_generation_attempts must be at least 1"
            )

        self._answer_generator = answer_generator
        self._logic_engine = (
            logic_engine or LogicEngine()
        )
        self._validation_engine = (
            validation_engine or ValidationEngine()
        )
        self._max_generation_attempts = (
            max_generation_attempts
        )

    def simulate(
        self,
        form: Form,
        respondent: Respondent,
    ) -> SimulationResult:
        context = SimulationContext(
            respondent=respondent,
        )

        for question in form.questions:
            context.current_question = question

            if not self._logic_engine.is_relevant(
                question,
                context.answers,
            ):
                context.skipped_questions.append(
                    question.name
                )
                continue

            answer = None
            validation = None

            for _ in range(
                self._max_generation_attempts
            ):
                answer = self._answer_generator.generate(
                    question
                )

                validation = (
                    self._validation_engine.validate(
                        question,
                        answer,
                        context.answers,
                    )
                )

                if validation.valid:
                    break

            if validation is None or not validation.valid:
                return SimulationResult(
                    respondent_id=respondent.id,
                    answers=context.answers,
                    validation=validation,
                    status=SimulationStatus.FAILED,
                    visited_questions=(
                        context.visited_questions
                    ),
                    skipped_questions=(
                        context.skipped_questions
                    ),
                )

            context.answers[question.name] = answer
            context.visited_questions.append(
                question.name
            )

        return SimulationResult(
            respondent_id=respondent.id,
            answers=context.answers,
            validation=None,
            status=SimulationStatus.COMPLETED,
            visited_questions=(
                context.visited_questions
            ),
            skipped_questions=(
                context.skipped_questions
            ),
        )
