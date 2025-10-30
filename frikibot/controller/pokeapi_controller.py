"""Module for PokeAPIController class."""

import requests

from frikibot.exceptions import VarietyFetchError
from frikibot.global_variables import TIMEOUT


class PokeAPIController:
        """Controller for handling PokeAPI interactions."""

        def __init__(self):
                """Initialize the PokeAPIController."""

        def fetch_pokemon_varieties(self, pokemon_index: int) -> list:
                """Get all varieties of a Pokémon given its index."""
                try:
                        raw_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_index}", timeout=TIMEOUT)
                        if raw_response.status_code == 200:
                                json_response = raw_response.json()
                                return json_response["varieties"]
                except requests.ConnectionError as exc:
                        raise VarietyFetchError(f"Connection error happened when trying to fetch pokémon: {pokemon_index}") from exc
                except requests.Timeout as exc:
                        raise VarietyFetchError(f"Timeout error happened when trying to fetch pokémon: {pokemon_index}") from exc
                raise VarietyFetchError(f"Failed fetching with index {pokemon_index}. Response status code: {raw_response.status_code}")
