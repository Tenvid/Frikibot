"""
Script made by David Gómez.

This module makes a request to PokeAPI and uses its info to generate
a random Pokémon.
"""

import logging
from secrets import randbelow
from typing import Any

import discord
import requests
from discord.ext import commands

from frikibot.database_handler import create_pokemon
from frikibot.global_variables import MAX_INDEX, TIMEOUT
from frikibot.pokemon import Pokemon
from frikibot.variety_data import VarietyData

logging.basicConfig(
    level="INFO", format="%(name)s - (%(levelname)s) -  [%(lineno)d] - %(message)s"
)
logger = logging.getLogger(name="PkGenerator")


def _get_natures_list() -> list[dict[str, str]] | None:
    try:
        response = requests.get(
            "https://pokeapi.co/api/v2/nature?limit=25", timeout=TIMEOUT
        )
        if response.status_code == 200:
            return response.json()["results"]
    except requests.ConnectionError as exc:
        logger.error("There was an error obtaining the natures: %s", exc)
    return None


def _fetch_random_nature() -> dict:
    if NATURES is None:
        return {}

    nature = NATURES[randbelow(len(NATURES))]["url"]
    try:
        if NATURES:
            response = requests.get(nature, timeout=TIMEOUT)
            if response.status_code == 200:
                return response.json()
    except requests.ConnectionError as exc:
        logger.error("There was an error trying to get the nature: %s \n ", nature, exc)
    return {}


NATURES = _get_natures_list()


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

    logger.info("Moves: ", ", ".join(moves_list))
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


def get_varieties(pokemon_index: int) -> list[Any]:
    """
    Request varietites of a Pokémon.

    Args:
    ----
        pokemon_index: Pokédex number of the Pokémon

    Returns:
    -------
        list[Any]: List of varieties

    Raises:
    ------
        requests.ConnectionError: When status_code is not 200 or an error
        requests.Timeout: When connection exceeds timeout

    """
    try:
        response = requests.get(
            f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_index}",
            timeout=TIMEOUT,
        )
        if response.status_code != 200:
            logger.error("Status code unexpected for index (%s)", pokemon_index)
            raise requests.exceptions.ConnectionError
        return response.json()["varieties"]
    except requests.Timeout as exc:
        logger.error("Timeout error happened trying to get the varieties: %s", exc)
        raise exc

    except requests.ConnectionError as exc:
        logger.error("Connection exception trying to get Pokémon varieties: %s", exc)
        raise exc


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

    try:
        varieties = get_varieties(pokemon_index)
    except (requests.ConnectionError, requests.Timeout):
        return discord.Embed(title="Error generating Pokémon data")

    variety = varieties[randbelow(len(varieties))]
    detailed_variety = requests.get(variety["pokemon"]["url"], timeout=TIMEOUT).json()

    data = VarietyData(
        available_abilities=detailed_variety["abilities"],
        available_moves=detailed_variety["moves"],
        combat_stats=detailed_variety["stats"],
        name=detailed_variety["name"],
        sprite=detailed_variety["sprites"]["other"]["home"][f"front_{color}"],
        types=detailed_variety["types"],
    )

    logger.info("VarietyData created")

    pokemon_entity = Pokemon(
        name=data.name,
        list_index=pokemon_index,
        author_code=str(ctx.author.id),
        nature=_fetch_random_nature(),
        first_type=data.types[0]["type"]["name"],
        second_type=data.types[1]["type"]["name"] if len(data.types) > 1 else "none",
        available_moves=data.available_moves,
        available_abilities=data.available_abilities,
        stats_data=data.combat_stats,
    )

    logger.info("Pokemon created")

    embed = _generate_embed(
        pokemon_entity.pokedex_number,
        pokemon_entity.name,
        pokemon_entity.nature,
        get_moves_string(pokemon_entity.moves_list),
        str(pokemon_entity.stats),
        pokemon_entity.ability,
        data.sprite,
    )

    create_pokemon(pokemon_entity)
    logger.info("Pokemon added to database")
    return embed


def _generate_embed(
    pokemon_index,
    pokemon_name,
    nature,
    moves_string,
    stats_string,
    ability,
    sprite,
):
    embed = (
        discord.Embed(
            title=f"# {pokemon_index}"
            f" *{nature['name'].capitalize() if nature else 'Hardy'}*"
            f" {pokemon_name.capitalize()}",
            description=f"Ability: {ability.replace('-', ' ').capitalize()}",
        )
        .set_image(url=sprite)
        .add_field(name="Moves", value=moves_string)
        .add_field(name="Stats", value=stats_string)
    )

    if sprite is None:
        embed.add_field(
            name="Unexpected Sprite",
            inline=False,
            value="There is no sprite. That means that this case should not happen."
            "Please, contact me on GitHub(@Tenvid) so I can fix this. Thank you :)",
        )
    return embed
