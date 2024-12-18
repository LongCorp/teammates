from __future__ import annotations

from pydantic import BaseModel, EmailStr


class RegisterModel(BaseModel):
    pass


class LoginModel(BaseModel):
    login: str
    password: str


class UserModel(BaseModel):
    nickname: str
    public_id: int
    secret_id: str
    email: EmailStr
    description: str
    image_path: str

