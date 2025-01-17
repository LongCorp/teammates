from enum import Enum
from typing import Optional, Annotated
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    nickname: str
    public_id: int
    secret_id: str = Field(exclude=True)
    email: Annotated[EmailStr, Field(exclude=True)]
    description: Optional[str]
    image_path: Optional[str]


class UserLikeModel(BaseModel):
    liker_id: int
    liked_id: int


class QuestionnaireLikeModel(BaseModel):
    liker_id: int
    questionnaire_id: UUID

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

class QuestionnaireOut(QuestionnaireIn):
    questionnaire_id: UUID
    photo_path: str