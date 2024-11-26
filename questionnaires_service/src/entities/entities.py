from dataclasses import dataclass
from typing import Final

from questionnaires_service.src.database.database import QuestionnairesDataBase, UsersDataBase
from questionnaires_service.src.config import db_data


@dataclass(frozen=True)
class DBEntities:
    users_db: Final[UsersDataBase] = UsersDataBase(db_data)
    questionnaires_db: Final[QuestionnairesDataBase] = QuestionnairesDataBase(db_data)