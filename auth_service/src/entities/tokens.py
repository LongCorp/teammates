import uuid
from datetime import datetime, timezone

import jwt

from src.config import JWT_SECRET
from src.models.models import UserModel


class RefreshToken:
    def __init__(self, token: str):
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        if payload["type"] == "refresh":
            self.__token = token
        else:
            raise TypeError("Token type must be 'refresh'")

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
            exp=current_timestamp + ttl,
            type="refresh"
        )

        return RefreshToken(jwt.encode(payload=data, key=JWT_SECRET, algorithm='HS256'))

    @staticmethod
    def from_secret_id(secret_id: str, ttl: int):
        current_timestamp = datetime.timestamp((datetime.now(tz=timezone.utc)))

        data = dict(
            iss='LongCorp@auth_service',
            sub=secret_id,
            jti=str(uuid.uuid4()),
            iat=current_timestamp,
            nbf=current_timestamp,
            exp=current_timestamp + ttl,
            type='refresh'
        )

        return RefreshToken(jwt.encode(payload=data, key=JWT_SECRET, algorithm='HS256'))

    def __str__(self):
        return self.__token

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__token == other.__token
        return False


class AccessToken:

    def __init__(self, token: str):
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        if payload["type"] == "access":
            self.__token = token
        else:
            raise TypeError("Token type must be 'access'")

    def get_secret_id(self):
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
            exp=current_timestamp + ttl,
            type="access"
        )

        return AccessToken(jwt.encode(payload=data, key=JWT_SECRET, algorithm='HS256'))

    def __str__(self):
        return self.__token
