from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter
from pydantic import TypeAdapter

from src.models.models import QuestionnaireModel, GameEnum
from src.entities.entities import DBEntities
from src.database import questionnaires_methods

questionnaires_router = APIRouter(prefix="/questionnaires")


@questionnaires_router.get(
    '',
    response_model=List[QuestionnaireModel]
)
async def get_questionnaires(
        user_id: UUID,
        page: Optional[int] = 1,
        limit: Optional[int] = 10,
        game: Optional[GameEnum] = None,
        author_id: Optional[UUID] = None,
        questionnaire_id: Optional[UUID] = None,
) -> List[QuestionnaireModel] | str:
    questionnaires = await DBEntities.questionnaires_cache.get_questionnaires(
        user_id, game, author_id, questionnaire_id
    )

    try:
        if author_id == user_id:
            questionnaires = await questionnaires_methods.get_questionnaires(
                game=game, author_id=author_id, questionnaire_id=questionnaire_id
            )
        elif questionnaires[0] is None:
            type_adapter = TypeAdapter(list[QuestionnaireModel])
            questionnaires = await questionnaires_methods.get_questionnaires(
                game=game, author_id=author_id, questionnaire_id=questionnaire_id
            )
            encoded = type_adapter.dump_json(questionnaires).decode("utf-8")

            await DBEntities.questionnaires_cache.set_questionnaires(
                user_id, game, author_id, questionnaire_id, value=encoded
            )
    except IndexError:
        return []

    start_index = (page - 1) * limit
    return questionnaires[start_index:start_index + limit]
