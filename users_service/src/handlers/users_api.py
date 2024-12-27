import json
import logging

from fastapi import FastAPI

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
    logger.info("%s's profile was shown", username)
    return Response(
        status_code=200,
        content=json.dumps({"user": user_info.model_dump()})
    )