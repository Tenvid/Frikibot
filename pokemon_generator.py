import random

import discord
from discord.ext import commands
import requests
import json
import logging

bot = commands.Bot(command_prefix="-", intents=discord.flags.Intents().all())

MIN_INDEX = 1
MAX_INDEX = 1010

logger = logging.Logger(name="logger", level=0)

NAME_REPLACEMENTS = {
    "gmax": "gigantamax",
    "alola": "alolan",
    "hisui": "hisuian",
    "paldea": "paldean",
    "galar": "galarian"
}

# name = name.replace("gmax", "gigantamax")
# name = name.replace("alola", "alolan")
# name = name.replace("hisui", "hisuian")
# name = name.replace("paldea", "paldean")
# name = name.replace("galar", "galarian")

def get_stats_string(name, decreased, increased):
    stats = get_pokemon_stats(name)
    ret = "```ansi\n"
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
        "Speed": 0
    }

    response_bis = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")

    load = json.loads(response_bis.text)

    stats = load['stats']

    stat_values = []
    for stat in stats:
        stat_values.append(stat['base_stat'])

    ret["Attack"] = stat_values[0]
    ret["Defense"] = stat_values[1]
    ret["Special attack"] = stat_values[2]
    ret["Special defense"] = stat_values[3]
    ret["Speed"] = stat_values[4]

    return ret


def get_random_nature(natures):
    return random.choice(natures['results'])


def get_moves_string(name: str):
    moves = get_pokemon_moves(name)
    ret = "```\n"
    for move in moves:
        ret += f"\n {move} "
    ret += "```"
    return ret


def eliminate_invalid_forms(varieties):
    variety = random.choice(varieties)
    ret_name = variety['pokemon']['name']

    if "pikachu" in ret_name:
        if 1 <= varieties.index(variety) <= 6 or varieties.index(variety) == 14:
            return eliminate_invalid_forms(varieties)

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


def generate_url(name):
    colour = get_shiny_chance()
    url = f"https://img.pokemondb.net/sprites/home/{colour}/{name}.png"
    return url, colour


def get_random_move(moves):
    return moves[random.randint(0, len(moves) - 1)]['move']['name'].capitalize()


def get_pokemon_moves(name):
    ret = []
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        jres = json.loads(response.text)
        moves = jres['moves']
        while True:
            move = get_random_move(moves)
            if move not in ret:
                ret.append(move)
            if len(ret) > 3:
                print(f"MOVES: {ret}")
                break
    except IndexError as e:
        print(f"MOVE ERROR: {e.args}")
        pass
    return ret


async def generate_random_pokemon(ctx):
    pokemon_index = await get_random_index()
    url = await get_url(pokemon_index)

    response = requests.get(url)

    colour, moves, name, nature, sprite_url = await get_pokemon_elements(response)

    decreased, increased = await get_changed_stats(nature)

    stats_string = get_stats_string(name, decreased, increased)

    embed = build_embed(moves, stats_string, name,
                        nature, sprite_url)

    message = await get_message(colour, ctx)

    return embed, message


async def get_message(colour, ctx):
    message = f"{ctx.author.mention} Here you have your Pokémon"
    if colour == "shiny":
        message = message.replace("Pokémon", "✨SHINY✨ Pokémon")
    return message


async def get_changed_stats(nature):
    decreased = nature['decreased_stat']['name'].replace("-", " ").capitalize()
    increased = nature['increased_stat']['name'].replace("-", " ").capitalize()
    return decreased, increased


async def get_pokemon_elements(response):
    poke = await load_pokemon(response)

    name = await validate_name(poke)

    colour, sprite_url = await get_sprite_color(name)

    moves = get_moves_string(name)

    nature = await get_nature()
    return colour, moves, name, nature, sprite_url


async def get_sprite_color(name):
    sprite_url, colour = generate_url(name)
    logging.info(msg=f"Sprite URL: {sprite_url}")
    logging.info(msg=f"Colour: {colour}")
    return colour, sprite_url


async def validate_name(poke):
    name = eliminate_invalid_forms(poke['varieties'])
    logging.info(msg=f"NAME:{name}")
    return name


async def load_pokemon(response):
    poke = json.loads(response.text)
    logging.info(msg=f"Pokemon response: \n {poke['name']}")
    return poke


async def get_nature():
    natures = json.loads(requests.get("https://pokeapi.co/api/v2/nature").text)
    nature = pick_nature(natures)
    return nature


async def get_url(pokemon_index):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_index}"
    return url


async def get_random_index():
    pokemon_index = random.randint(MIN_INDEX, MAX_INDEX)
    return pokemon_index


def pick_nature(natures):
    random_nature = get_random_nature(natures)
    detailed_nature = requests.get(random_nature['url'])
    loaded_detailed_nature = json.loads(detailed_nature.text)
    return loaded_detailed_nature


def build_embed(moves_string: str, stats_string: str, pokemon_name: str,
                nature, sprite_url):
    """
    Creates an Embed from Discord

    :param moves_string: Formatted string which contains the moves of the Pokémon
    :param stats_string: Formatted string which contains the stats of the Pokémon
    :param pokemon_name: Random generated name
    :param nature: Nature of the Pokémon
    :param sprite_url: URL of the sprite
    :return: Formatted embed
    """
    ret = discord.Embed()

    ret.set_image(url=sprite_url)
    logger.info(msg="Embed image setted")
    # Pokemon Moves
    ret.add_field(name="Moves", value=moves_string)
    logger.info(msg="Embed move list created")

    # Pokemon Stats
    ret.add_field(name="Stats", value=stats_string)
    logger.info(msg="Embed stats list created")

    # Pokémon name
    ret.title = f"*{nature['name'].capitalize()}* {pokemon_name.capitalize()}"
    logger.info(msg="Embed title setted")

    return ret
