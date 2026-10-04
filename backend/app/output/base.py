from abc import ABC, abstractmethod
from typing import Any

from app.domain.models import BatchSimulationResult, Form


class OutputGenerator(ABC):
    @abstractmethod
    def generate(
        self,
        form: Form,
        result: BatchSimulationResult,
    ) -> Any:
        pass
