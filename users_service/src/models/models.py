from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    nickname: str
    public_id: int
    secret_id: str = Field(exclude=True)
    email: EmailStr
    description: Optional[str]
    image_path: Optional[str]