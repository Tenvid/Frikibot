"""
Script made by David Gómez.

This module makes a request to PokeAPI and uses its info to generate
a random Pokémon.
"""

import json
import logging
from secrets import randbelow
from typing import Any

import discord
import requests
from discord.ext import commands

from frikibot.database_handler import create_pokemon
from frikibot.pokemon import Pokemon
from frikibot.stats import Stats

bot = commands.Bot(command_prefix="-", intents=discord.flags.Intents().all())

MAX_INDEX = 1010

TIMEOUT = 10

logging.basicConfig(level="INFO", format="%(name)s-%(levelname)s-%(message)s")
logger = logging.getLogger(name="PkGenerator")

NAME_REPLACEMENTS = {
    "gmax": "gigantamax",
    "alola": "alolan",
    "hisui": "hisuian",
    "paldea": "paldean",
    "galar": "galarian",
}


def get_stats_string(
    pokemon_name: str, decreased: str | None, increased: str | None
) -> str:
    """
    Return the ansi string of the stats of the Pokémon.

    Args:
    ----
        pokemon_name (str): Name of the Pokémon
        decreased (str): Decreased stat
        increased (str): Increased stat

    Returns:
    -------
        str: String of the stats in ansi format

    """
    stats = get_pokemon_stats(pokemon_name, decreased, increased)

    return "```ansi\n" + str(stats) + "```"


def get_pokemon_stats(
    name: str, decreased_stat: str | None, increased_stat: str | None
) -> Stats:
    """
    Get the stats of the Pokémon and return it in a dict.

    Args:
    ----
        name (str): Name of the Pokémon
        decreased_stat (str): Name of the stat whose value is decreased by nature
        increased_stat (str): Name of the stat whose value is increased by nature

    Returns:
    -------
        Stats: Stats of the pokemon

    """
    pokemon_data_response = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{name.replace('-gmax', '')}",
        timeout=TIMEOUT,
    )

    stats = json.loads(pokemon_data_response.text)["stats"]

    stat_values = []
    for stat in stats:
        stat_values.append(stat["base_stat"])

    return Stats(
        stat_values[0],
        stat_values[1],
        stat_values[2],
        stat_values[3],
        stat_values[4],
        stat_values[5],
        decreased_stat,
        increased_stat,
    )


def get_moves_string(name: str) -> str:
    """
    Generate string with the moves of the Pokémon from the possible ones.

    Args:
    ----
        name (str): Pokémon name

    Returns:
    -------
        str: String with moves in a list form

    """
    moves = get_pokemon_moves(name)

    ret = "```\n"

    for move in moves:
        ret += f"{move}"
        if move == moves[-1]:
            break
        ret += "\n"

    ret += "```"

    logger.info(f"Moves: {', '.join(moves)}")
    return ret


def eliminate_invalid_forms(varieties: list[dict[Any, Any]]) -> str:
    """
    Pick a random variety and correct name to get Pokémon image.

    Args:
    ----
        varieties (Dict): List of different forms of the Pokémon

    Returns:
    -------
        str: Pokémon name with the correct format

    """
    variety = varieties[randbelow(len(varieties))]

    ret_name = str(variety["pokemon"]["name"])

    return correct_name(ret_name, varieties, variety)


def correct_name(
    name: str,
    varieties: list[dict[Any, Any]],
    variety: dict[Any, Any],
) -> str:
    """
    Fix Pokémon names that cause error getting image url and re-format Pokémon name.

    Args:
    ----
        name (str): Name of the Pokémon
        varieties (List[Dict]): All Pokémon varieties
        variety (Dict): Picked variety

    Returns:
    -------
        str: Pokémon name with the correct format

    """
    if "pikachu" in name:
        if 1 <= varieties.index(variety) <= 6 or varieties.index(variety) == 14:
            return eliminate_invalid_forms(varieties)

    if "minior" in name:
        if "meteor" in name:
            name = "minior-meteor"

        else:
            name += "-core"

    name = correct_suffixes(name)

    return name


def correct_suffixes(name: str) -> str:
    """
    Replace all possible suffixes in Pokémon name.

    Args:
    ----
        name (str): Pokémon name

    Returns:
    -------
        str: Pokémon name with correct suffixes

    """
    for rep in NAME_REPLACEMENTS:
        name = name.replace(rep, NAME_REPLACEMENTS[rep])

    return name


def get_random_move(moves: list[dict[Any, Any]]) -> str:
    """
    Get a random move from all the available.

    Args:
    ----
        moves (List[Dict]): All possible moves

    Returns:
    -------
        str: Random selected move name

    """
    return str(
        moves[randbelow(len(moves))]["move"]["name"].replace("-", " ").capitalize(),
    )


