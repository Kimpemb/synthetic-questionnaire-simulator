from app.domain.models import (
    Form,
    GenerationStrategy,
    Question,
    QuestionType,
    Respondent,
    SimulationConfig,
)


def test_question_model():
    question = Question(
        name="age",
        type=QuestionType.INTEGER,
        label="How old are you?",
        required=True,
    )

    assert question.name == "age"
    assert question.type == QuestionType.INTEGER
    assert question.required is True
    assert question.choices == []


def test_form_model():
    question = Question(
        name="age",
        type=QuestionType.INTEGER,
        label="How old are you?",
    )

    form = Form(
        id="test_form",
        title="Test Questionnaire",
        questions=[question],
    )

    assert form.id == "test_form"
    assert len(form.questions) == 1
    assert form.questions[0].name == "age"


def test_respondent_model():
    respondent = Respondent(
        id="respondent_001",
        demographics={"age": 22},
    )

    assert respondent.id == "respondent_001"
    assert respondent.demographics["age"] == 22
    assert respondent.characteristics == {}


def test_simulation_config():
    config = SimulationConfig(
        respondent_count=100,
        generation_strategy=GenerationStrategy.RANDOM,
        max_generation_attempts=5,
        seed=42,
    )

    assert config.respondent_count == 100
    assert config.generation_strategy == GenerationStrategy.RANDOM
    assert config.seed == 42