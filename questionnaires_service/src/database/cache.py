from typing import List

import aioredis
from aioredis import Redis

from questionnaires_service.src.models.models import QuestionnaireIn, QuestionnaireOut

EXPIRATION_TIME = 3600

class RedisConnection:
    __con = None

    @staticmethod
    async def __create_connection():
        RedisConnection.__con = await aioredis.from_url("redis://localhost", decode_responses=True)

    @staticmethod
    async def get_connection() -> Redis:
        if not RedisConnection.__con:
            RedisConnection.__con = await RedisConnection.__create_connection()
        return RedisConnection.__con


class QuestionnairesCache:
    def __init__(self):
        self.__con = None

    async def __create_connection(self):
        self.__con = RedisConnection.get_connection()

    async def set_questionnaires(self, user_id: int, questionnaires: List[QuestionnaireOut]):
        if not self.__con:
            await self.__create_connection()

        await self.__con.set(user_id, questionnaires)
        await self.__con.expire(user_id, EXPIRATION_TIME)

    async def get_questionnaires(self, user_id: int) -> List[QuestionnaireOut] | None:
        if not self.__con:
            await self.__create_connection()

        result = await self.__con.get(user_id)
        return result
