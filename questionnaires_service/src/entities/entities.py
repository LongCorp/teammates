from dataclasses import dataclass

from questionnaires_service.src.database.database import QuestionnairesDataBase, UsersDataBase
from questionnaires_service.src.config import db_data


@dataclass(frozen=True)
class DBEntities:
    users_db: UsersDataBase = UsersDataBase(db_data)
    questionnaires_db: QuestionnairesDataBase = QuestionnairesDataBase(db_data)
