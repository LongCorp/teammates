import logging
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from pydantic import create_model
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.dao import QuestionnaireDAO
from src.database.dao.session_maker import connection
from src.models.models import GameEnum, QuestionnaireOut, QuestionnaireIn

logger = logging.getLogger(__name__)


@connection()
async def get_questionnaires(
        session: AsyncSession,
        game: Optional[GameEnum] = None,
        author_id: Optional[int] = None,
        questionnaire_id: Optional[UUID] = None
) -> list[QuestionnaireOut]:
    FiltersModel = create_model(
        "FiltersModel",
        game=(Optional[GameEnum], ...),
        author_id=(Optional[UUID], ...),
        id=(Optional[UUID], ...)
    )

    logger.info(
        "Getting questionnaires from db for (%s, %s, %s)",
        game, author_id, questionnaire_id
    )

    try:
        records = await QuestionnaireDAO.find_all(session=session,
                                                  filters=FiltersModel(
                                                      game=game,
                                                      author_id=author_id,
                                                      id=questionnaire_id)
                                                  )
        result = [QuestionnaireOut.model_validate(i) for i in records]

        logger.info(
            "Done getting questionnaires from db for (%s, %s, %s)",
            game, author_id, questionnaire_id
        )
    except Exception as e:
        logger.error(
            "Error while getting questionnaires from db for (%s, %s, %s)",
            game, author_id, questionnaire_id,
            exc_info=e
        )
        raise HTTPException(500)

    return result


@connection()
async def add_questionnaire(
        questionnaire_in: QuestionnaireIn,
        image_path: str,
        questionnaire_id: UUID,
        session: AsyncSession
) -> QuestionnaireOut:
    data = questionnaire_in.model_dump()
    data["image_path"] = image_path
    data["id"] = questionnaire_id
    logger.info("Adding questionnaire (%s) to db", questionnaire_in)
    try:
        result = await QuestionnaireDAO.add(session=session, values=QuestionnaireOut(**data))
    except Exception as e:
        logger.error("Error while adding questionnaire %s to db", questionnaire_in, exc_info=e)
        raise HTTPException(500)

    logger.info("Done adding questionnaire (%s) to db", questionnaire_in)

    return QuestionnaireOut.model_validate(result)


@connection()
async def delete_questionnaire(questionnaire_id: UUID, session: AsyncSession):
    logger.info("Start deleting questionnaire (%s) from db", questionnaire_id)
    try:
        deleted_status = await QuestionnaireDAO.delete_one_by_id(questionnaire_id, session=session)
    except Exception as e:
        logger.error("Error while deleting questionnaire %s from db", questionnaire_id, exc_info=e)
        return False

    logger.info("Done deleting questionnaire (%s) from db", questionnaire_id)
    return deleted_status
