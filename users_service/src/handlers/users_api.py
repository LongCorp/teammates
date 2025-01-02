import json
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException

from src.entities.entities import DBEntities
from starlette.responses import Response

from src.models.models import UserModel

logger = logging.getLogger(__name__)

app = FastAPI(
    version='1.0.0',
    title='TeamMates users API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


@app.get("/profile",  response_model=UserModel)
async def show_profile(nickname: Optional[str] = None, user_id: Optional[int] = None) -> Response:
    logger.info("Received request for showing %s's profile", nickname or user_id)
    if nickname:
        user_info = await DBEntities.users_db.get_user_by_nickname(nickname)
        if user_info:
            logger.info("%s's profile returned", nickname)
            return user_info

    if user_id:
        user_info = await DBEntities.users_db.get_user_by_public_id(user_id)
        if user_info:
            logger.info("%s's profile returned", user_id)
            return user_info

    logger.error("User %s not found", nickname or user_id)
    raise HTTPException(status_code=404, detail=f"User {nickname or user_id} not found")
