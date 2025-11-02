"""
Script made by David Gómez.

This module makes a request to PokeAPI and uses its info to generate
a random Pokémon.
"""

import enum
import logging
from secrets import randbelow
from typing import Any

import discord
import requests
from discord.ext import commands

from frikibot.controller.pokeapi_controller import PokeAPIController
from frikibot.database_handler import create_pokemon
from frikibot.domain.discord_embed_builder import DiscordEmbedBuilder
from frikibot.global_variables import MAX_INDEX, TIMEOUT
from frikibot.pokemon import Pokemon


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


logging.basicConfig(level="INFO", format="%(name)s - (%(levelname)s) -  [%(lineno)d] - %(message)s")
logger = logging.getLogger(name="PkGenerator")

pokeapi_controller = PokeAPIController()

NATURES = pokeapi_controller.fetch_all_natures()


def _fetch_random_nature() -> dict:
        if NATURES is None:
                return {}

        nature_url = NATURES[randbelow(len(NATURES))]["url"]

        response = try_make_http_get(nature_url, RequestTypes.RANDOM_NATURE)

        if response is None:
                return {}
        return response.json()


def try_make_http_get(url: str, request_type: RequestTypes) -> requests.Response | None:
        """
        Make a HTTP GET request and return its result.

        Args:
        ----
            url(str): URL which will receive the request.
            request_type(RequestTypes): Type of request.

        Returns:
        -------
            requests.Response | None: Request result. None if error.

        """
        try:
                response = requests.get(url, timeout=TIMEOUT)
                if response.status_code == 200:
                        return response
                raise requests.ConnectionError(f"Status code not valid {response.status_code}")
        except requests.ConnectionError as exc:
                logger.error(
                        "Connection error happened when doing a request: %s | Type: %s",
                        exc,
                        request_type,
                )
        except requests.Timeout as exc:
                logger.error(
                        "Timeout error happened when doing a request: %s | Type: %s",
                        exc,
                        request_type,
                )
        return None


def get_moves_string(moves_list: list[str]) -> str:
        """
        Generate a string with the moves of the Pokémon from the possible ones.

        Args:
        ----
            moves_list (list[str]): List with raw names of moves

        Returns:
        -------
            str: String with moves in a list form

        """
        moves_list = [move.replace("-", " ").capitalize() for move in moves_list]
        ret = "```\n"

        for move in moves_list:
                ret += f"{move}"
                if move == moves_list[-1]:
                        break
                ret += "\n"

        ret += "```"

        logger.info("Moves: %s", ", ".join(moves_list))
        return ret


def generate_random_pokemon(
        ctx: commands.Context[Any],
) -> tuple[discord.Embed, str]:
        """
        Generate a random Pokémon and return a message with an embed object.

        Args:
        ----
            ctx (commands.Context): Context of the command

        Returns:
        -------
            Tuple[discord.Embed, str]: Discord embed and message text

        """
        color = "shiny" if randbelow(101) <= 10 else "default"
        embed = build_embed(color, ctx)

        message = get_message(color, ctx)

        return embed, message


def get_message(color: str, ctx: commands.Context[Any]) -> str:
        """
        Return Discord message content depending if Pokémon is shiny or not.

        Args:
        ----
            color (str): Pokémon color ['normal', 'shiny']
            ctx (commands.Context): Discord command context

        Returns:
        -------
            str: Message content

        """
        message = f"{ctx.author.mention} Here you have your Pokémon"

        if color == "shiny":
                message = message.replace("Pokémon", "✨SHINY✨ Pokémon")
        return message


def build_embed(color: str, ctx: commands.Context[Any]) -> discord.Embed:
        """
        Create embed message to display all data.

        Args:
        ----
            color (str): Color of the Pokémon [Normal, Shiny]
            ctx (discord.ext.commands.Context): Temporary way to pass author code

        Returns:
        -------
            discord.Embed | None: Formatted embed object

        """
        pokemon_index = randbelow(MAX_INDEX - 1) + 1
        varieties = pokeapi_controller.fetch_pokemon_varieties(pokemon_index)
        detailed_variety = pokeapi_controller.fetch_variety_details(varieties[randbelow(len(varieties))])

        logger.info("VarietyData created")

        pokemon_entity = Pokemon(
                name=detailed_variety.name,
                list_index=pokemon_index,
                author_code=str(ctx.author.id),
                nature=_fetch_random_nature(),
                first_type=detailed_variety.types[0]["type"]["name"],
                second_type=detailed_variety.types[1]["type"]["name"] if len(detailed_variety.types) > 1 else "none",
                available_moves=detailed_variety.available_moves,
                available_abilities=detailed_variety.available_abilities,
                stats_data=detailed_variety.combat_stats,
                sprite=detailed_variety.get_official_artwork_sprite(color),
        )

        logger.info("Pokemon created")

        embed = _generate_embed(pokemon_entity)

        create_pokemon(pokemon_entity)
        logger.info("Pokemon added to database")
        return embed


def _generate_embed(pokemon: Pokemon):
        embed = (
                DiscordEmbedBuilder()
                .with_title(f"# {pokemon.pokedex_number} *{pokemon.nature['name'].capitalize() if pokemon.nature else 'Hardy'}* {pokemon.name.capitalize()}")
                .with_description(f"Ability: {pokemon.ability.replace('-', ' ').capitalize()}")
                .with_image(pokemon.sprite)
                .with_field(name="Moves", value=get_moves_string(pokemon.moves_list))
                .with_field(name="Stats", value=str(pokemon.stats))
                .build()
        )

        if pokemon.sprite is None:
                embed.add_field(
                        name="Unexpected Sprite",
                        inline=False,
                        value="There is no sprite. That means that this case should not happen."
                        "Please, contact me on GitHub(@Tenvid) so I can fix this. Thank you :)",
                )
        return embed
