"""
Script made by David Gómez.

This module contains CRUD for Trainers and Pokémon.
"""

import logging
import os
import sqlite3
from logging import getLogger
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from frikibot.pokemon import Pokemon

load_dotenv()
logger = getLogger("DB-Handler")

logger = logging.getLogger("Database")

POKEMON_TABLE = os.getenv("POKEMON_TABLE")
TRAINER_TABLE = os.getenv("TRAINER_TABLE")
DATABASE_FOLDER: Path = Path(str(os.getenv("DATABASE_FOLDER")) if os.getenv("DATABASE_FOLDER") else "db")
DATABASE: Path = Path(DATABASE_FOLDER / str(os.getenv("DATABASE")) if os.getenv("DATABASE") else "pokemon.db")

if not DATABASE_FOLDER.exists():
    DATABASE_FOLDER.mkdir()


class NonExistingElementError(Exception):
    """Raise when an element is missing."""


def create_trainer(trainer_name: str, trainer_code: str) -> None:
    """
    Insert trainer in database.

    Args:
    ----
        trainer_name (str): Trainer name. Same as Discord username.
        trainer_code (str): Trainer primary key. Same as Discord inner id.

    Raises:
    ------
        NonExistingElementError: Raise if there is no trainer table set.

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


def read_trainer(trainer_code: str) -> Any | None:
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


def create_pokemon(poke: Pokemon) -> None:
    """
    Insert a Pokémon in database.

    Args:
    ----
        poke (Pokemon): Generated Pokémon

    Raises:
    ------
        NonExistingElementException: Raise when POKEMON_TABLE not in .env

    """
    if not POKEMON_TABLE:
        raise NonExistingElementError

    logger.debug(poke.name)
    logger.debug(poke.first_type)
    logger.debug(poke.second_type)
    logger.debug(poke.author_code)
    logger.debug(poke.moves_list)
    for move in poke.moves_list:
        logger.debug("Move: %s, type: %s", move, type(move))
    logger.debug(poke.nature_name)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
INSERT INTO {POKEMON_TABLE} (
                        Name,
                        Tipo1,
                        Tipo2,
                        Entrenador,
                        Move1,
                        Move2,
                        Move3,
                        Move4,
                        Naturaleza
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,  # noqa: S608
            (
                poke.name,
                poke.first_type,
                poke.second_type,
                poke.author_code,
                poke.moves_list[0],
                poke.moves_list[1],
                poke.moves_list[2],
                poke.moves_list[3],
                poke.nature_name,
            ),
        )
        conn.commit()
        logger.info("Pokemon inserted")


def read_pokemon_by_trainer(trainer_code: str) -> list[Pokemon]:
    """
    Get all Pokémon owned by a trainer.

    Args:
    ----
        trainer_code (str): ID of the trainer.

    Raises:
    ------
        NonExistingElementError: Raise when there is no database configured.

    Returns:
    -------
        list[Pokemon]: List of Pokémon instances.

    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
            SELECT ID,
                Name,
                Tipo1,
                Tipo2,
                Entrenador,
                Move1,
                Move2,
                Move3,
                Move4,
                Naturaleza
            FROM pokemon
            WHERE Entrenador = ?;
            """,
                (trainer_code,),
            )
            return cursor.fetchall()

        except sqlite3.Error as e:
            raise e


def create_database() -> None:
    """
    Create tables for the database.

    Raises
    ------
        NonExistingElementError: Rise if there is no DATABASE in .env

    """
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
