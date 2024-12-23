from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter
from pydantic import TypeAdapter

from src.models.models import QuestionnaireOut, Game
from src.entities.entities import DBEntities

questionnaires_router = APIRouter(
    prefix="/questionnaires",
)


@questionnaires_router.get(
    '/{game}',
    response_model=List[QuestionnaireOut]
)
async def get_questionnaires(
        game: Game,
        user_id: int,
        page: Optional[int] = 1, limit: Optional[int] = 10,
) -> List[QuestionnaireOut] | str:
    questionnaires = await DBEntities.questionnaires_cache.get_questionnaires(user_id, game)

    if questionnaires[0] is None:
        type_adapter = TypeAdapter(list[QuestionnaireOut])
        questionnaires = await DBEntities.questionnaires_db.get_by_game(game)
        encoded = type_adapter.dump_json(questionnaires).decode("utf-8")

        await DBEntities.questionnaires_cache.set_questionnaires(user_id, game, encoded)

    start_index = (page - 1) * limit
    return questionnaires[start_index:start_index + limit]
