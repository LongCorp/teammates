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


class NewMessageModel(BaseModel):
    content: str = Field(...,min_length=1, max_length=5000)
    sender_id: UUID
    receiver_id: UUID
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    msg_type: str = "new_message"

    # sender: Optional[UserModel]
    # receiver: Optional[UserModel]

    class Config:
        orm_mode = True


class MessageFilter(BaseModel):
    sender_id: UUID
    receiver_id: UUID


class UpdatedMessageModel(BaseModel):
    content: str = Field(...,min_length=1, max_length=5000)
    updated_at: datetime = Field(default_factory=datetime.now)
    sender_id: UUID
    receiver_id: UUID
    message_id: UUID
    msg_type: str = "message_edited"


class ReadMessageModel(BaseModel):
    message_id: UUID
    msg_type: str = "message_read"
    receiver_id: UUID
    sender_id: UUID

class DeletedMessageModel(BaseModel):
    message_id: UUID
    msg_type: str = "message_deleted"
    receiver_id: UUID
    sender_id: UUID


class ErrorModel(BaseModel):
    data: dict
    error_msg: str