"""
Script made by David Gómez.

This module contains CRUD for Trainers and Pokémon.
"""

import os
import sqlite3
from typing import Any

from dotenv import load_dotenv

from frikibot.pokemon import Pokemon

load_dotenv()

POKEMON_TABLE = os.getenv("POKEMON_TABLE")
TRAINER_TABLE = os.getenv("TRAINER_TABLE")
DATABASE = os.getenv("DATABASE")


class NonExistingElementError(Exception):
    """Raise when an element is missing."""

    pass


def create_trainer(trainer_name: str, trainer_code: str) -> None:
    """
    Insert trainer in database.

    Args:
    ----
        trainer_name (str): _description_
        trainer_code (str): _description_

    Raises:
    ------
        NonExistingElementError: _description_
        NonExistingElementError: _description_

    """
    if not DATABASE:
        raise NonExistingElementError()
    if not TRAINER_TABLE:
        raise NonExistingElementError()

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
    Get data of a trainer by its code.

    Args:
    ----
        trainer_code (str): _description_

    Raises:
    ------
        NonExistingElementError: _description_
        NonExistingElementError: _description_

    Returns:
    -------
        _type_: _description_

    """
    if not DATABASE:
        raise NonExistingElementError()
    if not TRAINER_TABLE:
        raise NonExistingElementError()

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


def update_trainer(trainer_code: str, trainer_name: str) -> None:
    """
    Update trainer data by its code.

    Args:
    ----
        trainer_code (str): _description_
        trainer_name (str): _description_

    Raises:
    ------
        NonExistingElementError: _description_
        NonExistingElementError: _description_

    """
    if not DATABASE:
        raise NonExistingElementError()
    if not TRAINER_TABLE:
        raise NonExistingElementError()

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
        UPDATE {TRAINER_TABLE}
            SET trainer_name = ?,
                enabled = 1
            WHERE trainer_code = '?'
        """,  # noqa: S608 - Ignored because user cannot insert values to make SQL Injection and I want the possibility to change table name with .env
            (trainer_name, trainer_code),
        )
    cursor.fetchall()


def delete_trainer(trainer_code: str) -> None:
    """
    Disable a trainer.

    Args:
    ----
        trainer_code (str): _description_

    Raises:
    ------
        NonExistingElementException: _description_
        NonExistingElementException: _description_

    """
    if not DATABASE:
        raise NonExistingElementError()
    if not TRAINER_TABLE:
        raise NonExistingElementError()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {TRAINER_TABLE}
                SET 'enabled' = 0
            WHERE trainer_code = ?
            """,  # noqa: S608 - Ignored because user cannot insert values to make SQL Injection and I want the possibility to change table name with .env
            (trainer_code),
        )
        cursor.fetchall()


def create_pokemon(poke: Pokemon) -> None:
    """
    Insert a Pokémon in database.

    Args:
    ----
        poke (Pokemon): Generated Pokémon

    Raises:
    ------
        NonExistingElementException: Raise when DATABASE not in .env
        NonExistingElementException: Raise when POKEMON_TABLE not in .env

    """
    if not DATABASE:
        raise NonExistingElementError()
    if not POKEMON_TABLE:
        raise NonExistingElementError()

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
        """,
            (
                poke.name,
                poke.first_type,
                poke.second_type,
                poke.author_code,
                poke.moves_list[1],
                poke.moves_list[2],
                poke.moves_list[3],
                poke.moves_list[4],
                poke.nature,
            ),
        )
        conn.commit()
        print("Pokemon inserted")


def create_database():
    """
    Create tables for the database.

    Raises
    ------
        NonExistingElementError: Rise if there is no DATABASE in .env

    """
    if not DATABASE:
        raise NonExistingElementError()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
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
        conn.commit()
