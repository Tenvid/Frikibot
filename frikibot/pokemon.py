"""
Script made by David Gómez.

This module contains a class for Pokémon entities
"""

from discord import reaction
import requests

from frikibot.global_variables import TIMEOUT
from random import choice
from frikibot.move_fetcher import create_random_moves_list
from frikibot.stats import Stats


class Pokemon:
    """Pokémon definition."""

    def __init__(
        self,
        *,
        name: str,
        list_index: int,
        nature: dict,
        first_type: str,
        second_type: str | None,
        author_code: str,
        available_moves: list[dict],
        available_abilities: list[dict],
        stats_data: list[dict],
    ):
        """
        Create Pokémon instance.

        Args:
        ----
            name (str): Pokémon name
            list_index (int): Pokémon number in list
            moves_list (list): List of movements
            nature (str): Pokémon nature
            first_type (str): Primary type
            second_type (str): Secondary type if there is
            author_code (str): Trainer id

        """
        self.name = name
        self.pokedex_number = list_index
        self.nature = nature
        self.nature_name = nature["name"]
        self.first_type = first_type
        self.second_type = second_type
        self.author_code = author_code
        self.moves_list = self.get_pokemon_moves(available_moves)
        self.ability = self.get_random_ability(available_abilities)
        self.stats = Stats(stats_data, self.nature["decreased"], self.nature["increased"])

    # @classmethod
    # def from_tuple(cls: type["Pokemon"], pokemon_data: tuple) -> "Pokemon":
    #     """
    #     Generate Pokémon data using tuple data from database.
    #
    #     Args:
    #     ----
    #         pokemon_data (tuple): Pokémon data obtained from database.
    #
    #     Returns:
    #     -------
    #         Pokemon: Pokemon instance
    #
    #     """
    #     return cls(
    #         list_index=pokemon_data[0],
    #         name=pokemon_data[1],
    #         first_type=pokemon_data[2],
    #         second_type=pokemon_data[3],
    #         author_code=pokemon_data[4],
    #         nature=pokemon_data[9],
    #         available_moves=None,
    #     )
    #
    # def _get_random_moves_list(self):
    #     moves_string.replace("```", "").split("\n")
    #
    def get_pokemon_moves(self, available_moves: list[dict]) -> list[str]:
        """
        Generate four random moves from the possible ones of the Pokémon to learn.

        Args:
        ----
            name (str): Pokémon name

        Returns:
        -------
            List[str]: List of Pokémon moves

        """
        ret: list = []
        while len(ret) < 4:
            move = choice(available_moves)["move"]["name"]

            if move not in ret:
                ret.append(move)
        return ret

    def get_random_ability(self, abilities_list):
        return choice(abilities_list)["ability"]["name"]
