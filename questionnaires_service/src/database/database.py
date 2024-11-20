from abc import ABC, abstractmethod
from uuid import UUID

import aiomysql

from questionnaires_service.src.models.models import QuestionnaireOut, QuestionnaireIn


class DBConnection(ABC):
    @staticmethod
    @abstractmethod
    def _create_pool(data_base_data: dict):
        pass

    @staticmethod
    @abstractmethod
    def get_pool(data_base_data: dict) -> aiomysql.Pool:
        pass

    @staticmethod
    @abstractmethod
    def close(self):
        pass


class MySqlConnection(DBConnection):
    __pool = None

    @staticmethod
    async def _create_pool(data_base_data: dict):
        MySqlConnection.__pool = await aiomysql.create_pool(**data_base_data)

    @staticmethod
    async def get_pool(data_base_data: dict) -> aiomysql.Pool:
        if not MySqlConnection.__pool:
            await MySqlConnection._create_pool(data_base_data)
        return MySqlConnection.__pool

    @staticmethod
    async def close(self):
        if MySqlConnection.__pool:
            MySqlConnection.__pool.close()
            await self.pool.wait_closed()
            MySqlConnection.__pool = None


class MySqlCommands:
    def __init__(self, database_data: dict):
        self.__pool = None
        self.__database_data = database_data

    async def __create_pool(self):
        self.__pool = await MySqlConnection.get_pool(self.__database_data)

    async def _create(self, query: str, params: tuple|None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)

    async def _read(self, query: str, params: tuple|None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                result = await cur.fetchall()
                return result

    async def _update(self, query: str, params: tuple|None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)

    async def _delete(self, query: str, params: tuple|None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)


class QuestionnairesDataBase(MySqlCommands):

    def __init__(self, database_data: dict):
        super().__init__(database_data)

    async def get_by_page(self, page: int, limit: int) -> list[QuestionnaireOut]:
        pass

    async def add_questionnaire(self, questionnaire_in: QuestionnaireIn):
        pass


class UsersDataBase(MySqlCommands):
    def __init__(self, database_data: dict):
        super().__init__(database_data)

    async def get_public_id(self, secret_id: UUID) -> int:
        pass
