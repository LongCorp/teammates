from abc import ABC, abstractmethod
from uuid import UUID

import aiomysql

from src.models.models import QuestionnaireOut, QuestionnaireIn, Game
from src.utils.utils import get_validated_dict_from_tuple


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

    async def get_by_game(self, game: Game) -> list[QuestionnaireOut]:
        result = await super()._read(
            "SELECT * FROM Questionnaires WHERE game = %s ORDER BY RAND()",
            (game.value, )
        )
        result = [QuestionnaireOut(**get_validated_dict_from_tuple(i)) for i in result]
        return result

    async def add_questionnaire(self, questionnaire_in: QuestionnaireIn,
                                image_path: str, questionnaire_id: UUID) -> QuestionnaireOut:
        await self._create(
            "INSERT INTO Questionnaires (author_public_id, id, header, description, image_path, game)"
            " VALUES (%s, %s, %s, %s, %s, %s)",
            (questionnaire_in.author_id, questionnaire_id, questionnaire_in.header,
             questionnaire_in.description, image_path, questionnaire_in.game.value)
        )
        return QuestionnaireOut(
            header=questionnaire_in.header,
            game=questionnaire_in.game.value,
            description=questionnaire_in.description,
            author_id=questionnaire_in.author_id,
            photo_path=image_path,
            questionnaire_id=questionnaire_id
        )


class UsersDataBase(MySqlCommands):
    def __init__(self, database_data: dict):
        super().__init__(database_data)

    async def get_public_id(self, secret_id: UUID) -> int:
        response = await self._read(
            "SELECT public_id FROM Users WHERE secret_id = %s",
            (secret_id,)
        )

        return response[0][0]
