import logging
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

import aiomysql
from fastapi import HTTPException
from pymysql import IntegrityError

from src.models.models import QuestionnaireOut, QuestionnaireIn, Game
from src.utils.utils import get_validated_dict_from_tuple

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
        self.__pool = await MySqlConnection.get_pool(self.__database_data)

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


class QuestionnairesDataBase(MySqlCommands):

    def __init__(self, database_data: dict):
        super().__init__(database_data)

    async def get_questionnaires(
            self,
            game: Optional[Game] = None,
            author_id: Optional[int] = None,
            questionnaire_id: Optional[UUID] = None) -> list[QuestionnaireOut]:
        try:
            logger.info(
                "Getting questionnaires from db for (%s, %s, %s)",
                game, author_id, questionnaire_id
            )

            query = "SELECT * FROM Questionnaires WHERE 1=1"
            params = set()
            if game:
                query += " AND game=%s"
                params.add(game.value)
            if author_id:
                query += " AND author_public_id=%s"
                params.add(author_id)
            if questionnaire_id:
                query += " AND id=%s"
                params.add(questionnaire_id)
            query += " ORDER BY RAND()"

            result = await super()._read(query, tuple(params))
            result = [QuestionnaireOut(**get_validated_dict_from_tuple(i)) for i in result]
            logger.info(
                "Done getting questionnaires from db for (%s, %s, %s)",
                game, author_id, questionnaire_id
            )
            return result
        except Exception as e:
            logger.error(
                "Error while getting questionnaires from db for (%s, %s, %s)",
                game, author_id, questionnaire_id,
                exc_info=e
            )
            raise HTTPException(500)

    async def add_questionnaire(self, questionnaire_in: QuestionnaireIn,
                                image_path: str, questionnaire_id: UUID) -> QuestionnaireOut:
        try:
            logger.info("Adding questionnaire (%s) to db", questionnaire_in)
            await self._create(
                "INSERT INTO Questionnaires (author_public_id, id, header, description, image_path, game)"
                " VALUES (%s, %s, %s, %s, %s, %s)",
                (questionnaire_in.author_id, questionnaire_id, questionnaire_in.header,
                 questionnaire_in.description, image_path, questionnaire_in.game.value)
            )
            logger.info("Done adding questionnaire (%s) to db", questionnaire_in)
            return QuestionnaireOut(
                header=questionnaire_in.header,
                game=questionnaire_in.game.value,
                description=questionnaire_in.description,
                author_id=questionnaire_in.author_id,
                photo_path=image_path,
                questionnaire_id=questionnaire_id
            )
        except IntegrityError as e:
            logger.error("Error while adding questionnaire %s to db", questionnaire_in, exc_info=e)
            raise HTTPException(400)
        except Exception as e:
            logger.error("Error while adding questionnaire %s to db", questionnaire_in, exc_info=e)
            raise HTTPException(500)

    async def delete_questionnaire(self, user_id: int, questionnaire_id: UUID):
        try:
            logger.info("Start deleting questionnaire (%s) from db", questionnaire_id)
            await self._delete(
                "DELETE FROM Questionnaires WHERE id = %s AND author_public_id = %s",
                (questionnaire_id, user_id)
            )
            logger.info("Done deleting questionnaire (%s) from db", questionnaire_id)
            return True
        except Exception as e:
            logger.error("Error while deleting questionnaire %s from db", questionnaire_id, exc_info=e)
            return False


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
