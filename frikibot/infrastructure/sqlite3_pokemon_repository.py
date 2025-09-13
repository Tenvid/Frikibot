"""SQLite3 implementation of PokemonRepository."""

import logging
import sqlite3

from frikibot.domain.pokemon import Pokemon
from frikibot.domain.pokemon_repository import PokemonRepository
from frikibot.shared.constants import DATABASE, POKEMON_TABLE
from frikibot.shared.exceptions import NonExistingElementError

logger = logging.getLogger(__name__)


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
            logger.error("No POKEMON_TABLE defined in .env")
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

    def get_by_trainer_id(self, trainer_code: str) -> list[Pokemon]:
        """
        Get all Pokémon owned by a trainer.

        Args:
        ----
            trainer_code (str): ID of the trainer.

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
