import random

import discord
from discord.ext import commands
import requests
import json
import logging
from typing import Dict

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


def get_stats_string(name, decreased, increased):
    stats = get_pokemon_stats(name)
    logging.info("Stats generated")
    ret = "```ansi\n"

    if decreased is None and increased is None:
        for stat in stats:
            actual_stat = stats[stat]
            ret += f"{stat}: {actual_stat}\n"
    else:
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


def get_pokemon_stats(name):
    ret = {
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

    ret["Attack"] = stat_values[0]
    ret["Defense"] = stat_values[1]
    ret["Special attack"] = stat_values[2]
    ret["Special defense"] = stat_values[3]
    ret["Speed"] = stat_values[4]

    logging.info(f"Stats: {ret}")

    return ret


def get_random_nature(natures):
    return random.choice(natures["results"])


def get_moves_string(name: str):
    moves = get_pokemon_moves(name)
    ret = "```\n"
    for move in moves:
        ret += f"\n {move} "
    ret += "```"

    logging.info(f"Moves: {moves}")
    return ret


def eliminate_invalid_forms(varieties):
    variety = random.choice(varieties)
    ret_name = str(variety["pokemon"]["name"])
    return correct_name(ret_name, varieties, variety)


def correct_name(ret_name: str, varieties: Dict, variety: Dict):
    if "pikachu" in ret_name:
        if 1 <= varieties.index(variety) <= 6 or varieties.index(variety) == 14:
            return eliminate_invalid_forms(varieties)

    if "minior" in ret_name:
        if "meteor" in ret_name:
            ret_name = "minior-meteor"
        else:
            ret_name += "-core"

    ret_name = correct_suffixes(ret_name)

    return ret_name


def correct_suffixes(name):
    for rep in NAME_REPLACEMENTS:
        name = name.replace(rep, NAME_REPLACEMENTS[rep])

    return name


def get_shiny_chance():
    index = random.randint(1, 100)
    if index <= 10:
        return "shiny"
    return "normal"


def generate_image_url(name):
    colour = get_shiny_chance()
    url = f"https://img.pokemondb.net/sprites/home/{colour}/{name}.png"
    return url, colour


def get_random_move(moves):
    return (
        moves[random.randint(0, len(moves) - 1)]["move"]["name"]
        .replace("-", " ")
        .capitalize()
    )


def get_pokemon_moves(name):
    ret = []
    try:
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
    except IndexError:
        pass
    return ret


def get_normal_or_shiny():
    return "shiny" if random.randint(1, 100) <= 10 else "normal"


def get_pokemon_variety(loaded_response: Dict):
    return random.choice(loaded_response["varieties"])


def generate_random_pokemon(ctx):
    color = get_normal_or_shiny()

    embed = build_embed(color)

    message = get_message(color, ctx)

    return embed, message


def get_message(colour, ctx):
    message = f"{ctx.author.mention} Here you have your Pokémon"
    if colour == "shiny":
        message = message.replace("Pokémon", "✨SHINY✨ Pokémon")
    return message


def get_changed_stats(nature):
    try:
        decreased = nature["decreased_stat"]["name"].replace("-", " ")
        increased = nature["increased_stat"]["name"].replace("-", " ")
    except TypeError:
        decreased = None
        increased = None

    logging.info(f"Decreased stat: {decreased}")
    logging.info(f"Increased stat: {increased}")

    if decreased is not None and increased is not None:
        decreased = decreased.capitalize()
        increased = increased.capitalize()
        logging.info(f"Modified stats: +{increased} -{decreased}")

    return decreased, increased


def get_pokemon_elements(response):
    poke = load_pokemon(response)

    variety = random.choice(poke["varieties"])

    name = variety["pokemon"]["name"]

    colour, sprite_url = get_sprite_color(name, poke["varieties"], variety)

    moves = get_moves_string(name)

    nature = get_nature()
    return colour, moves, name, nature, sprite_url


def get_sprite_color(name, varieties, variety):
    name = correct_name(name, varieties, variety)
    sprite_url, colour = generate_image_url(name)
    logging.info(msg=f"Sprite URL: {sprite_url}")
    logging.info(msg=f"Colour: {colour}")
    return colour, sprite_url


def validate_name(poke):
    name = eliminate_invalid_forms(poke["varieties"])
    logging.info(msg=f"NAME:{name}")
    return name


def load_pokemon(response):
    poke = json.loads(response.text)
    logging.info(msg=f"\nPokemon response: {poke['name']}")
    return poke


def get_nature():
    natures = json.loads(requests.get("https://pokeapi.co/api/v2/nature").text)
    nature = pick_nature(natures)
    logging.info(f"Nature: {nature['name']}")
    return nature


def pick_nature(natures):
    random_nature = get_random_nature(natures)
    detailed_nature = requests.get(random_nature["url"])
    loaded_detailed_nature = json.loads(detailed_nature.text)
    return loaded_detailed_nature


def build_embed(color: str):
    """
    Creates an Embed from Discord

    :param index: Pokédex number
    :param moves_string: Formatted string which contains the moves of the Pokémon
    :param stats_string: Formatted string which contains the stats of the Pokémon
    :param pokemon_name: Random generated name
    :param nature: Nature of the Pokémon
    :param sprite_url: URL of the sprite
    :return: Formatted embed
    """

    pokemon_index = random.randint(MIN_INDEX, MAX_INDEX)

    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_index}"

    response = requests.get(url)

    pokemon_name = get_pokemon_variety(json.loads(response.text))["pokemon"]["name"]

    nature = get_nature()

    decreased, increased = get_changed_stats(nature)

    ret = discord.Embed()

    ret.set_image(
        url=f"https://img.pokemondb.net/sprites/home/{color}/{pokemon_name}.png"
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
