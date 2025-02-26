from enum import Enum
from typing import Optional, Annotated
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    nickname: str
    id: UUID
    auth_id: UUID = Field(exclude=True)
    email: Annotated[EmailStr, Field(exclude=True)]
    description: Optional[str]
    image_path: Optional[str]


class UserLikeModel(BaseModel):
    liked_by_id: UUID
    liked_id: UUID


class QuestionnaireLikeModel(BaseModel):
    liker_id: UUID
    questionnaire_id: UUID

class Game(Enum):
    CS2 = 'CS2'
    Dota_2 = 'Dota 2'
    GTA_5 = 'GTA 5'
    Volorant = 'Volorant'

class QuestionnaireIn(BaseModel):
    header: str = Field(example="Wanna find teammate Dota 2")
    game: Game
    description: str
    author_id: UUID

class QuestionnaireOut(QuestionnaireIn):
    id: UUID
    image_path: str