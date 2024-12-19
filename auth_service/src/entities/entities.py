from dataclasses import dataclass
from typing import Final

from src.database.database import UsersDataBase
from src.config import db_data


@dataclass(frozen=True)
class DBEntities:
    users_db: Final[UsersDataBase] = UsersDataBase(db_data)
