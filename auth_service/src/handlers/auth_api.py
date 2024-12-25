from __future__ import annotations

import json
import logging
from http import HTTPStatus
from fastapi import HTTPException

from fastapi import FastAPI, Response
from jwt import DecodeError

from src.entities.tokens import AccessToken, RefreshToken
from src.models.models import LoginModel, UserModel, RegisterModel
from src.entities.entities import DBEntities

logger = logging.getLogger(__name__)
app = FastAPI(
    version='1.0.0',
    title='TeamMates auth API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


@app.post("/login")
async def login(login_info: LoginModel):

    logger.info("Received login request with login: %s", login_info.login)

    password_from_db = await DBEntities.users_db.get_password_hash_by_nickname(
        login_info.login
    )

    if password_from_db == login_info.password:
        user = await DBEntities.users_db.get_user_by_nickname(login_info.login)

        refresh_token = RefreshToken.from_user(user, 86400)
        access_token = AccessToken.from_refresh_token(refresh_token, 3600)
        logger.info("User with login %s successfully authenticated", login_info.login)

        return Response(
            status_code=201,
            content=json.dumps({
                "user": user.model_dump(),
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            })
        )
    logger.error("Authentication failed for user with login: %s", login_info.login)
    raise HTTPException(401, "Not authenticated")


@app.post("/register")
async def register(register_data: RegisterModel):
    logger.info("Received register request with register: %s %s", register_data.login, register_data.email)

    registered_user = await DBEntities.users_db.create_user(register_data)

    if registered_user:
        refresh_token = RefreshToken.from_user(registered_user, 86400)
        access_token = AccessToken.from_refresh_token(refresh_token, 3600)

        logger.info("User %s successfully registered", register_data.login)
        return Response(
            status_code=201,
            content=json.dumps({
                "user": registered_user.model_dump(),
                "access_token": str(access_token),
                "refresh_token": str(refresh_token)
            })
        )

    logger.error("Registration failed for user with register: %s %s", register_data.login, register_data.email)
    raise HTTPException(500, "Server error")


@app.get("/get_id_by_token", include_in_schema=False)
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


@app.post("/update_tokens")
async def update_tokens(tokens: dict):
    pass