from __future__ import annotations

import json
import uuid
from uuid import UUID
from typing import List, Optional
import aiohttp

from fastapi import FastAPI, Depends, HTTPException, UploadFile, Body
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import TypeAdapter
from starlette import status

from src.models.models import QuestionnaireOut, QuestionnaireIn, Game
from src.entities.entities import DBEntities
from src.utils.utils import save_questionnaire_image
from src.config import auth_service_url

app = FastAPI(
    version='1.0.0',
    title='TeamMates questionnaires API',
    contact={'name': 'LongCorp', 'email': 'LongCorp@gmail.com'},
)

auth_scheme = HTTPBearer()


async def authenticate_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> UUID:
    async with aiohttp.ClientSession() as session:
        response = await session.request(
            "get", f"{auth_service_url}/get_id_by_token",
            params={"token": token.credentials}
        )

        user_secret_id = await response.json()
        if user_secret_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    return UUID(user_secret_id)


@app.get(
    '/questionnaires/{game}',
    response_model=List[QuestionnaireOut]
)
async def get_questionnaires(
        game: Game,
        user_id: int,
        page: Optional[int] = 1, limit: Optional[int] = 10,
        secret_id: UUID = Depends(authenticate_user)
) -> List[QuestionnaireOut] | str:
    current_user_id = await DBEntities.users_db.get_public_id(secret_id)
    if user_id == current_user_id:
        questionnaires = await DBEntities.questionnaires_cache.get_questionnaires(user_id)

        if questionnaires[0] is None:
            type_adapter = TypeAdapter(list[QuestionnaireOut])
            questionnaires = await DBEntities.questionnaires_db.get_by_game(game)
            encoded = type_adapter.dump_json(questionnaires).decode("utf-8")
            await DBEntities.questionnaires_cache.set_questionnaires(user_id, encoded)

        start_index = (page - 1) * limit
        return questionnaires[start_index:start_index + limit]
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')


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
