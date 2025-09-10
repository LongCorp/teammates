import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.dao import MessageDAO
from src.database.dao.session_maker import connection
from src.models.models import MessageModel


logger = logging.getLogger(__name__)


@connection()
async def add_message_to_database(
        message: MessageModel,
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
        messages = [MessageModel.model_validate(message, from_attributes=True) for message in messages]
        return messages
    except Exception as e:
        logger.exception("Failed to get chat messages for %s with %s", user_id, peer_id, exc_info=e)
        return []


@connection()
async def mark_read_message(
        user_id: UUID,
        message_id: UUID,
        session: AsyncSession,
):
    logger.info("Marking read message from database")
    try:
        status = await MessageDAO.mark_read_message(
            session=session,
            user_id=user_id,
            message_id=message_id,
        )
        return status
    except Exception as e:
        logger.exception("Failed to mark read message %s for %s", message_id, user_id, exc_info=e)