def get_pokemon_moves(name: str) -> list[str]:
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

    try:
        name = name.replace("-gmax", "")

        url = f"https://pokeapi.co/api/v2/pokemon/{name}"

        response = requests.get(url, timeout=TIMEOUT)

        jres = json.loads(response.text)

        moves = jres["moves"]

        while len(ret) < 4:
            move = get_random_move(moves)

            if move not in ret:
                ret.append(move)

    except IndexError:
        # TODO: Handle this exception in upper levels
        pass
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
    color = "shiny" if randbelow(101) <= 10 else "normal"

    embed = build_embed(color, ctx)

    message = get_message(color, ctx)

    return embed, message


def get_message(colour: str, ctx: commands.Context[Any]) -> str:
    """
    Return Discord message content depending if Pokémon is shiny or not.

    Args:
    ----
        colour (str): Pokémon color ['normal', 'shiny']
        ctx (commands.Context): Discord command context

    Returns:
    -------
        str: Message content

    """
    message = f"{ctx.author.mention} Here you have your Pokémon"

    if colour == "shiny":
        message = message.replace("Pokémon", "✨SHINY✨ Pokémon")
    return message


def get_changed_stats(nature: dict[Any, Any]) -> tuple[str | None, str | None]:
    """
    Get two stats which are modified by selected nature.

    Args:
    ----
        nature (Dict): Chosen nature

    Returns:
    -------
        Tuple[str | None, str | None]: Decreased and increased stat
            None if neutral nature

    """
    try:
        decreased = nature["decreased_stat"]["name"]
        increased = nature["increased_stat"]["name"]

    except TypeError:
        decreased = None
        increased = None

    logger.info(f"Decreased stat: {decreased}")
    logger.info(f"Increased stat: {increased}")

    return decreased, increased


def get_nature() -> dict[Any, Any]:
    """
    Get a random nature.

    Returns
    -------
        Dict: Nature object

    """
    natures = dict(
        json.loads(
            requests.get("https://pokeapi.co/api/v2/nature", timeout=TIMEOUT).text,
        ),
    )

    nature = pick_nature(natures)

    logger.info(f"Nature: {nature['name']}")
    return nature


def pick_nature(natures: dict[Any, Any]) -> dict[Any, Any]:
    """
    Get a random nature and return its json.

    Args:
    ----
        natures (dict[Any, Any]): All possible natures

    Returns:
    -------
        Dict: Nature object

    """
    random_nature = natures["results"][randbelow(len(natures["results"]))]
    detailed_nature = requests.get(random_nature["url"], timeout=TIMEOUT)

    return dict(json.loads(detailed_nature.text))


def generate_pokemon_types(variety: dict[Any, Any]) -> list[dict[Any, Any]] | None:
    """
    Get types of a given Pokémon variety.

    Args:
    ----
        variety (dict): Pokémon data dict

    Returns:
    -------
        list | None: List of types, None if error

    """
    try:
        text_response = requests.get(variety["pokemon"]["url"], timeout=TIMEOUT).text
        return list[dict[Any, Any]](json.loads(text_response)["types"])

    except KeyError:
        logger.error("Types could not be obtained.")
        return None


def build_embed(color: str, ctx: commands.Context[Any]) -> discord.Embed:
    """
    Create an Embed from Discord.

    Args:
    ----
        color (str): Color of the Pokémon [Normal, Shiny]
        ctx (discord.ext.commands.Context): Temporary way to pass author code

    Returns:
    -------
        discord.Embed: Formatted embed object

    """
    pokemon_index = randbelow(MAX_INDEX - 1) + 1

    json_response = json.loads(
        requests.get(
            f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_index}",
            timeout=TIMEOUT,
        ).text
    )

    varieties: list[Any] = json_response["varieties"]

    variety = varieties[randbelow(len(varieties))]

    pokemon_name = variety["pokemon"]["name"]

    nature = get_nature()

    decreased, increased = get_changed_stats(nature)

    ret = discord.Embed()

    ret.set_image(
        url=f"https://img.pokemondb.net/sprites/home/{color}/"
        f"{correct_name(pokemon_name, varieties=varieties, variety=variety)}.png",
    )

    moves_string = get_moves_string(pokemon_name)

    # Pokemon Moves

    ret.add_field(name="Moves", value=moves_string)

    stats_string = get_stats_string(pokemon_name, decreased, increased)

    # Pokemon Stats

    ret.add_field(name="Stats", value=stats_string)

    # Pokémon name

    ret.title = (
        f"# {pokemon_index} *{nature['name'].capitalize()}* {pokemon_name.capitalize()}"
    )

    types = generate_pokemon_types(variety)

    create_pokemon(
        Pokemon(
            name=pokemon_name,
            list_index=pokemon_index,
            moves_list=moves_string.replace("```", "").split("\n"),
            nature=nature["name"],
            first_type=types[0]["type"]["name"] if types else "none",
            second_type=types[1]["type"]["name"] if types and len(types) > 1 else "none",
            author_code=str(ctx.author.id),
        ),
    )

    logger.info(msg="Embed title set")

    return ret
