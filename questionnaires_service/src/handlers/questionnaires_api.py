from __future__ import annotations

import uuid
from uuid import UUID
from typing import List, Optional, Union, Annotated

import jwt
from fastapi import FastAPI, Depends, HTTPException, Header, UploadFile, Body
from starlette import status

from questionnaires_service.src.models.models import QuestionnaireOut, QuestionnaireIn
from questionnaires_service.src.entities.entities import DBEntities
from questionnaires_service.src.utils.utils import save_questionnaire_image

app = FastAPI(
    version='1.0.0',
    title='TeamMates questionnaires API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)


def authenticate_user(token: str = Depends(...)) -> UUID:
    try:
        ...
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')


@app.get(
    '/questionnaires',
    response_model=List[QuestionnaireOut]
)
async def get_questionnaires(
        page: Optional[int] = 1, limit: Optional[int] = 10
) -> List[QuestionnaireOut] | str:
    questionnaires = await DBEntities.questionnaires_db.get_by_page(page, limit)
    return questionnaires


@app.post(
    '/questionnaire',
    response_model=Optional[QuestionnaireOut],
)
async def post_questionnaire(
        questionnaire_in: QuestionnaireIn = Body(...),
        image: Optional[UploadFile] = None,
        secret_id: UUID = Depends(authenticate_user)
) -> Optional[QuestionnaireOut]:
    current_author_id = await DBEntities.users_db.get_public_id(secret_id)
    if questionnaire_in.author_id == current_author_id:
        questionnaire_id = uuid.uuid4()
        image_path = await save_questionnaire_image(image, questionnaire_id)

        response_questionnaire = await DBEntities.questionnaires_db.add_questionnaire(
            questionnaire_in, image_path, questionnaire_id
        )
        return response_questionnaire
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
