import logging
from abc import abstractmethod, ABC
from uuid import UUID

import aiomysql
from pydantic import ValidationError
from pymysql import IntegrityError

from src.models.models import QuestionnaireOut
from src.models.models import UserModel
from src.utils.utils import get_validated_user_dict_from_tuple, get_validated_questionnaire_dict_from_tuple

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
        except (IndexError, ValidationError) as e:
            logger.error("Can't get user by nickname for user %s: ", nickname, exc_info=e)
            return None

    async def get_user_by_public_id(self, public_id: int) -> UserModel | None:
        try:
            logger.info("Getting user by public ID for user %s", public_id)
            response = await self._read(
                "SELECT * FROM Users WHERE public_id = %s",
                (public_id,)
            )
            user = UserModel(**get_validated_user_dict_from_tuple(response[0]))
            logger.info("Done getting user by public ID for user %s", public_id)
            return user
        except (IndexError, ValidationError) as e:
            logger.error("Can't get user by public ID for user %s: ", public_id, exc_info=e)
            return None

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


class LikedQuestionnairesDataBase(MySqlCommands):
    def __init__(self, database_data: dict):
        super().__init__(database_data)

    async def add_questionnaire(self, liker_id: int, questionnaire_id: UUID):
        try:
            logger.info("Adding a questionnaire %s like by an user %s", questionnaire_id, liker_id)
            await super()._create(
                "INSERT INTO LikedQuestionnaires (questionnaire_id, liker_id) VALUES (%s, %s)",
                (questionnaire_id, liker_id)
            )
        except IntegrityError as e:
            logger.error("Error while adding an questionnaire %s like by an user %s: ", questionnaire_id, liker_id, exc_info=e)

    async def delete_questionnaire(self, liker_id: int, questionnaire_id: UUID):
        try:
            logger.info("Deletion the questionnaire %s like by user %s", questionnaire_id, liker_id)
            await super()._delete(
                "DELETE FROM LikedQuestionnaires WHERE liker_id = %s AND questionnaire_id = %s",
                (liker_id, questionnaire_id)
            )
        except IntegrityError as e:
            logger.error("Error while deletion the questionnaire %s like by user %s: ", questionnaire_id, liker_id, exc_info=e)

    async def check_existing(self, liker_id: int, questionnaire_id: UUID):
        try:
            logger.info("Checking the questionnaire %s like by user %s", questionnaire_id, liker_id)
            exists = await super()._read(
                """SELECT EXISTS (
                                SELECT 1
                                FROM LikedQuestionnaires
                                WHERE liker_id = %s AND questionnaire_id = %s
                )""",
                (liker_id, questionnaire_id)
            )
            return exists[0][0]
        except (IndexError, ValidationError, IntegrityError) as e:
            logger.error("Error while checking the questionnaire %s like by user %s: ", questionnaire_id, liker_id, exc_info=e)
            return None

    async def get_liked_questionnaires(self, liker_id: int) -> list | None:
        try:
            logger.info("Getting questionnaires liked by user %s", liker_id)
            response = await super()._read("""
                SELECT author_public_id, questionnaire_id, header, description, image_path, game
                    FROM Questionnaires
                    JOIN LikedQuestionnaires ON Questionnaires.id = LikedQuestionnaires.questionnaire_id
                    WHERE LikedQuestionnaires.liker_id = %s;
                """, (liker_id,))
            result = [QuestionnaireOut(**get_validated_questionnaire_dict_from_tuple(i)) for i in response]
            return result
        except (IntegrityError, ValidationError, ValueError) as e:
            logger.error("Error while getting questionnaires liked by user %s", liker_id, exc_info=e)
            return None


class LikedUsersDataBase(MySqlCommands):
    def __init__(self, database_data: dict):
        super().__init__(database_data)

    async def add_user(self, liker_id: int, liked_id: int):
        try:
            logger.info("Adding an user %s like by an user %s", liked_id, liker_id)
            await super()._create(
                "INSERT INTO LikedUsers (liked_id, liker_id) VALUES (%s, %s)",
                (liked_id, liker_id)
            )
        except IntegrityError as e:
            logger.error("Error while adding an user %s like by an user %s: ", liked_id, liker_id, exc_info=e)


    async def delete_user(self, liker_id: int, liked_id: int):
        try:
            logger.info("Deletion the users %s like by user %s", liked_id, liker_id)
            await super()._delete(
                "DELETE FROM LikedUsers WHERE liker_id = %s AND liked_id = %s",
                (liker_id, liked_id)
            )
        except IntegrityError as e:
            logger.error("Error while deletion the users %s like by user %s: ", liked_id, liker_id, exc_info=e)


    async def check_existing(self, liker_id: int, liked_id: int):
        try:
            logger.info("Checking the user like %s by user %s", liked_id, liker_id)
            exists = await super()._read(
                """SELECT EXISTS (
                                SELECT 1
                                FROM LikedUsers
                                WHERE liker_id = %s AND liked_id = %s
                )""",
                (liker_id, liked_id)
            )
            return exists[0][0]
        except (IndexError, ValidationError, IntegrityError) as e:
            logger.error("Error while checking the user like %s by user %s: ", liked_id, liker_id, exc_info=e)
            return None

    async def get_liked_users(self, liker_id: int):
        try:
            logger.info("Getting users liked by user %s", liker_id)
            response = await super()._read("""
                SELECT public_id, secret_id, nickname, email, description, image_path
                    FROM Users
                    JOIN LikedUsers ON Users.public_id = LikedUsers.liked_id
                    WHERE LikedUsers.liker_id = %s
            """, (liker_id,))
            result = [UserModel(**get_validated_user_dict_from_tuple(i)) for i in response]
            return result
        except (IntegrityError, ValueError) as e:
            logger.error("Error getting users liked by user %s", liker_id, exc_info=e)
            return None


class QuestionnairesDataBase(MySqlCommands):
    def __init__(self, database_data: dict):
        super().__init__(database_data)

    async def check_existing(self, questionnaire_id):
        try:
            logger.info("Checking the existence of a questionnaire %s", questionnaire_id)
            exists = await super()._read(
                        """SELECT EXISTS (
                                SELECT 1
                                FROM Questionnaires
                                WHERE id = %s
                )""",
                (questionnaire_id,)
            )
            return exists[0][0]
        except (IndexError, ValidationError, IntegrityError) as e:
            logger.error("Error while checking the existence of a questionnaire %s: ", questionnaire_id, exc_info=e)
            return None