"""Generate a pokemon"""
import random
import json
import logging
import discord
import requests

from frikibot.database_handler import insert_registry

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
    """Transform stats into a string"""
    stats = get_pokemon_stats(name)
    logging.info("Stats generated")
    ret = "```ansi\n"

    if decreased is None and increased is None:
        for stat in stats.items():
            actual_stat = stats[stat]
            ret += f"{stat}: {actual_stat}\n"
    else:
        for stat in stats.items():
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
    """Get 'stats' element from a Pokémon into a dict"""
    ret = {
        "Attack": 0,
        "Defense": 0,
        "Special attack": 0,
        "Special defense": 0,
        "Speed": 0
    }

    response_bis = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.replace('-gmax', '')}",
                                timeout=10)

    stats = json.loads(response_bis.text)['stats']

    stat_values = []
    for stat in stats:
        stat_values.append(stat['base_stat'])

    ret["Attack"] = stat_values[0]
    ret["Defense"] = stat_values[1]
    ret["Special attack"] = stat_values[2]
    ret["Special defense"] = stat_values[3]
    ret["Speed"] = stat_values[4]

    logging.info(f"Stats: {ret}")

    return ret


def get_random_nature(natures):
    """Pick random nature"""
    return random.choice(natures['results'])


def get_moves_string(name: str):
    """Build a string using random moves of the ones
    that a Pokémon can learn"""
    moves = get_pokemon_moves(name)
    ret = "```\n"
    for move in moves:
        ret = ret.join(f"\n {move} ")
    ret = ret.join("```")

    logging.info(f"Moves: {moves}")
    return ret


def eliminate_invalid_forms(varieties):
    """Filter Pokémon forms that cannot be printed correctly """
    variety = random.choice(varieties)
    ret_name = str(variety['pokemon']['name'])
    return correct_name(ret_name, varieties, variety)


def correct_name(ret_name: str, varieties: {}, variety: {}):
    """Fix name differencies between PokeAPI and image source"""
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
    """Fix suffixes in Pokémon names"""
    for rep in NAME_REPLACEMENTS.items():
        name = name.replace(rep, NAME_REPLACEMENTS[rep])

    return name


def get_shiny_chance():
    """Generate a random number to determine if Pokémon should be shiny"""
    index = random.randint(1, 100)
    if index <= 10:
        return "shiny"
    return "normal"


def generate_image_url(name):
    """Build image url"""
    colour = get_shiny_chance()
    url = f"https://img.pokemondb.net/sprites/home/{colour}/{name}.png"
    return url, colour


def get_random_move(moves):
    """Return a random move picked from the possible moves of a Pokémon"""
    return moves[random.randint(0, len(moves) - 1)]['move']['name'].replace("-", " ").capitalize()


def get_pokemon_moves(name):
    """Get four random moves from the ones that a Pokémon can learn"""
    ret = []
    try:
        name = name.replace("-gmax", "")
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url, timeout=10)
        jres = json.loads(response.text)
        moves = jres['moves']
        while True:
            move = get_random_move(moves)
            if move not in ret:
                ret.append(move)
            if len(ret) > 3:
                break
    except IndexError:
        pass
    return ret


def generate_random_pokemon(ctx):
    """Create a random Pokémon and send information to DB Handler"""

    author = ctx.author

    pokemon_index = get_random_index()

    url = get_url(pokemon_index)

    response = load_pokemon(requests.get(url, timeout=10))

    colour, moves, name, nature, sprite_url = get_pokemon_elements(response)

    decreased, increased = get_changed_stats(nature)

    stats_string = get_stats_string(name, decreased, increased)

    embed = build_embed(moves, stats_string, name,
                        nature, sprite_url, pokemon_index)

    message = get_message(colour, ctx)

    insert_registry(author, response, moves, nature["name"])

    return embed, message


def get_message(colour, ctx):
    """Create the message depending of the colour of the Pokémon"""
    message = f"{ctx.author.mention} Here you have your Pokémon"
    if colour == "shiny":
        message = message.replace("Pokémon", "✨SHINY✨ Pokémon")
    logging.info("Message obtained")
    return message


def get_changed_stats(nature):
    """Get the stats modified by the nature"""
    try:
        decreased = nature['decreased_stat']['name'].replace("-", " ")
        increased = nature['increased_stat']['name'].replace("-", " ")
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


def insert_pokemon_in_database():
    """TODO: Not implemented yet"""


def get_pokemon_elements(response):
    """Get all the elements from a Pokémon"""
    poke = response

    variety = random.choice(poke['varieties'])

    name = variety['pokemon']['name']

    colour, sprite_url = get_sprite_color(name, poke['varieties'], variety)

    moves = get_moves_string(name)

    nature = get_nature()

    insert_pokemon_in_database()
    return colour, moves, name, nature, sprite_url


def get_sprite_color(name, varieties, variety):
    "Build url and get colour"
    name = correct_name(name, varieties, variety)
    sprite_url, colour = generate_image_url(name)
    logging.info(msg=f"Sprite URL: {sprite_url}")
    logging.info(msg=f"Colour: {colour}")
    return colour, sprite_url


def validate_name(poke):
    """Validate the name of the Pokémon fixing naming problems"""
    name = eliminate_invalid_forms(poke['varieties'])
    logging.info(msg=f"NAME:{name}")
    return name


def load_pokemon(response):
    """Transform string response into an object"""
    poke = json.loads(response.text)
    logging.info(msg=f"\nPokemon response: {poke['name']}")
    return poke


def get_nature():
    "Get a random nature from all the available"
    natures = json.loads(requests.get("https://pokeapi.co/api/v2/nature", timeout=10).text)
    nature = pick_nature(natures)
    logging.info(f"Nature: {nature['name']}")
    return nature


def get_url(pokemon_index):
    """Generate url using Pokémon index"""
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_index}"
    return url


def get_random_index():
    """Generate a random pokedex number"""
    pokemon_index = random.randint(MIN_INDEX, MAX_INDEX)
    return pokemon_index


def pick_nature(natures):
    """Select a random nature object"""
    random_nature = get_random_nature(natures)
    detailed_nature = requests.get(random_nature['url'], timeout=10)
    loaded_detailed_nature = json.loads(detailed_nature.text)
    return loaded_detailed_nature


def build_embed(moves_string: str, stats_string: str, pokemon_name: str,
                nature, sprite_url, index: int):
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
    # Pokemon Moves
    ret.add_field(name="Moves", value=moves_string)

    # Pokemon Stats
    ret.add_field(name="Stats", value=stats_string)

    # Pokémon name
    ret.title = f"# {index} *{nature['name'].capitalize()}* {pokemon_name.capitalize()}"
    logger.info(msg="Embed title setted")

    logging.info("Embed built")

    return ret
