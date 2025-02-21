from __future__ import annotations

from hashlib import sha256
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo
from src.config import PASSWORD_SALT


class RegisterModel(BaseModel):
    nickname: str
    password: str
    email: EmailStr

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, value: str, info: ValidationInfo) -> str:
        string_to_hash = value + info.data["nickname"] + PASSWORD_SALT
        hashed_value = sha256(string_to_hash.encode()).hexdigest()
        return hashed_value


class LoginModel(BaseModel):
    nickname: str
    password: str

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, value: str, info: ValidationInfo) -> str:
        string_to_hash = value+info.data["nickname"]+PASSWORD_SALT
        hashed_value = sha256(string_to_hash.encode()).hexdigest()
        return hashed_value


class UserModel(BaseModel):
    nickname: str
    public_id: str
    auth_id: str = Field(exclude=True)
    email: EmailStr
    description: Optional[str] = None
    image_path: Optional[str] = None

    @field_validator('public_id', 'auth_id', mode='before')
    @classmethod
    def validate_public_id(cls, value: UUID) -> str:
        return str(value)


class UpdateTokensModel(BaseModel):
    public_id: str
    refresh_token: str
