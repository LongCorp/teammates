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
    content: str = Field(..., max_length=5000)
    sender_id: UUID
    receiver_id: UUID
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    msg_type: str

    # sender: Optional[UserModel]
    # receiver: Optional[UserModel]

    class Config:
        orm_mode = True


class MessageFilter(BaseModel):
    sender_id: UUID
    receiver_id: UUID