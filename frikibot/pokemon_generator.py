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
    pokemon_name: str, modified_stats: tuple[str | None, str | None]
) -> str:
    """
    Return the ansi string of the stats of the Pokémon.

    Args:
    ----
        pokemon_name (str): Name of the Pokémon
        modified_stats (tuple[str | None, str | None]): Tuple with modified stats names

    Returns:
    -------
        str: String of the stats in ansi format

    """
    stats = get_pokemon_stats(pokemon_name, modified_stats)

    return "```ansi\n" + str(stats) + "```"


def get_pokemon_stats(name: str, modified_stats: tuple[str | None, str | None]) -> Stats:
    """
    Get the stats of the Pokémon and return it in a dict.

    Args:
    ----
        name (str): Name of the Pokémon
        decreased_stat (str): Name of the stat whose value is decreased by nature
        modified_stats (tuple[str | None, str | None]): Tuple with modified stats names


    Returns:
    -------
        Stats: Stats of the pokemon

    """
    stats = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{name.replace('-gmax', '')}",
        timeout=TIMEOUT,
    ).json()["stats"]

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
        modified_stats[0],
        modified_stats[1],
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

    name = name.replace("-gmax", "")

    url = f"https://pokeapi.co/api/v2/pokemon/{name}"

    response = requests.get(url, timeout=TIMEOUT)

    json_response = response.json()

    moves = json_response["moves"]

    while len(ret) < 4:
        move = get_random_move(moves)

        if move not in ret:
            ret.append(move)
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


def get_changed_stats(nature: dict[Any, Any] | None) -> tuple[str | None, str | None]:
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
    if nature:
        try:
            decreased = nature["decreased_stat"]["name"]
            increased = nature["increased_stat"]["name"]
        except TypeError:
            decreased = None
            increased = None
    else:
        logger.info("Nature is none, so stats will not be modified")
        decreased = None
        increased = None

    logger.info(f"Decreased stat: {decreased}")
    logger.info(f"Increased stat: {increased}")

    return decreased, increased


def get_nature() -> dict[Any, Any] | None:
    """
    Get a random nature.

    Returns
    -------
        Dict: Nature object

    """
    try:
        natures = requests.get("https://pokeapi.co/api/v2/nature", timeout=TIMEOUT).json()
    except requests.ConnectionError:
        logger.error("Error trying to get natures list")
        return None

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

    return detailed_nature.json()


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
        response = requests.get(variety["pokemon"]["url"], timeout=TIMEOUT).json()
        return list[dict[Any, Any]](response["types"])

    except KeyError:
        logger.error("Types could not be obtained.")
        return None


def get_pokemon_ability(variety: dict) -> str:
    """
    Pick a nature from the available for the Pokémon.

    Args:
    ----
        variety (dict): Pokémon data

    Raises:
    ------
        TypeError: Raises if variety is not a dict

    Returns:
    -------
        str: Ability name

    """
    if not isinstance(variety, dict):
        raise TypeError(f"Variety is not a dict, is of type {type(variety)}")

    return variety["abilities"][randbelow(len(variety["abilities"]))]["ability"]["name"]


def build_embed(color: str, ctx: commands.Context[Any]) -> discord.Embed:
    """
    Create an Embed from Discord.

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
        varieties: list[Any] = requests.get(
            f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_index}",
            timeout=TIMEOUT,
        ).json()["varieties"]
    except requests.ConnectionError:
        logger.error("Timeout exception trying to get Pokémon varieties")
        return discord.Embed(title="Error generating Pokémon data")

    variety = varieties[randbelow(len(varieties))]

    pokemon_name = variety["pokemon"]["name"]

    ability = get_pokemon_ability(
        requests.get(variety["pokemon"]["url"], timeout=TIMEOUT).json()
    )

    nature = get_nature()

    moves_string = get_moves_string(pokemon_name)

    stats_string = (
        "```ansi\n"
        + str(get_pokemon_stats(pokemon_name, get_changed_stats(nature)))
        + "```"
    )

    embed = _generate_embed(
        color,
        pokemon_index,
        varieties,
        variety,
        pokemon_name,
        nature,
        moves_string,
        stats_string,
        ability,
    )

    types = generate_pokemon_types(variety)

    create_pokemon(
        Pokemon(
            name=pokemon_name,
            list_index=pokemon_index,
            moves_list=moves_string.replace("```", "").split("\n"),
            nature=nature["name"] if nature else "None",
            first_type=types[0]["type"]["name"] if types else "none",
            second_type=types[1]["type"]["name"] if types and len(types) > 1 else "none",
            author_code=str(ctx.author.id),
        ),
    )

    logger.info(msg="Embed title set")

    return embed


def _generate_embed(
    color,
    pokemon_index,
    varieties,
    variety,
    pokemon_name,
    nature,
    moves_string,
    stats_string,
    ability,
):
    ret = discord.Embed()

    ret.set_image(
        url=f"https://img.pokemondb.net/sprites/home/{color}/"
        f"{correct_name(pokemon_name, varieties=varieties, variety=variety)}.png",
    )

    # Pokemon Moves

    ret.add_field(name="Moves", value=moves_string)

    # Pokemon Stats

    ret.add_field(name="Stats", value=stats_string)

    # Pokémon name

    ret.title = (
        f"# {pokemon_index} *{nature['name'].capitalize() if nature else 'Hardy'}*"
        f" {pokemon_name.capitalize()}"
    )

    ret.description = f"Ability: {ability.replace('-', ' ').capitalize()}"

    return ret
