from __future__ import annotations

from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Game(Enum):
    CS2 = 'CS2'
    Dota_2 = 'Dota 2'
    GTA_5 = 'GTA 5'
    Volorant = 'Volorant'


class QuestionnaireIn(BaseModel):
    name: str = Field(example='Wanna find teammate Dota 2')
    game: Game
    text: str
    image: Optional[bytes] = None
    author_id: int


class QuestionnaireOut(QuestionnaireIn):
    id: UUID
