from abc import ABC, abstractmethod

from app.domain.models import Question


class AnswerGenerator(ABC):
    @abstractmethod
    def generate(self, question: Question):
        pass