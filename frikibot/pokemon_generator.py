import json
import logging
import random
from typing import Dict, List, Optional, Tuple

import discord
import discord.ext
import discord.ext.commands
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix="-", intents=discord.flags.Intents().all())

MIN_INDEX = 1
MAX_INDEX = 1010

logger = logging.Logger(name="logger", level=0)

NAME_REPLACEMENTS = {
    "gmax": "gigantamax",
    "alola": "alolan",
    "hisui": "hisuian",
    "paldea": "paldean",
    "galar": "galarian",
}


def get_stats_string(name: str, decreased: str, increased: str) -> str:
    """Return the ansi string of the stats of the Pokémon

    Args:
        name (str): Name of the Pokémon
        decreased (str): Decreased stat
        increased (str): Increased stat

    Returns:
        str: String of the stats in ansi format
    """

    stats = get_pokemon_stats(name)

    logging.info("Stats generated")

    ret = "```ansi\n"

    if decreased is None and increased is None:
        # Neutral nature -> No color in texts
        for stat in stats:
            actual_stat = stats[stat]
            ret += f"{stat}: {actual_stat}\n"

    else:
        # Non-neutral nature -> Red to increased, Blue to decreased
        for stat in stats:
            actual_stat = stats[stat]
            if stat == decreased:
                ret += f"\u001b[0;34m{stat}: {actual_stat} -\u001b[0;0m\n"
            elif stat == increased:
                ret += f"\u001b[0;31m{stat}: {actual_stat} +\u001b[0;0m\n"
            else:
                ret += f"{stat}: {actual_stat}\n"

    ret += "```"
    return ret


def get_pokemon_stats(name: str) -> Dict[str, int]:
    """Get the stats of the Pokémon and return it in a dict

    Args:
        name (str): Name of the Pokémon

    Returns:
        Dict[str, int]: stats of the pokemon
    """

    ret = {
        "Hp": 0,
        "Attack": 0,
        "Defense": 0,
        "Special attack": 0,
        "Special defense": 0,
        "Speed": 0,
    }

    response_bis = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{name.replace('-gmax', '')}"
    )

    stats = json.loads(response_bis.text)["stats"]

    stat_values = []
    for stat in stats:
        stat_values.append(stat["base_stat"])

    ret["Hp"] = stat_values[0]
    ret["Attack"] = stat_values[1]
    ret["Defense"] = stat_values[2]
    ret["Special attack"] = stat_values[3]
    ret["Special defense"] = stat_values[4]
    ret["Speed"] = stat_values[5]

    logging.info(f"Stats: {ret}")

    return ret


def get_moves_string(name: str) -> str:
    """Generate string with the moves of the Pokémon from
    the possible ones

    Args:
        name (str): Pokémon name

    Returns:
        str: String with moves in a list form
    """

    moves = get_pokemon_moves(name)
    ret = "```"
    for move in moves:
        ret += f"{move.strip()}"
        if move == moves[-1]:
            break
        ret += "\n"
    ret += "```"

    logging.info(f"Moves: {moves}")
    return ret


def eliminate_invalid_forms(varieties: List[Dict]) -> str:
    """Pick a random variety and correct name to get Pokémon image

    Args:
        varieties (Dict): List of different forms of the Pokémon

    Returns:
        str: Pokémon name with the correct format
    """

    variety = random.choice(varieties)
    ret_name = str(variety["pokemon"]["name"])
    return correct_name(ret_name, varieties, variety)


def correct_name(name: str, varieties: List[Dict], variety: Dict) -> str:
    """Check all the possible cases where name causes error getting image url
    and re-format Pokémon name

    Args:
        name (str): Name of the Pokémon
        varieties (List[Dict]): All Pokémon varieties
        variety (Dict): Picked variety

    Returns:
        str: Pokémon name with the correct format
    """

    if "pikachu" in name:
        if 1 <= varieties.index(variety) <= 6 or varieties.index(variety) == 14:
            return eliminate_invalid_forms(
                varieties
            )  # Select another variety. // TODO: Improve this to avoid possible infinite loop

    if "minior" in name:
        if "meteor" in name:
            name = "minior-meteor"

        else:
            name += "-core"

    name = correct_suffixes(name)

    return name


def correct_suffixes(name: str) -> str:
    """Replace all possible suffixes in Pokémon name

    Args:
        name (str): Pokémon name

    Returns:
        str: Pokémon name with correct suffixes
    """

    for rep in NAME_REPLACEMENTS:
        name = name.replace(rep, NAME_REPLACEMENTS[rep])

    return name


def get_random_move(moves: str) -> str:
    """Get a random move from all the available

    Args:
        moves (str): All possible moves

    Returns:
        str: Random selected move name
    """

    return (
        moves[random.randint(0, len(moves) - 1)]["move"]["name"]
        .replace("-", " ")
        .capitalize()
    )


