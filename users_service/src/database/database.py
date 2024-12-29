import logging
from abc import abstractmethod, ABC

import aiomysql
from pydantic import ValidationError

from src.models.models import UserModel
from src.utils.utils import get_validated_user_dict_from_tuple

logger = logging.getLogger(__name__)

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
        logger.info("Creating MySql pool")
        self.__pool = await MySqlConnection.get_pool(self.__database_data)
        logger.info("MySql pool created")

    async def _create(self, query: str, params: tuple | None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)

    async def _read(self, query: str, params: tuple | None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                result = await cur.fetchall()
                return result

    async def _update(self, query: str, params: tuple | None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)

    async def _delete(self, query: str, params: tuple | None = None):
        if not self.__pool:
            await self.__create_pool()

        async with self.__pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)


class UsersDataBase(MySqlCommands):
    def __init__(self, database_data: dict):
        super().__init__(database_data)

    async def get_user_by_nickname(self, nickname: str) -> UserModel | None:
        try:
            logger.info("Getting user by nickname for user %s", nickname)
            response = await self._read(
                "SELECT * FROM Users WHERE nickname = %s",
                (nickname,)
            )
            user = UserModel(**get_validated_user_dict_from_tuple(response[0]))
            logger.info("Done getting user by nickname for user %s", nickname)
            return user
        except (IndexError, ValidationError):
            logger.error("Can't get user by nickname for user %s", nickname)
            return None

    async def get_user_by_public_id(self, public_id: str) -> UserModel | None:
        try:
            logger.info("Getting user by public ID for user %s", public_id)
            response = await self._read(
                "SELECT * FROM Users WHERE public_id = %s",
                (public_id,)
            )
            user = UserModel(**get_validated_user_dict_from_tuple(response[0]))
            logger.info("Done getting user by public ID for user %s", public_id)
            return user
        except (IndexError, ValidationError):
            logger.error("Can't get user by public ID for user %s", public_id)
            return None