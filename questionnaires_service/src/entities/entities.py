import logging
from dataclasses import dataclass
from typing import Final

from src.database.cache import QuestionnairesCache
from src.database.database import QuestionnairesDataBase, UsersDataBase
from src.config import db_data, redis_config


@dataclass(frozen=True)
class DBEntities:
    users_db: Final[UsersDataBase] = UsersDataBase(db_data)
    questionnaires_db: Final[QuestionnairesDataBase] = QuestionnairesDataBase(db_data)
    questionnaires_cache: Final[QuestionnairesCache] = QuestionnairesCache(redis_config)


@dataclass(frozen=True)
class LoggerHandlers:
    file_handler: Final[logging.FileHandler] = logging.FileHandler("./logs/service.log")
    console_handler: Final[logging.StreamHandler] = logging.StreamHandler()
