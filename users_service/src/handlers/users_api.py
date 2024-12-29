import json
import logging

from fastapi import FastAPI, HTTPException

from src.entities.entities import DBEntities
from starlette.responses import Response

logger = logging.getLogger(__name__)

app = FastAPI(
    version='1.0.0',
    title='TeamMates users API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


@app.get("/profile/{username}")
async def show_profile(username: str) -> Response:
    logger.info("Received request for showing %s's profile", username)
    user_info = await DBEntities.users_db.get_user_by_nickname(username)
    if user_info:
        logger.info("%s's profile was shown", username)
        return Response(
            status_code=200,
            content=json.dumps({"user": user_info.model_dump(exclude={"email"})})
        )
    logger.error("User %s not found", username)
    raise HTTPException(status_code=404, detail=f"User {username} not found")

@app.get("/profile/id/{user_id}")
async def show_profile_by_id(user_id: int) -> Response:
    logger.info("Received request for showing profile by ID %s", user_id)
    user_info = await DBEntities.users_db.get_user_by_public_id(user_id)
    if user_info:
        logger.info("Profile with ID %s was shown", user_id)
        return Response(
            status_code=200,
            content=json.dumps({"user": user_info.model_dump(exclude={"email"})})
        )
    logger.error("User with ID %s not found", user_id)
    raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")