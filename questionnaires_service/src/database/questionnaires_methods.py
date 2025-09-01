import logging
import uuid
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, UploadFile
from pydantic import create_model
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.dao import QuestionnaireDAO
from src.database.dao.session_maker import connection
from src.models.models import GameEnum, QuestionnaireModel, QuestionnaireInModel
from src.utils.utils import save_questionnaire_image, delete_questionnaire_photo

logger = logging.getLogger(__name__)


@connection()
async def get_questionnaires(
        session: AsyncSession,
        game: Optional[GameEnum] = None,
        author_id: Optional[int] = None,
        questionnaire_id: Optional[UUID] = None
) -> list[QuestionnaireModel]:
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
                                                      id=questionnaire_id),
                                                  order_by_func=func.random()
                                                  )
        result = [QuestionnaireModel.model_validate(i) for i in records]

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
        questionnaire_in: QuestionnaireInModel,
        session: AsyncSession,
        image: Optional[UploadFile] = None,
        request_url: Optional[str] = None
) -> QuestionnaireModel:
    questionnaire_id = uuid.uuid4()
    image_path = await save_questionnaire_image(image, questionnaire_id, request_url)

    data = questionnaire_in.model_dump()
    data["image_path"] = image_path
    data["id"] = questionnaire_id

    logger.info("Adding questionnaire (%s) to db", questionnaire_in)
    try:
        result = await QuestionnaireDAO.add(session=session, values=QuestionnaireModel(**data))
    except Exception as e:
        logger.error("Error while adding questionnaire %s to db", questionnaire_in, exc_info=e)
        raise HTTPException(500)

    logger.info("Done adding questionnaire (%s) to db", questionnaire_in)

    return QuestionnaireModel.model_validate(result)


@connection()
async def update_questionnaire(
        questionnaire_id: UUID,
        questionnaire_in: QuestionnaireInModel,
        session: AsyncSession,
        image: Optional[UploadFile] = None,
        request_url: Optional[str] = None
) -> Optional[QuestionnaireModel]:
    image_path = await save_questionnaire_image(image, questionnaire_id, request_url)

    data = questionnaire_in.model_dump()
    data["image_path"] = image_path
    data["id"] = questionnaire_id

    logger.info("Updating questionnaire (%s) in db", questionnaire_in)
    try:
        result = await QuestionnaireDAO.update_questionnaire_by_id(
            session=session,
            questionnaire_id=questionnaire_id,
            new_questionnaire=QuestionnaireModel(**data)
        )

    except Exception as e:
        logger.error("Error while updating questionnaire %s in db", questionnaire_in, exc_info=e)
        raise HTTPException(500)

    if result:
        logger.info("Done updating questionnaire (%s) in db", questionnaire_in)
        return QuestionnaireModel(**data)


@connection()
async def delete_questionnaire(questionnaire_id: UUID, session: AsyncSession):
    logger.info("Start deleting questionnaire (%s) from db", questionnaire_id)
    try:
        deleted_status = await QuestionnaireDAO.delete_one_by_id(questionnaire_id, session=session)
        delete_questionnaire_photo(questionnaire_id=questionnaire_id)
    except Exception as e:
        logger.error("Error while deleting questionnaire %s from db", questionnaire_id, exc_info=e)
        return False

    logger.info("Done deleting questionnaire (%s) from db", questionnaire_id)
    return deleted_status
