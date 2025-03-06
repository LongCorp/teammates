from typing import Optional, Annotated
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from src.models.enums import GameEnum


class UserModel(BaseModel):
    nickname: str
    id: UUID
    auth_id: UUID = Field(exclude=True)
    email: Annotated[EmailStr, Field(exclude=True)]
    description: Optional[str]
    image_path: Optional[str]

class UserUpdateModel(BaseModel):
    nickname: str
    id: UUID
    description: str


class UserLikeModel(BaseModel):
    liked_by_id: UUID
    liked_id: UUID


class QuestionnaireLikeModel(BaseModel):
    liker_id: UUID
    questionnaire_id: UUID


class QuestionnaireIn(BaseModel):
    header: str = Field(example="Wanna find teammate Dota 2")
    game: GameEnum
    description: str
    author_id: UUID


class QuestionnaireOut(QuestionnaireIn):
    id: UUID
    image_path: str
