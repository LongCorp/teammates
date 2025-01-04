from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter
from pydantic import TypeAdapter

from src.models.models import QuestionnaireOut, Game
from src.entities.entities import DBEntities

questionnaires_router = APIRouter()


@questionnaires_router.get(
    '/questionnaires',
    response_model=List[QuestionnaireOut]
)
async def get_questionnaires(
        user_id: int,
        page: Optional[int] = 1,
        limit: Optional[int] = 10,
        game: Optional[Game] = None,
        author_id: Optional[int] = None,
        questionnaire_id: Optional[UUID] = None,
) -> List[QuestionnaireOut] | str:
    questionnaires = await DBEntities.questionnaires_cache.get_questionnaires(
        user_id, game, author_id, questionnaire_id
    )

    try:
        if questionnaires[0] is None:
            type_adapter = TypeAdapter(list[QuestionnaireOut])
            questionnaires = await DBEntities.questionnaires_db.get_questionnaires(game, author_id, questionnaire_id)
            encoded = type_adapter.dump_json(questionnaires).decode("utf-8")

            await DBEntities.questionnaires_cache.set_questionnaires(
                user_id, game, author_id, questionnaire_id, value=encoded
            )
    except IndexError:
        return []
    start_index = (page - 1) * limit
    return questionnaires[start_index:start_index + limit]
