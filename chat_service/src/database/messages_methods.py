import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import session

from src.database.dao.dao import MessageDAO
from src.database.dao.session_maker import connection
from src.models.models import NewMessageModel, DeletedMessageModel, UpdatedMessageModel, ReadMessageModel

logger = logging.getLogger(__name__)


@connection()
async def add_message_to_database(
        message: NewMessageModel,
        session: AsyncSession,
):
    logger.info("Adding message to database")
    try:
        await MessageDAO.add(
            session=session,
            values=message
        )
        return True
    except Exception as e:
        logger.exception("Failed to add message to database", exc_info=e)
        return False


@connection()
async def get_chat_messages(
        user_id: UUID,
        peer_id: UUID,
        session: AsyncSession,
        before: Optional[datetime] = None,
        limit: int = Query(20, ge=1, le=100)
):
    logger.info("Getting chat messages from database")
    try:
        messages = await MessageDAO.get_messages(
            session=session,
            user_id=user_id,
            before=before,
            limit=limit,
            peer_id=peer_id,
        )
        logger.info(messages)
        messages = [NewMessageModel.model_validate(message, from_attributes=True) for message in messages]
        return messages
    except Exception as e:
        logger.exception("Failed to get chat messages for %s with %s", user_id, peer_id, exc_info=e)
        return []


@connection()
async def update_read_message(
        message: ReadMessageModel,
        session: AsyncSession,
):
    logger.info("Marking read message from database")
    try:
        status = await MessageDAO.mark_read_message(
            session=session,
            user_id=message.receiver_id,
            message_id=message.message_id,
        )
        return status
    except Exception as e:
        logger.exception("Failed to mark read message %s for %s", message.message_id, message.receiver_id, exc_info=e)


@connection()
async def update_edited_message(
        message: UpdatedMessageModel,
        session: AsyncSession,
):
    logger.info("Marking update message from database")
    try:

        status = await MessageDAO.update_message(
            session=session,
            user_id=message.sender_id,
            message_id=message.message_id,
            new_value=message.content
        )
        return status
    except Exception as e:
        logger.exception("Failed to mark update message %s for %s", message.message_id, message.sender_id, exc_info=e)
        return False


@connection()
async def delete_message(
        deleted_message: DeletedMessageModel,
        session: AsyncSession
):
    logger.info("Deleting message from database")
    try:
        status = await MessageDAO.delete_message(
            session=session,
            message_id=deleted_message.message_id,
            receiver_id=deleted_message.receiver_id,
            sender_id=deleted_message.sender_id,
        )
        return status
    except Exception as e:
        logger.exception("Failed to delete message from %s", deleted_message.message_id, exc_info=e)
        return False