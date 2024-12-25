import uuid
from datetime import datetime, timezone

import jwt

from src.config import JWT_SECRET
from src.models.models import UserModel


class RefreshToken:
    def __init__(self, token: str):
        self.__token = token

    def get_secret_id(self):
        payload = jwt.decode(self.__token, JWT_SECRET, algorithms=['HS256'])
        return payload["sub"]

    @staticmethod
    def from_user(user: UserModel, ttl: int):

        current_timestamp = datetime.timestamp((datetime.now(tz=timezone.utc)))

        data = dict(
            iss='LongCorp@auth_service',
            sub=user.secret_id,
            jti=str(uuid.uuid4()),
            iat=current_timestamp,
            nbf=current_timestamp,
            exp=current_timestamp + ttl
        )

        return RefreshToken(jwt.encode(payload=data, key=JWT_SECRET, algorithm='HS256'))

    @staticmethod
    def from_id(secret_id: str, ttl: int):
        current_timestamp = datetime.timestamp((datetime.now(tz=timezone.utc)))

        data = dict(
            iss='LongCorp@auth_service',
            sub=secret_id,
            jti=str(uuid.uuid4()),
            iat=current_timestamp,
            nbf=current_timestamp,
            exp=current_timestamp + ttl
        )

        return RefreshToken(jwt.encode(payload=data, key=JWT_SECRET, algorithm='HS256'))

    def __str__(self):
        return self.__token


class AccessToken:

    def __init__(self, token: str):
        self.__token = token

    def get_secret_key(self):
        payload = jwt.decode(self.__token, JWT_SECRET, algorithms=['HS256'])
        return payload["sub"]

    @staticmethod
    def from_refresh_token(refresh_token: RefreshToken, ttl: int):
        current_timestamp = datetime.timestamp((datetime.now(tz=timezone.utc)))

        secret_id = refresh_token.get_secret_id()

        data = dict(
            iss='LongCorp@auth_service',
            sub=secret_id,
            jti=str(uuid.uuid4()),
            iat=current_timestamp,
            nbf=current_timestamp,
            exp=current_timestamp + ttl
        )

        return AccessToken(jwt.encode(payload=data, key=JWT_SECRET, algorithm='HS256'))

    def __str__(self):
        return self.__token
