from __future__ import annotations

from hashlib import sha256
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo
from src.config import PASSWORD_SALT


class RegisterModel(BaseModel):
    login: str
    password: str
    email: EmailStr

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, value: str, info: ValidationInfo) -> str:
        string_to_hash = value + info.data["login"] + PASSWORD_SALT
        hashed_value = sha256(string_to_hash.encode()).hexdigest()
        return hashed_value


class LoginModel(BaseModel):
    login: str
    password: str

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, value: str, info: ValidationInfo) -> str:
        string_to_hash = value+info.data["login"]+PASSWORD_SALT
        hashed_value = sha256(string_to_hash.encode()).hexdigest()
        return hashed_value


class UserModel(BaseModel):
    nickname: str
    public_id: int
    secret_id: str = Field(exclude=True)
    email: EmailStr
    description: Optional[str]
    image_path: Optional[str]
