"""SQLite3 implementation of the TrainerRepository."""

import os
import sqlite3
from pathlib import Path

from frikibot.database_handler import NonExistingElementError
from frikibot.domain.trainer_repository import TrainerRepository

TRAINER_TABLE = os.getenv("TRAINER_TABLE")
DATABASE_FOLDER: Path = Path(
    str(os.getenv("DATABASE_FOLDER")) if os.getenv("DATABASE_FOLDER") else "db"
)
DATABASE: Path = Path(
    DATABASE_FOLDER / str(os.getenv("DATABASE"))
    if os.getenv("DATABASE")
    else "pokemon.db"
)

if not DATABASE_FOLDER.exists():
    DATABASE_FOLDER.mkdir()


class SQLite3TrainerRepository(TrainerRepository):
    """SQLite3 implementation of the TrainerRepository."""

    def add(self, trainer_name: str, trainer_code: str):
        """
        Add a new trainer to the repository.

        Args:
        ----
            trainer_name (str): Trainer name. Same as Discord username.
            trainer_code (str): Trainer primary key. Same as Discord inner id.

        """
        if not TRAINER_TABLE:
            raise NonExistingElementError

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {TRAINER_TABLE}"  # noqa: S608
                "(trainer_name, trainer_code, enabled) VALUES (?, ?, 1)",  # noqa: S608
                # Ignored because user cannot insert values to make SQL
                # Injection and I want the possibility to change table name with .env
                (trainer_name, trainer_code),
            )
            conn.commit()
