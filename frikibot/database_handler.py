"""
Script made by David Gómez.

This module contains CRUD for Trainers and Pokémon.
"""

import logging
import sqlite3
from logging import getLogger

from dotenv import load_dotenv

from frikibot.shared.constants import DATABASE, POKEMON_TABLE, TRAINER_TABLE

load_dotenv()
logger = getLogger("DB-Handler")

logger = logging.getLogger("Database")


def create_database():
    """Create tables for the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
        CREATE TABLE {TRAINER_TABLE} (
    trainer_ID   INTEGER PRIMARY KEY AUTOINCREMENT
                         NOT NULL,
    trainer_name TEXT    NOT NULL,
    trainer_code TEXT    UNIQUE
                         NOT NULL,
    enabled      INTEGER NOT NULL
                         REFERENCES enabled_state (value)
);
""")
        except sqlite3.OperationalError:
            logger.error("There was an error creating the %s table", TRAINER_TABLE)

        try:
            cursor.execute(f"""
        CREATE TABLE {POKEMON_TABLE} (
    ID         INTEGER PRIMARY KEY ON CONFLICT ROLLBACK AUTOINCREMENT
                       NOT NULL,
    Name       TEXT    NOT NULL,
    Tipo1      TEXT    NOT NULL,
    Tipo2      TEXT,
    Entrenador TEXT    NOT NULL
                       REFERENCES entrenador (trainer_code),
    Move1      TEXT    NOT NULL,
    Move2      TEXT    NOT NULL,
    Move3      TEXT    NOT NULL,
    Move4      TEXT    NOT NULL,
    Naturaleza TEXT    NOT NULL
);
""")
        except sqlite3.OperationalError:
            logger.error("There was an error creating %s table", POKEMON_TABLE)

        conn.commit()
