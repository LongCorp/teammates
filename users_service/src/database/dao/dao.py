from typing import TypeVar, Generic
from uuid import UUID


from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from src.database.dao.models import Base, User, Questionnaire, LikedQuestionnaire, LikedUser
from src.models.models import UserModel

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: UUID, session: AsyncSession):
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None):
        if filters:
            filter_dict = filters.model_dump(exclude_none=True, exclude_unset=True)
        else:
            filter_dict = {}
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def delete_one_by_id(cls, data_id: UUID, session: AsyncSession):
        try:
            data = await session.get(cls.model, data_id)
            if data:
                await session.delete(data)
                await session.flush()

            return True
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_public_id_by_auth_id(cls, auth_id: UUID, session: AsyncSession):
        try:
            stmp = sa.select(cls.model.id).where(cls.model.auth_id == auth_id)

            result = await session.execute(stmp)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def get_user_by_nickname(cls, nickname: str, session: AsyncSession) -> User:

        try:
            query = sa.select(cls.model).where(cls.model.nickname == nickname)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            return result
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def update_profile_info(
            cls,
            user_id: UUID,
            user: UserModel,
            session: AsyncSession
    ) -> bool:
        try:
            query = sa.update(cls.model).where(cls.model.id == user_id).values(user.model_dump())
            await session.execute(query)
            user = await  cls.find_one_or_none_by_id(user_id, session)
            return user
        except SQLAlchemyError as e:
            raise e



class QuestionnaireDAO(BaseDAO[Questionnaire]):
    model = Questionnaire


class LikedQuestionnaireDAO(BaseDAO[LikedQuestionnaire]):
    model = LikedQuestionnaire

    @classmethod
    async def delete_like(cls, liker_id: UUID, questionnaire_id: UUID, session: AsyncSession):
        try:
            query = sa.select(cls.model).where(
                cls.model.questionnaire_id == questionnaire_id,
                cls.model.liker_id == liker_id
            )
            result = await session.execute(query)
            like = result.scalar_one_or_none()
            if like:
                await session.delete(like)
                await session.flush()
                return True
            return False
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

    @classmethod
    async def get_liked_questionnaires(cls, liker_id: UUID, session: AsyncSession):
        try:
            query = sa.select(Questionnaire).join(cls.model).where(cls.model.liker_id == liker_id,
                                                                   cls.model.questionnaire_id == Questionnaire.id
            )
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def check_like(cls, liker_id: UUID, questionnaire_id: UUID, session: AsyncSession):
        try:
            query = sa.select(LikedQuestionnaire).where(cls.model.liker_id == liker_id,
                                                        cls.model.questionnaire_id == questionnaire_id
            )
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            return result
        except SQLAlchemyError as e:
            raise e


class LikedUserDAO(BaseDAO[LikedUser]):
    model = LikedUser

    @classmethod
    async def delete_like(cls, liker_id: UUID, liked_id: UUID, session: AsyncSession):
        try:
            query = sa.select(cls.model).where(
                cls.model.liked_id == liked_id,
                cls.model.liked_by_id == liker_id
            )
            result = await session.execute(query)
            like = result.scalar_one_or_none()
            if like:
                await session.delete(like)
                await session.flush()
                return True
            return False
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

    @classmethod
    async def get_liked_users(cls, liker_id: UUID, session: AsyncSession):
        try:
            query = sa.select(User).join(cls.model, User.id == LikedUser.liked_id).where(cls.model.liked_by_id == liker_id,
                                                                   cls.model.liked_id == User.id
            )
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def check_like(cls, liker_id: UUID, liked_id: UUID, session: AsyncSession):
        try:
            query = sa.select(LikedUser).where(cls.model.liked_by_id == liker_id,
                                                        cls.model.liked_id == liked_id
            )
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            return result
        except SQLAlchemyError as e:
            raise e

