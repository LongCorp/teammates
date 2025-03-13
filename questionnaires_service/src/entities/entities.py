import logging
from dataclasses import dataclass
from typing import Final

from src.database.cache import QuestionnairesCache
from src.config import redis_config


@dataclass(frozen=True)
class DBEntities:
    questionnaires_cache: Final[QuestionnairesCache] = QuestionnairesCache(redis_config)
