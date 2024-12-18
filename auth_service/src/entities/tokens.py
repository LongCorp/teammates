import uuid
from datetime import datetime, timezone

import jwt

from auth_service.src.config import JWT_SECRET
from auth_service.src.models.models import UserModel


class AccessToken:

    def __init__(self, token: str):
        self.__token = token

    def get_secret_key(self):
        payload = jwt.decode(self.__token, JWT_SECRET, algorithms=['HS256'])
        return payload["sub"]

    @staticmethod
    def create_token(user: UserModel, ttl: int):

        current_timestamp = datetime.timestamp((datetime.now(tz=timezone.utc)))

        data = dict(
            iss='LongCorp@auth_service',
            sub=user.secret_id,
            jti=str(uuid.uuid4()),
            iat=current_timestamp,
            nbf=current_timestamp,
            exp=current_timestamp + ttl
        )

        return jwt.encode(payload=data, key=JWT_SECRET, algorithm='HS256')
