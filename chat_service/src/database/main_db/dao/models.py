import uuid
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import Uuid, func, String, CHAR, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'users'

    auth_id: Mapped[UUID] = mapped_column(Uuid, default=uuid.uuid4())
    nickname: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(CHAR(64))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    questionnaires: Mapped[List["Questionnaire"]] = relationship(
        "Questionnaire",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    refresh_token: Mapped["UserRefreshToken"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )