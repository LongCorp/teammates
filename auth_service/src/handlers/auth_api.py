from __future__ import annotations

import json
from http import HTTPStatus
from http.client import HTTPException

from fastapi import FastAPI, Response
from jwt import DecodeError

from src.entities.tokens import AccessToken
from src.models.models import LoginModel, UserModel
from src.entities.entities import DBEntities

app = FastAPI(
    version='1.0.0',
    title='TeamMates auth API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


@app.post("/login", response_model=UserModel)
async def login(login_info: LoginModel):
    password_from_db = await DBEntities.users_db.get_password_hash_by_nickname(
        login_info.login
    )
    if password_from_db == login_info.password:
        user = await DBEntities.users_db.get_user_by_nickname(login_info.login)
        token = AccessToken.create_token(user, 3600)
        return Response(
            status_code=HTTPStatus.OK,
            content=json.dumps({"user": user.model_dump()}),
            headers={"Authorization": f"Bearer {token}"}
        )
    raise HTTPException(401, "Not authenticated")


@app.post("/register")
async def register():
    pass


@app.get("/get_id_by_token")
async def get_id_by_token(token: str):
    try:
        token = AccessToken(token)
        secret_key = token.get_secret_key()
    except DecodeError:
        secret_key = None
    return secret_key
