from __future__ import annotations

from uuid import UUID
from typing import Optional

from fastapi import UploadFile, Body, Request, APIRouter, HTTPException, Response

from src.models.models import QuestionnaireModel, QuestionnaireInModel
from src.database import questionnaires_methods

questionnaire_router = APIRouter(prefix="/questionnaire")


@questionnaire_router.post(
    '',
    response_model=Optional[QuestionnaireModel],
)
async def post_questionnaire(
        user_id: UUID,
        request: Request,
        questionnaire_in: QuestionnaireInModel = Body(...),
        image: Optional[UploadFile] = None,
) -> Response:
    if user_id == questionnaire_in.author_id:
        response_questionnaire = await questionnaires_methods.add_questionnaire(
            questionnaire_in=questionnaire_in,
            image=image,
            request_url=str(request.url)
        )
        return Response(status_code=201, content=response_questionnaire.model_dump_json())
    raise HTTPException(400, "author_id and user_id must be the same")


@questionnaire_router.put(
    "/{questionnaire_id}",
    response_model=QuestionnaireModel
)
async def put_questionnaire(
        user_id: UUID,
        questionnaire_id: UUID,
        request: Request,
        questionnaire_in: QuestionnaireInModel = Body(...),
        image: Optional[UploadFile] = None
) -> QuestionnaireModel:
    if user_id == questionnaire_in.author_id:
        updated_questionnaire = await questionnaires_methods.update_questionnaire(
            questionnaire_id=questionnaire_id,
            questionnaire_in=questionnaire_in,
            image=image,
            request_url=str(request.url)
        )
        return updated_questionnaire

    raise HTTPException(400, "author_id and user_id must be the same")


@questionnaire_router.delete(
    '/{questionnaire_id}',
)
async def delete_questionnaire(
        user_id: UUID,
        questionnaire_id: UUID
) -> Response:
    try:
        questionnaire = await questionnaires_methods.get_questionnaires(questionnaire_id=questionnaire_id)
        questionnaire = questionnaire[0]
        if questionnaire.author_id == user_id:
            deleted = await questionnaires_methods.delete_questionnaire(questionnaire_id)
            if deleted:
                return Response(status_code=200, content=f"Deleted {questionnaire_id}")
            raise HTTPException(500)
        raise HTTPException(status_code=400, detail="Questionnaire don't belong to user")
    except IndexError:
        raise HTTPException(status_code=404, detail="Wrong questionnaire id")
