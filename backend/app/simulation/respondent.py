import random
import uuid
from copy import deepcopy

from app.domain.models import Respondent


class RespondentGenerator:
    def __init__(self, seed: int | None = None):
        self._random = random.Random(seed)

    def generate(
        self,
        profile: dict | None = None,
    ) -> Respondent:
        respondent_id = str(
            uuid.UUID(
                int=self._random.getrandbits(128)
            )
        )

        profile = profile or {}

        return Respondent(
            id=respondent_id,
            demographics=deepcopy(
                profile.get("demographics", {})
            ),
            characteristics=deepcopy(
                profile.get("characteristics", {})
            ),
            preferences=deepcopy(
                profile.get("preferences", {})
            ),
            attributes=deepcopy(
                profile.get("attributes", {})
            ),
        )