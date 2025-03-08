from global_variables import TIMEOUT
import requests
from random import choice


def create_random_moves_list(base_name: str) -> list[str]:
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

    url = f"https://pokeapi.co/api/v2/pokemon/{base_name.replace('-gmax', '')}"

    response = requests.get(url, timeout=TIMEOUT)

    if response.status_code == 200:
        json_response = response.json()

        available_moves = json_response["moves"]

        while len(ret) < 4:
            move = choice(available_moves)["move"]["name"]

            if move not in ret:
                ret.append(move)
    return ret
