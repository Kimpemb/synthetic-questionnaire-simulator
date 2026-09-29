from app.simulation.respondent import RespondentGenerator


def test_generator_returns_respondent():
    generator = RespondentGenerator()

    respondent = generator.generate()

    assert respondent.id
    assert respondent.demographics == {}
    assert respondent.characteristics == {}
    assert respondent.preferences == {}
    assert respondent.attributes == {}


def test_generator_creates_unique_ids():
    generator = RespondentGenerator()

    first = generator.generate()
    second = generator.generate()

    assert first.id != second.id


def test_generator_is_reproducible_with_seed():
    first_generator = RespondentGenerator(seed=42)
    second_generator = RespondentGenerator(seed=42)

    first = first_generator.generate()
    second = second_generator.generate()

    assert first.id == second.id

def test_generator_accepts_profile():
    generator = RespondentGenerator()

    respondent = generator.generate(
        profile={
            "demographics": {
                "age": 21,
                "sex": "male",
            }
        }
    )

    assert respondent.demographics["age"] == 21
    assert respondent.demographics["sex"] == "male"

def test_generator_does_not_mutate_profile():
    generator = RespondentGenerator()

    profile = {
        "demographics": {
            "age": 21,
        }
    }

    respondent = generator.generate(profile)

    respondent.demographics["age"] = 30

    assert profile["demographics"]["age"] == 21