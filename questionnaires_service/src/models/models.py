from __future__ import annotations

import json
from enum import Enum
from typing import Optional, Iterable
from uuid import UUID

from pydantic import BaseModel, Field, model_validator
from fastapi import UploadFile, Form


class Game(Enum):
    CS2 = 'CS2'
    Dota_2 = 'Dota 2'
    GTA_5 = 'GTA 5'
    Volorant = 'Volorant'


class QuestionnaireIn(BaseModel):
    header: str = Field(example='Wanna find teammate Dota 2')
    game: Game
    description: str
    author_id: int

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class QuestionnaireOut(QuestionnaireIn):
    questionnaire_id: UUID
    photo_path: str
