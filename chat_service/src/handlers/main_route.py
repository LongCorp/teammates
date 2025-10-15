import logging
from uuid import UUID

from fastapi import FastAPI, Request, Response
import aiohttp
from fastapi.security.http import HTTPBearer
from starlette import status

from src.config import auth_service_url
from src.database import users_methods

logger = logging.getLogger(__name__)

auth_scheme = HTTPBearer(auto_error=True)
app = FastAPI(
    version='1.0.0',
    title='TeamMates chat API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'}
)


async def authenticate_user(token: str) -> UUID | None:
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.request(
                "get", f"{auth_service_url}/get_id_by_token",
                params={"token": token}
            )
            user_secret_id = await response.json()
            if user_secret_id is None:
                return None
        return UUID(user_secret_id)
    except ConnectionError as e:
        logger.error("Error while response from auth service", exc_info=e)


@app.middleware('http')
async def auth_middleware(request: Request, call_next):
    try:
        if ("/docs" in request.url.path or "/openapi.json" in request.url.path
                in request.url.path or "/favicon.ico" in request.url.path):
            return await call_next(request)

        token = request.headers["Authorization"].split(" ")[1]
        secret_id = await authenticate_user(token)
        current_user_id = await users_methods.get_public_id(secret_id)

        user_public_id = UUID(request.query_params["user_id"])
        if user_public_id == current_user_id:
            return await call_next(request)
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    except (KeyError, ValueError):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)