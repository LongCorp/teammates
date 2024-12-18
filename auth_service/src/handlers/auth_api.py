from __future__ import annotations

from fastapi import FastAPI
from jwt import DecodeError

from auth_service.src.entities.tokens import AccessToken
from auth_service.src.models.models import LoginModel
from auth_service.src.entities.entities import DBEntities

app = FastAPI(
    version='1.0.0',
    title='TeamMates auth API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


@app.post("/login")
async def login(login_info: LoginModel):
    user = await DBEntities.users_db.get_user(login_info.login)
    token = AccessToken.create_token(user, 3600)
    return {"token": token}


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
