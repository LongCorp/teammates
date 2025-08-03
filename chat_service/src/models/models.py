from datetime import datetime
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


class MessageModel(BaseModel):
    id: int
    content: str = Field(..., max_length=5000)
    sender_id: int
    receiver_id: int
    is_read: bool
    created_at: datetime
    updated_at: datetime

    sender: Optional[UserModel]
    receiver: Optional[UserModel]

    class Config:
        orm_mode = True