import logging
from uuid import UUID

import sqlalchemy.exc
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.dao import UserDAO
from src.database.dao.session_maker import connection
from src.models.models import UserModel, RegisterModel

logger = logging.getLogger(__name__)


@connection()
async def get_public_id(auth_id: UUID, session: AsyncSession) -> UUID | None:
    logger.info("Getting public id for %s", auth_id)

    try:
        user = await UserDAO.find_one_or_none_by_id(auth_id, session=session)
    except Exception as e:
        logger.error("Can't get public_id for user with secret_id %s", auth_id, exc_info=e)
        return None

    if user:
        logger.info("Done getting public id for user %s", auth_id)
        return user.id

    return None


@connection()
async def get_password_hash_by_nickname(nickname: str, session: AsyncSession) -> str | None:
    logger.info("Getting password hash for user %s", nickname)

    try:
        password = await UserDAO.get_password_hash_by_nickname(nickname=nickname, session=session)

        return password
    except Exception as e:
        logger.error("Can't get password hash for user %s", nickname, exc_info=e)
        return None


@connection()
async def get_user_by_nickname(nickname: str, session: AsyncSession) -> UserModel | None:
    logger.info("Getting user by nickname for user %s", nickname)
    try:
        user = await UserDAO.get_user_by_nickname(nickname=nickname, session=session)
        pydantic_user = UserModel(
            nickname=user.nickname,
            public_id=user.id,
            auth_id=user.auth_id,
            email=user.email,
            description=user.description,
            image_path=user.image_path
        )
        logger.info("Done getting user by nickname for user %s", nickname)

        return pydantic_user
    except Exception as e:
        logger.error("Can't get user by nickname for user %s", nickname, exc_info=e)
        return None


@connection()
async def create_user(register_data: RegisterModel, session: AsyncSession) -> UserModel | None:
    logger.info("Started creating new user %s", register_data.nickname)
    try:
        user = await UserDAO.add(session=session, values=register_data)
        pydantic_user = UserModel(
            nickname=user.nickname,
            public_id=user.id,
            auth_id=user.auth_id,
            email=user.email,
            description=user.description,
            image_path=user.image_path
        )
        logger.info("Done creating new user %s", register_data.nickname)

        return pydantic_user
    except sqlalchemy.exc.IntegrityError as e:
        logger.warning("Can`t create user %s: %s", register_data.nickname, e.orig)
        raise HTTPException(status_code=400)
    except Exception as e:
        logger.error("Error while creating new user %s", register_data.nickname, exc_info=e)
        return None
