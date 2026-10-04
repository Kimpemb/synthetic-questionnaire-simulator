from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QuestionType(str, Enum):
    TEXT = "text"
    INTEGER = "integer"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    DATE = "date"
    TIME = "time"
    SELECT_ONE = "select_one"
    SELECT_MULTIPLE = "select_multiple"


class ValidationErrorType(str, Enum):
    REQUIRED = "required"
    TYPE = "type"
    CHOICE = "choice"
    CONSTRAINT = "constraint"
    CROSS_QUESTION = "cross_question"


class SimulationStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class GenerationStrategy(str, Enum):
    RANDOM = "random"
    DISTRIBUTION = "distribution"
    PERSONA = "persona"
    LLM = "llm"


@dataclass
class Choice:
    value: str
    label: str


@dataclass
class Constraint:
    expression: str
    message: str | None = None


@dataclass
class RelevanceCondition:
    expression: str


@dataclass
class Question:
    name: str
    type: QuestionType
    label: str
    required: bool = False
    choices: list[Choice] = field(default_factory=list)
    relevance: RelevanceCondition | None = None
    constraint: Constraint | None = None


@dataclass
class Form:
    id: str
    title: str
    questions: list[Question]
    version: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Respondent:
    id: str
    demographics: dict[str, Any] = field(default_factory=dict)
    characteristics: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationConfig:
    respondent_count: int
    generation_strategy: GenerationStrategy
    max_generation_attempts: int
    seed: int | None = None
    respondent_profile: str | dict[str, Any] | None = None


@dataclass
class SimulationContext:
    respondent: Respondent
    answers: dict[str, Any] = field(default_factory=dict)
    current_question: Question | None = None
    visited_questions: list[str] = field(default_factory=list)
    skipped_questions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationError:
    question: str
    type: ValidationErrorType
    message: str
    value: Any = None


@dataclass
class ValidationResult:
    valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[ValidationError] = field(default_factory=list)

@dataclass
class SimulationResult:
    respondent_id: str
    answers: dict[str, Any]
    validation: ValidationResult | None = None
    status: SimulationStatus = SimulationStatus.COMPLETED
    visited_questions: list[str] = field(default_factory=list)
    skipped_questions: list[str] = field(default_factory=list)
    logic_trace: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class BatchSimulationResult:
    results: list[SimulationResult]
    status: SimulationStatus
    total_requested: int
    total_completed: int
    total_failed: int
