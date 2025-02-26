import json
import logging
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, APIRouter

from src.database import users_methods
from src.models.models import UserModel

logger = logging.getLogger(__name__)


users_router = APIRouter()


@users_router.get("/profile",  response_model=UserModel)
async def show_profile(user_id: UUID, nickname: Optional[str] = None, public_id: Optional[UUID] = None) -> UserModel:
    logger.info("Received request for showing %s's profile", nickname or user_id)
    if nickname:
        user_info = await users_methods.get_user_by_nickname(nickname)
        if user_info:
            logger.info("%s's profile returned", nickname)
            return user_info

    if public_id:
        user_info = await users_methods.get_user_by_public_id(public_id=public_id)
        print(user_info)
        if user_info:
            logger.info("%s's profile returned", public_id)
            return user_info

    logger.error("User %s not found", nickname or public_id)
    raise HTTPException(status_code=404, detail=f"User {nickname or public_id} not found")
