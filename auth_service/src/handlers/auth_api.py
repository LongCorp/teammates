from __future__ import annotations

import json
import logging
from uuid import UUID

from fastapi import HTTPException

from fastapi import FastAPI, Response
from jwt import DecodeError, ExpiredSignatureError

from src.database import users_methods, tokens_methods
from src.entities.tokens import AccessToken, RefreshToken
from src.models.models import LoginModel, RegisterModel, UpdateTokensModel

logger = logging.getLogger(__name__)
app = FastAPI(
    version='1.0.0',
    title='TeamMates auth API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


@app.post("/login")
async def login(login_info: LoginModel):

    logger.info("Received login request with login: %s", login_info.nickname)

    password_from_db = await users_methods.get_password_hash_by_nickname(
        login_info.nickname
    )

    if password_from_db == login_info.password:
        user = await users_methods.get_user_by_nickname(login_info.nickname)

        refresh_token = RefreshToken.from_user(user, 86400)
        access_token = AccessToken.from_refresh_token(refresh_token, 3600)

        added = await tokens_methods.update_refresh_token_for_user(UUID(user.public_id), refresh_token)

        if added:
            logger.info("User with login %s successfully authenticated", login_info.nickname)

            return Response(
                status_code=201,
                content=json.dumps({
                    "user": user.model_dump(),
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                })
            )
    logger.error("Authentication failed for user with login: %s", login_info.nickname)
    raise HTTPException(401, "Not authenticated")


@app.post("/register")
async def register(register_data: RegisterModel):
    logger.info("Received register request with register: %s %s", register_data.nickname, register_data.email)

    registered_user = await users_methods.create_user(register_data)

    if registered_user:
        refresh_token = RefreshToken.from_user(registered_user, 86400)
        access_token = AccessToken.from_refresh_token(refresh_token, 3600)

        added = await tokens_methods.update_refresh_token_for_user(UUID(registered_user.public_id), refresh_token)

        if added:
            logger.info("User %s successfully registered", register_data.nickname)
            return Response(
                status_code=201,
                content=json.dumps({
                    "user": registered_user.model_dump(),
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token)
                })
            )

    logger.error("Registration failed for user with register: %s %s", register_data.nickname, register_data.email)
    raise HTTPException(500, "Server error")


@app.get("/get_id_by_token", include_in_schema=False)
async def get_id_by_token(token: str):
    try:
        logger.info("Received request to get ID by token: %s", token)
        token = AccessToken(token)
        secret_key = token.get_auth_id()
        logger.info("ID by token successfully received")
    except (DecodeError, ExpiredSignatureError, TypeError):
        logger.error("Error getting ID by token --- invalid token")
        secret_key = None
    return secret_key


@app.post("/update_tokens")
async def update_tokens(tokens_input: UpdateTokensModel):
    logger.info("Received request to update tokens")
    try:
        current_refresh_token = await tokens_methods.get_refresh_token_for_user_by_id(UUID(tokens_input.public_id))
        refresh_token = RefreshToken(tokens_input.refresh_token)
        if current_refresh_token == refresh_token:
            auth_id = refresh_token.get_auth_id()
            new_refresh_token = RefreshToken.from_auth_id(auth_id, 86400)
            new_access_token = AccessToken.from_refresh_token(new_refresh_token, 3600)

            added = await tokens_methods.update_refresh_token_for_user(UUID(tokens_input.public_id), new_refresh_token)
            if added:
                logger.info("Updated tokens for user %s", tokens_input.public_id)
                return Response(
                    status_code=201,
                    content=json.dumps({
                        "refresh_token": str(new_refresh_token),
                        "access_token": str(new_access_token),
                    })
                )
        raise ValueError
    except (KeyError, DecodeError, ExpiredSignatureError, TypeError, ValueError):
        logger.info("Wrong refresh token received")
        raise HTTPException(401, "Not authenticated")
    except Exception as e:
        logger.error("Error while updating tokens", exc_info=e)
        raise HTTPException(500, "Server error")
