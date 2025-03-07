import json
import logging
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, APIRouter, UploadFile
from starlette.requests import Request

from src.database import users_methods
from src.models.models import UserModel, UserUpdateModel

logger = logging.getLogger(__name__)


users_router = APIRouter(prefix="/users")


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


@users_router.put("/update", response_model=UserModel)
async def update_profile(
        user_id: UUID,
        user_model: UserUpdateModel
) -> UserModel:
    logger.info("Received request for updating %s profile", user_model.id)
    if user_id == user_model.id:
        updated_profile = await users_methods.update_profile_info(
            user_id=user_id,
            user=user_model
        )
        logger.info("%s profile updated", user_model.id)
        return updated_profile

    raise HTTPException(400, "id in user_model and user_id must be the same")

@users_router.put("/update/photo")
async def update_profile_photo(
        user_id: UUID,
        image: UploadFile,
        request: Request
):
    logger.info("Received request for updating %s profile photo", user_id)
    image_path = await users_methods.update_profile_photo(
        user_id=user_id,
        image=image,
        request_url=str(request.url)
    )
    return {
        "user_id": user_id,
        "image_path": image_path
    }
