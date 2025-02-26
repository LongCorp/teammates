import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.dao.dao import QuestionnaireDAO
from src.database.dao.session_maker import connection
from src.models.models import QuestionnaireOut

logger = logging.getLogger(__name__)

@connection()
async def get_questionnaire(session: AsyncSession, questionnaire_id: UUID) -> QuestionnaireOut:
    logger.info("Getting questionnaire %s from db", questionnaire_id)
    try:
        questionnaire = await QuestionnaireDAO.find_one_or_none_by_id(session=session, data_id=questionnaire_id)
        pydantic_questionnaire = QuestionnaireOut.model_validate(questionnaire, from_attributes=True)
        return pydantic_questionnaire
    except Exception as e:
        logger.error("Error while getting questionnaire %s from db:", questionnaire_id, exc_info=e)
        raise HTTPException(500)


