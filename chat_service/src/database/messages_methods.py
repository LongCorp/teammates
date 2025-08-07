import logging
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.dao import MessageDAO
from src.database.dao.session_maker import connection
from src.models.models import MessageModel, MessageFilter

logger = logging.getLogger(__name__)


@connection()
async def get_all_chat_messages(
        user_id: UUID,
        interlocutor_id: UUID,
        session: AsyncSession,
) -> List[MessageModel]:
    logger.info("Getting chat messages for user %s with interlocutor %d", user_id, interlocutor_id)
    try:
        chat_messages_list = []
        filter1 = MessageFilter(sender_id=interlocutor_id, receiver_id=user_id)
        filter2 = MessageFilter(receiver_id=interlocutor_id, sender_id=user_id)
        messages1 =  await MessageDAO.find_all(
            session=session,
            filters=filter1,
        )
        messages2 = await MessageDAO.find_all(
            session=session,
            filters=filter2,
        )
        chat_messages_list.extend(map(lambda x: MessageModel.model_validate(x), messages1))
        chat_messages_list.extend(map(lambda x: MessageModel.model_validate(x), messages2))
        chat_messages_list.sort(key=lambda x: x.created_at)
        return chat_messages_list
    except Exception as e:
        logger.exception("Failed to get chat messages for user %s with interlocutor %d:", user_id, exc_info=e)
        return []