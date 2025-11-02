"""
Script made by David Gómez.

This module contains a class for Pokémon entities
"""

from logging import getLogger
from secrets import randbelow

from frikibot.entities.nature import Nature
from frikibot.stats import Stats

logger = getLogger("Pokemon")


class Pokemon:
        """Pokémon definition."""

        def __init__(
                self,
                *,
                name: str,
                list_index: int,
                nature: Nature,
                first_type: str,
                second_type: str | None,
                author_code: str,
                available_abilities: list[dict],
                available_moves: list[dict],
                stats: Stats,
                sprite: str | None,
        ):
                """
                Create Pokémon instance.

                Args:
                ----
                    name (str): Pokémon name
                    list_index (int): Pokémon number in list
                    nature (Nature): Pokémon nature
                    first_type (str): Primary type
                    second_type (str | None): Secondary type if there is
                    author_code (str): Trainer id
                    available_abilities (list[dict]): List of Pokémon available abilities
                    available_moves (list[dict]): List of available moves
                    stats (Stats): Pokémon stats
                    sprite (str | None): Url of the sprite

                """
                logger.debug("Pokemon initalization started.")
                self.name = name
                logger.debug("Pokemon name set")
                self.pokedex_number = list_index
                logger.debug("Pokemon pokedex_number set")
                self.nature = nature
                logger.debug("Pokemon nature set")
                try:
                        self.nature_name = nature.name
                        logger.debug("Pokemon nature_name set")
                except KeyError:
                        self.nature_name = "Unknown nature"
                        logger.warning(
                                "Nature name could not be obtained from given nature: %s",
                                nature,
                        )
                self.first_type = first_type
                logger.debug("Pokemon first_type set")
                self.second_type = second_type
                logger.debug("Pokemon second_type set")
                self.author_code = author_code
                logger.debug("Pokemon author_code set")
                self.moves_list = self._get_pokemon_moves(available_moves)
                logger.debug("Pokemon moves_list set")
                self.ability = self._get_random_ability(available_abilities)
                logger.debug("Pokemon ability set")
                self.sprite = sprite

                self.stats = stats

        def _get_pokemon_moves(self, available_moves: list[dict]) -> list[str]:
                """
                Generate four random moves from the possible ones of the Pokémon to learn.

                Args:
                ----
                    available_moves (list[dict): List of all moves which this Pokémon can learn.

                Returns:
                -------
                    List[str]: List of Pokémon moves

                """
                ret: list = []
                while len(ret) < 4:
                        move = available_moves[randbelow(len(available_moves))]["move"]["name"]

                        if move not in ret:
                                ret.append(move)
                return ret

        def _get_random_ability(self, abilities_list) -> dict:
                """
                Pick a random ability from the availables.

                Args:
                ----
                    abilities_list (list[dict]): List of available abilities

                Returns:
                -------
                    dict: Chosen ability

                """
                return abilities_list[randbelow(len(abilities_list))]["ability"]["name"]
