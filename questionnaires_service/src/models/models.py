from __future__ import annotations

import json
from uuid import UUID

from pydantic import BaseModel, Field, model_validator, ConfigDict
from teammates_db.enums import GameEnum


class QuestionnaireIn(BaseModel):
    header: str = Field(example='Wanna find teammate Dota 2')
    game: GameEnum
    description: str
    author_id: UUID

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class QuestionnaireOut(QuestionnaireIn):
    id: UUID
    image_path: str

    model_config = ConfigDict(from_attributes=True)
