from __future__ import annotations

import json
import logging
from http import HTTPStatus
from fastapi import HTTPException

from fastapi import FastAPI, Response
from jwt import DecodeError

from src.entities.tokens import AccessToken
from src.models.models import LoginModel, UserModel
from src.entities.entities import DBEntities

logger = logging.getLogger(__name__)
app = FastAPI(
    version='1.0.0',
    title='TeamMates auth API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


@app.post("/login", response_model=UserModel)
async def login(login_info: LoginModel):

    logger.info("Received login request with login: %s", login_info.login)

    password_from_db = await DBEntities.users_db.get_password_hash_by_nickname(
        login_info.login
    )
    if password_from_db == login_info.password:
        user = await DBEntities.users_db.get_user_by_nickname(login_info.login)
        token = AccessToken.create_token(user, 3600)

        logger.info("User with login  %s successfully authenticated", login_info.login)

        return Response(
            status_code=HTTPStatus.OK,
            content=json.dumps({"user": user.model_dump()}),
            headers={"Authorization": f"Bearer {token}"}
        )
    logger.error("Authentication failed for user with login: %s", login_info.login)
    raise HTTPException(401, "Not authenticated")


@app.post("/register")
async def register():
    pass


@app.get("/get_id_by_token")
async def get_id_by_token(token: str):
    try:
        logger.info("Received request to get ID by token: %s", token)
        token = AccessToken(token)
        secret_key = token.get_secret_key()
        logger.info("ID by token successfully received")
    except DecodeError:
        logger.error("Error getting ID by token")
        secret_key = None
    return secret_key
