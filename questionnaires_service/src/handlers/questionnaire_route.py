from __future__ import annotations

import uuid
from typing import Optional

from fastapi import UploadFile, Body, Request, APIRouter, HTTPException, Response

from src.models.models import QuestionnaireOut, QuestionnaireIn
from src.entities.entities import DBEntities
from src.utils.utils import save_questionnaire_image

questionnaire_router = APIRouter()


@questionnaire_router.post(
    '/questionnaire',
    response_model=Optional[QuestionnaireOut]
)
async def post_questionnaire(
        user_id: int,
        request: Request,
        questionnaire_in: QuestionnaireIn = Body(...),
        image: Optional[UploadFile] = None,
) -> Optional[QuestionnaireOut]:
    if user_id == questionnaire_in.author_id:
        questionnaire_id = uuid.uuid4()
        image_path = await save_questionnaire_image(image, questionnaire_id, str(request.url))
        response_questionnaire = await DBEntities.questionnaires_db.add_questionnaire(
            questionnaire_in, image_path, questionnaire_id
        )
        return response_questionnaire
    raise HTTPException(400, "author_id and user_id must be the same")


@questionnaire_router.delete(
    '/questionnaire/{questionnaire_id}',
)
async def delete_questionnaire(
        user_id: int,
        questionnaire_id: uuid.UUID
) -> Response:
    try:
        questionnaire = await DBEntities.questionnaires_db.get_questionnaires(questionnaire_id=questionnaire_id)
        questionnaire = questionnaire[0]
        if questionnaire.author_id == user_id:
            deleted = await DBEntities.questionnaires_db.delete_questionnaire(user_id, questionnaire_id)
            if deleted:
                return Response(status_code=200, content=f"Deleted {questionnaire_id}")
            raise HTTPException(500)
        raise HTTPException(status_code=400, detail="Questionnaire don't belong to user")
    except IndexError:
        raise HTTPException(status_code=404, detail="Wrong questionnaire id")
