import uuid
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import String, ForeignKey, Uuid, Text, CHAR, func
from sqlalchemy.ext.asyncio import AsyncAttrs

from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from enums import GameEnum


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class Questionnaire(Base):
    __tablename__ = 'questionnaires'

    author_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    header: Mapped[str | None] = mapped_column(String(63))
    description: Mapped[str] = mapped_column(Text)
    image_path: Mapped[str | None] = mapped_column(String(255))
    game: Mapped[GameEnum]

    author: Mapped["User"] = relationship(
        "User",
        back_populates="questionnaires",
        lazy="joined"
    )


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


class UserRefreshToken(Base):
    __tablename__ = 'users_refresh_tokens'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    refresh_token: Mapped[str] = mapped_column(String(500), unique=True)

    user: Mapped["User"] = relationship(
        back_populates="refresh_token",
        uselist=False
    )


class LikedQuestionnaire(Base):
    __tablename__ = 'liked_questionnaires'

    liker_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    questionnaire_id: Mapped[str] = mapped_column(ForeignKey("questionnaires.id"))

    questionnaire: Mapped["Questionnaire"] = relationship(
        "Questionnaire",
    )


class LikedUser(Base):
    __tablename__ = 'liked_users'

    liked_by_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    liked_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    sender_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    receiver_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    is_read: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_changed: Mapped[bool] = mapped_column(default=False, nullable=False)

    sender: Mapped["User"] = relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_messages"
    )

    receiver: Mapped["User"] = relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_messages"
    )