from app.domain.models import (
    Form,
    Respondent,
    SimulationResult,
    SimulationStatus,
    SimulationContext,
)
from app.generation.base import AnswerGenerator
from app.logic.engine import LogicEngine
 


class SimulationEngine:
    def __init__(
        self,
        answer_generator: AnswerGenerator,
        logic_engine: LogicEngine | None = None,
    ):
        self._answer_generator = answer_generator
        self._logic_engine = logic_engine or LogicEngine()

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

            answer = self._answer_generator.generate(
                question
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
            visited_questions=context.visited_questions,
            skipped_questions=context.skipped_questions,
        )