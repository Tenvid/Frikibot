"""SQLite3 implementation of PokemonRepository."""

import logging
import os
import sqlite3
from pathlib import Path

from domain.pokemon import Pokemon

from frikibot.database_handler import NonExistingElementError
from frikibot.domain.pokemon_repository import PokemonRepository

POKEMON_TABLE = os.getenv("POKEMON_TABLE")

logger = logging.getLogger(__name__)

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


class SQLite3PokemonRepository(PokemonRepository):
    """SQLite3 implementation of PokemonRepository."""

    def add(self, poke: Pokemon) -> None:
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
