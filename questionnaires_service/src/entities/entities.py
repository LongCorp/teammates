import logging
from dataclasses import dataclass
from typing import Final

from src.database.cache import QuestionnairesCache
from src.config import redis_config


@dataclass(frozen=True)
class DBEntities:
    questionnaires_cache: Final[QuestionnairesCache] = QuestionnairesCache(redis_config)


@dataclass(frozen=True)
class LoggerHandlers:
    file_handler: Final[logging.FileHandler] = logging.FileHandler("./logs/service.log")
    console_handler: Final[logging.StreamHandler] = logging.StreamHandler()
