import asyncio
import logging
import uuid
from abc import ABC, abstractmethod
from uuid import UUID

import aiomysql
from pydantic import ValidationError
from pymysql import IntegrityError

from src.entities.tokens import RefreshToken
from src.models.models import UserModel, RegisterModel
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

    async def get_public_id(self, secret_id: UUID) -> int | None:
        try:
            logger.info("Getting public id for user %s", secret_id)
            response = await self._read(
                "SELECT public_id FROM Users WHERE secret_id = %s",
                (secret_id,)
            )
            logger.info("Done getting public id for user %s", secret_id)
            return response[0][0]
        except IndexError as e:
            logger.error("Can't get public_id for user with secret_id %s", secret_id, exc_info=e)
            return None

    async def get_password_hash_by_nickname(self, nickname: str) -> int | None:
        try:
            logger.info("Getting password hash for user %s", nickname)
            response = await self._read(
                "SELECT password FROM Users JOIN UsersPasswords on Users.public_id WHERE Users.nickname = %s ",
                (nickname,)
            )
            logger.info("Done getting password hash for user %s", nickname)
            return response[0][0]
        except IndexError:
            logger.error("Can't get password hash for user %s", nickname)
            return None

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

    async def create_user(self, register_data: RegisterModel) -> UserModel | None:
        try:
            logger.info("Started creating new user %s", register_data.login)

            await self._create(
                "START transaction;"
                "SET @nickname := %s COLLATE utf8mb4_0900_ai_ci;"
                "INSERT INTO Users (secret_id, nickname, email) VALUES (%s, @nickname, %s);"
                "SET @user_id := (SELECT public_id FROM Users WHERE nickname = (SELECT @nickname));"
                "INSERT INTO UsersPasswords VALUES (@user_id, %s);"
                "COMMIT;",
                (register_data.login, uuid.uuid4(), register_data.email, register_data.password)
            )
            logger.info("Done creating new user %s", register_data.login)

            created_user = await self.get_user_by_nickname(register_data.login)
            return created_user
        except Exception as e:
            logger.error("Error while creating new user %s", register_data.login, exc_info=e)
            return None


class TokensDataBase(MySqlCommands):
    def __init__(self, database_data: dict):
        super().__init__(database_data)

    async def update_refresh_token_for_user(self, user_id: int, refresh_token: RefreshToken) -> bool:
        try:
            logger.info("Updating refresh token for user %s", user_id)
            await self._update(
                "SET @token = %s;"
                "INSERT INTO UsersTokens VALUES (%s, @token) ON DUPLICATE KEY UPDATE refresh_token = @token;",
                (refresh_token, user_id)
            )
            logger.info("Done updating refresh token for user %s", user_id)
            return True
        except Exception as e:
            logger.error("Error while updating refresh token for user %s", user_id, exc_info=e)
            return False

    async def get_refresh_token_for_user(self, user_id: int) -> RefreshToken | None:
        try:
            logger.info("Getting refresh token for user %s", user_id)
            response = await self._read(
                "SELECT refresh_token FROM UsersTokens WHERE user_id = %s;",
                (user_id, ))
            return RefreshToken(response[0][0])
        except (IndexError, IntegrityError):
            logger.error("Can't get refresh token for user %s", user_id)
            return None
