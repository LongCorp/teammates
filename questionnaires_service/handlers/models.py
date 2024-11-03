from __future__ import annotations

from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import AnyUrl, BaseModel, EmailStr, Field


class UserOut(BaseModel):
    name: str = Field(..., example='ProGamer228')
    id: UUID
    description: Optional[str] = Field(None, example='Some words about author')
    icon: Optional[AnyUrl] = None


class UserIn(BaseModel):
    name: str = Field(..., example='ProGamer228')
    email: EmailStr
    description: Optional[str] = Field(None, example='Some words about author')
    icon: Optional[bytes] = None


class Game(Enum):
    CS2 = 'CS2'
    Dota_2 = 'Dota 2'
    GTA_5 = 'GTA 5'
    Volorant = 'Volorant'


class QuestionnaireOut(BaseModel):
    name: str = Field(..., example='Wanna find teammate Dota 2')
    id: UUID
    game: Game
    text: str
    image: Optional[AnyUrl] = Field(None, description='Image URL')
    author_id: UUID


class QuestionnaireIn(BaseModel):
    name: str = Field(..., example='Wanna find teammate Dota 2')
    game: Game
    text: str
    image: Optional[bytes] = None
    author_id: UUID
