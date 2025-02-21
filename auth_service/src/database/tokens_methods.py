import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.session_maker import connection
from src.database.dao.dao import UserRefreshTokenDAO
from src.database.dao.models import UserRefreshToken
from src.entities.tokens import RefreshToken

logger = logging.getLogger(__name__)


@connection()
async def update_refresh_token_for_user(user_id: UUID, refresh_token: RefreshToken, session: AsyncSession) -> bool:
    try:
        logger.info("Updating refresh token for user %s", user_id)

        user_refresh_token = await UserRefreshTokenDAO.find_one_or_none_by_id(user_id, session=session)

        if user_refresh_token:
            user_refresh_token.refresh_token = str(refresh_token)
        else:
            user_refresh_token = UserRefreshToken(user_id=user_id, refresh_token=str(refresh_token))
            session.add(user_refresh_token)
        await session.flush()

        logger.info("Done updating refresh token for user %s", user_id)
    except Exception as e:
        logger.error("Error while updating refresh token for user %s", user_id, exc_info=e)
        return False

    return True


@connection()
async def get_refresh_token_for_user_by_id(user_id: UUID, session: AsyncSession) -> RefreshToken | None:
    try:
        logger.info("Getting refresh token for user %s", user_id)

        user_refresh_token = await UserRefreshTokenDAO.find_one_or_none_by_id(user_id, session=session)
        user_refresh_token = RefreshToken(str(user_refresh_token.refresh_token))

        logger.info("Done getting refresh token for user %s", user_id)

        return user_refresh_token
    except Exception as e:
        logger.error("Can't get refresh token for user %s", user_id, exc_info=e)
        return None
