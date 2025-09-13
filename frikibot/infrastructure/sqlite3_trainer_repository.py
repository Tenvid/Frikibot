"""SQLite3 implementation of the TrainerRepository."""

import sqlite3
from typing import Any

from frikibot.domain.trainer_repository import TrainerRepository
from frikibot.shared.constants import DATABASE, TRAINER_TABLE
from frikibot.shared.exceptions import NonExistingElementError


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

    def get_by_id(self, trainer_code: str) -> Any | None:
        """
        Get trainer from database by its ID.

        Args:
        ----
            trainer_code (str): Trainer ID.

        Raises:
        ------
            NonExistingElementError: Raises if no Trainer table is set.

        Returns:
        -------
            Any: Trainer with the given id.

        """
        if not TRAINER_TABLE:
            raise NonExistingElementError

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"""SELECT *
                        FROM {TRAINER_TABLE}
                        WHERE trainer_code = ? AND enabled = 1
                """,  # noqa: S608 - Ignored because user cannot insert values to make SQL Injection and I want the possibility to change table name with .env
                (trainer_code,),
            )
            return cursor.fetchone()
