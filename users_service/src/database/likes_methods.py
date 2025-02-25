import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from questionnaires_service.src.models.models import QuestionnaireOut
from src.database.dao.dao import LikedQuestionnaireDAO, LikedUserDAO
from src.database.dao.session_maker import connection
from src.models.models import QuestionnaireLikeModel, UserLikeModel, UserModel


logger = logging.getLogger(__name__)


@connection()
async def get_liked_questionnaires(session: AsyncSession, liker_id: UUID) -> list[QuestionnaireOut]:
    logger.info("Getting questionnaires liked by user %s", liker_id)
    try:
        records = await LikedQuestionnaireDAO.get_liked_questionnaires(session=session, liker_id=liker_id)
        result = [QuestionnaireOut.model_validate(i, from_attributes=True) for i in records]
    except Exception as e:
        logger.error("Error while getting questionnaires liked by user %s", liker_id, exc_info=e)
        raise HTTPException(500)
    return result


@connection()
async def check_questionnaire_like(liker_id: UUID, questionnaire_id: UUID, session: AsyncSession):
    logger.info("Checking questionnaire %s like from user %s", questionnaire_id, liker_id)
    try:
        like = await LikedQuestionnaireDAO.check_like(liker_id=liker_id, questionnaire_id=questionnaire_id, session=session)
        return like
    except Exception as e:
        logger.info("Error while checking  questionnaire %s like from user %s", questionnaire_id, liker_id)
        raise HTTPException(500)

@connection()
async def get_liked_users(session: AsyncSession, liker_id: UUID) -> list[UserModel]:
    logger.info("Getting users liked by user %s", liker_id)
    try:
        records = await  LikedUserDAO.get_liked_users(session=session, liker_id=liker_id)
        result = [UserModel.model_validate(i, from_attributes=True) for i in records]
    except Exception as e:
        logger.error("Error getting users liked by user %s", liker_id, exc_info=e)
        raise HTTPException(500)
    return result


@connection()
async def check_user_like(liker_id: UUID, liked_id: UUID, session: AsyncSession):
    logger.info("Checking user %s like from user %s", liked_id, liker_id)
    try:
        like = await LikedUserDAO.check_like(liker_id=liker_id, liked_id=liked_id, session=session)
        return like
    except Exception as e:
        logger.info("Error while checking  questionnaire %s like from user %s", liked_id, liker_id)
        raise HTTPException(500)


@connection()
async def add_like_to_questionnaire(session: AsyncSession, liker_id: UUID, questionnaire_id: UUID) -> QuestionnaireLikeModel:
    logger.info("Adding a questionnaire %s like by an user %s", questionnaire_id, liker_id)
    model = QuestionnaireLikeModel(liker_id=liker_id, questionnaire_id=questionnaire_id)
    try:
        result = await LikedQuestionnaireDAO.add(session=session, values=model)
    except Exception as e:
        logger.error("Error while adding an questionnaire %s like by an user %s: ", questionnaire_id, liker_id,
                     exc_info=e)
        raise HTTPException(500)
    return QuestionnaireLikeModel.model_validate(result, from_attributes=True)


@connection()
async def add_like_to_user(session: AsyncSession, liker_id: UUID, liked_id: UUID) -> UserLikeModel:
    logger.info("Adding an user %s like by an user %s", liked_id, liker_id)
    model = UserLikeModel(liked_by_id=liker_id, liked_id=liked_id)
    try:
        result = await LikedUserDAO.add(session=session, values=model)
    except Exception as e:
        logger.error("Error while adding an user %s like by an user %s: ", liked_id, liker_id, exc_info=e)
        raise HTTPException(500)
    return UserLikeModel.model_validate(result, from_attributes=True)


@connection()
async def delete_liked_questionnaire(session: AsyncSession, liker_id: UUID, questionnaire_id: UUID) -> bool:
    logger.info("Deletion the questionnaire %s like by user %s", questionnaire_id, liker_id)
    try:
        deleted_status = await LikedQuestionnaireDAO.delete_like(liker_id=liker_id,
                                                                 questionnaire_id=questionnaire_id,
                                                                 session=session
        )
    except Exception as e:
        logger.error("Error while deletion the questionnaire %s like by user %s: ", questionnaire_id, liker_id,
                     exc_info=e)
        return HTTPException(500)
    return deleted_status


@connection()
async def delete_liked_user(session: AsyncSession, liker_id: UUID, liked_id: UUID) -> bool:
    logger.info("Deletion the users %s like by user %s", liked_id, liker_id)
    try:
        deleted_status = await LikedUserDAO.delete_like(liker_id=liker_id,
                                                        liked_id=liked_id,
                                                        session=session
        )
    except Exception as e:
        logger.error("Error while checking the user like %s by user %s: ", liked_id, liker_id, exc_info=e)
        raise HTTPException(500)
    return deleted_status