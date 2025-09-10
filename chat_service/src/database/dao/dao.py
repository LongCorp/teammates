from datetime import datetime
from typing import TypeVar, Generic, Optional
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel
from sqlalchemy import select, or_, desc, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.database.dao.models import Base, User, Message  # , Message

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: UUID, session: AsyncSession):
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None):
        if filters:
            filter_dict = filters.model_dump(exclude_none=True, exclude_unset=True)
        else:
            filter_dict = {}
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def delete_one_by_id(cls, data_id: UUID, session: AsyncSession):
        try:
            data = await session.get(cls.model, data_id)
            if data:
                await session.delete(data)
                await session.flush()

            return True
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_public_id_by_auth_id(cls, auth_id: UUID, session: AsyncSession) -> UUID:
        try:
            query = sa.select(cls.model.id).where(cls.model.auth_id == auth_id)

            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise e


class MessageDAO(BaseDAO[Message]):
    model = Message

    @classmethod
    async def get_messages(
            cls,
            user_id: UUID,
            peer_id: UUID,
            before: Optional[datetime] = None,
            limit: int = Query(20, ge=1, le=100),
            session: AsyncSession = None
    ):
        try:
            query = (
                select(Message)
                .where(
                    or_(
                        (Message.sender_id == user_id) & (Message.receiver_id == peer_id),
                        (Message.sender_id == peer_id) & (Message.receiver_id == user_id),
                    )
                )
            )
            if before:
                query = query.where(Message.created_at < before)

            query = query.order_by(desc(Message.created_at)).limit(limit)

            result = await session.execute(query)
            messages = result.scalars().all()

            return messages
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def mark_read_message(cls, session, user_id, message_id):
        try:
            query = (
                update(Message)
                .where(Message.id == message_id)
                .where(Message.receiver_id == user_id)
                .values(is_read=True)
                .execution_options(synchronize_session="fetch")
            )

            result = await session.execute(query)

            return result.rowcount
        except SQLAlchemyError as e:
            raise e
