from app.domain.models import BatchSimulationResult, Form
from app.output.base import OutputGenerator


def test_output_generator_is_abstract():
    try:
        OutputGenerator()
        assert False, "Expected TypeError"
    except TypeError:
        pass


def test_output_generator_requires_generate_implementation():
    class TestOutputGenerator(OutputGenerator):
        def generate(
            self,
            form: Form,
            result: BatchSimulationResult,
        ):
            return "output"

    generator = TestOutputGenerator()

    assert generator.generate(
        Form(
            id="test",
            title="Test",
            questions=[],
        ),
        BatchSimulationResult(
            results=[],
            status=None,
            total_requested=0,
            total_completed=0,
            total_failed=0,
        ),
    ) == "output"
