from dataclasses import dataclass

from questionnaires_service.src.database.database import QuestionnairesDataBase
from questionnaires_service.src.config import db_data


@dataclass(frozen=True)
class DBEntities:
    questionnaires_db: QuestionnairesDataBase = QuestionnairesDataBase(db_data)
