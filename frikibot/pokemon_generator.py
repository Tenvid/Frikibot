"""
Script made by David Gómez.

This module makes a request to PokeAPI and uses its info to generate
a random Pokémon.
"""

import enum
import logging
from secrets import randbelow
from typing import Any

from discord.ext import commands

from frikibot.controller.pokeapi_controller import PokeAPIController
from frikibot.global_variables import MAX_INDEX
from frikibot.pokemon import Pokemon
from frikibot.stats import Stats


class RequestTypes(enum.StrEnum):
        """
        Types of requests.

        Each type refers to the "intention" of the request.
        (i.e: If there is a request to get all the varieties, its type should be 'VARIETIES')
        """

        VARIETIES = "VARIETIES"
        DETAILED_VARIETY = "DETAILED_VARIETY"
        NATURES_LIST = "NATURES_LIST"
        RANDOM_NATURE = "RANDOM_NATURE"


logger = logging.getLogger(name="PkGenerator")

pokeapi_controller = PokeAPIController()


def generate_random_pokemon(
        ctx: commands.Context[Any],
        color: str,
):
        """
        Generate a random Pokémon and return a message with an embed object.

        Args:
        ----
            ctx (commands.Context): Context of the command
            color (str): Representation of pokémon color. Shiny or normal

        Returns:
        -------
            Tuple[discord.Embed, str]: Discord embed and message text

        """
        pokemon_index = randbelow(MAX_INDEX - 1) + 1

        varieties = pokeapi_controller.fetch_pokemon_varieties(pokemon_index)
        detailed_variety = pokeapi_controller.fetch_variety_details(varieties[randbelow(len(varieties))])

        logger.info("VarietyData created")

        nature = pokeapi_controller.fetch_random_nature()

        logger.info("Nature created: %s", nature)

        pokemon_stats = Stats(detailed_variety.combat_stats, nature.decreased, nature.increased)

        return Pokemon(
                name=detailed_variety.name,
                list_index=pokemon_index,
                author_code=str(ctx.author.id),
                nature=nature,
                first_type=detailed_variety.types[0]["type"]["name"],
                second_type=detailed_variety.types[1]["type"]["name"] if len(detailed_variety.types) > 1 else "none",
                available_moves=detailed_variety.available_moves,
                available_abilities=detailed_variety.available_abilities,
                stats=pokemon_stats,
                sprite=detailed_variety.get_official_artwork_sprite(color),
        )
