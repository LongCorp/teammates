import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.dao import UserDAO
from src.database.dao.session_maker import connection

logger = logging.getLogger(__name__)


@connection()
async def get_public_id(auth_id: UUID, session: AsyncSession) -> UUID | None:
    logger.info("Getting public id for %s", auth_id)

    try:
        auth_id = await UserDAO.get_public_id_by_auth_id(auth_id, session=session)
    except Exception as e:
        logger.error("Can't get public_id for user with secret_id %s", auth_id, exc_info=e)
        return None

    if auth_id:
        logger.info("Done getting public id for user %s", auth_id)
        return auth_id

    return None