def get_pokemon_moves(name: str) -> List[str]:
    """Generate four random moves from the possible ones of the Pokémon to learn

    Args:
        name (str): Pokémon name

    Returns:
        List[str]: List of Pokémon moves
    """

    ret = []
    name = name.replace("-gmax", "")
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    jres = json.loads(response.text)
    moves = jres["moves"]
    while True:
        move = get_random_move(moves)
        if move not in ret:
            ret.append(move)
        if len(ret) > 3:
            break
    return ret


def generate_random_pokemon(
    ctx: discord.ext.commands.Context,
) -> Tuple[discord.Embed, str]:
    """Generate a random Pokémon with stats, moves and nature and return
    a message with an embed object

    Args:
        ctx (discord.ext.commands.Context): Context of the command

    Returns:
        Tuple[discord.Embed, str]: Discord embed and message text
    """

    color = "shiny" if random.randint(1, 100) <= 10 else "normal"

    embed = build_embed(color)

    message = get_message(color, ctx)

    return embed, message


def get_message(colour: str, ctx: discord.ext.commands.Context) -> str:
    """Return Discord message content depending if Pokémon is shiny or not

    Args:
        colour (str): Pokémon color ['normal', 'shiny']
        ctx (discord.ext.commands.Context): Discord command context

    Returns:
        str: Message content
    """

    message = f"{ctx.author.mention} Here you have your Pokémon"
    if colour == "shiny":
        message = message.replace("Pokémon", "✨SHINY✨ Pokémon")
    return message


def get_changed_stats(nature: Dict) -> Tuple[Optional[str], Optional[str]]:
    """Get two stats which are modified by selected nature if there are

    Args:
        nature (Dict): Chosen nature

    Returns:
        Tuple[Optional[str], Optional[str]]: Decreased and increased stat, None if neutral nature
    """

    try:
        decreased = nature["decreased_stat"]["name"].replace("-", " ")
        increased = nature["increased_stat"]["name"].replace("-", " ")
    except TypeError:
        decreased = None
        increased = None

    # TODO: Check try-except clause and replace with if-else

    logging.info(f"Decreased stat: {decreased}")
    logging.info(f"Increased stat: {increased}")

    if decreased is not None and increased is not None:
        decreased = decreased.capitalize()
        increased = increased.capitalize()
        logging.info(f"Modified stats: +{increased} -{decreased}")

    return decreased, increased


def load_pokemon(response: requests.Response) -> Dict:
    """Serialize response plain text to a dict

    Args:
        response (requests.Response): Response from HTTP request

    Returns:
        Dict: Response as dict
    """

    poke = json.loads(response.text)
    logging.info(msg=f"\nPokemon response: {poke['name']}")
    return poke


def get_nature() -> Dict:
    """Get a random nature

    Returns:
        Dict: Nature object
    """

    natures: List = json.loads(requests.get("https://pokeapi.co/api/v2/nature").text)
    nature = pick_nature(natures)
    logging.info(f"Nature: {nature['name']}")
    return nature


def pick_nature(natures: List) -> Dict:
    """Get a random nature and return its json

    Args:
        natures (List): All possible natures

    Returns:
        Dict: Nature object
    """

    random_nature = random.choice(natures["results"])
    detailed_nature = requests.get(random_nature["url"])
    return json.loads(detailed_nature.text)


def build_embed(color: str) -> discord.Embed:
    """Create an Embed from Discord

    Args:
        color (str): Color of the Pokémon [Normal, Shiny]

    Returns:
        discord.Embed: Formatted embed object
    """

    pokemon_index = random.randint(MIN_INDEX, MAX_INDEX)

    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_index}"

    response = requests.get(url)

    varieties: List = json.loads(response.text)["varieties"]

    variety = random.choice(varieties)

    pokemon_name = variety["pokemon"]["name"]

    nature = get_nature()

    decreased, increased = get_changed_stats(nature)

    ret = discord.Embed()

    ret.set_image(
        url=f"https://img.pokemondb.net/sprites/home/{color}/{correct_name(pokemon_name, varieties=varieties, variety=variety)}.png"
    )

    # Pokemon Moves
    ret.add_field(name="Moves", value=get_moves_string(pokemon_name))

    # Pokemon Stats
    ret.add_field(
        name="Stats", value=get_stats_string(pokemon_name, decreased, increased)
    )

    # Pokémon name
    ret.title = (
        f"# {pokemon_index} *{nature['name'].capitalize()}* {pokemon_name.capitalize()}"
    )
    logger.info(msg="Embed title set")

    logging.info("Embed built")

    return ret
