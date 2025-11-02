"""Module for PokeAPIController class."""

import random

import requests

from frikibot.entities.nature import Nature
from frikibot.entities.variety import Variety
from frikibot.entities.variety_details import VarietyDetails
from frikibot.exceptions import NatureFetchError, VarietyDetailsFetchError, VarietyFetchError
from frikibot.global_variables import TIMEOUT


class PokeAPIController:
        """Controller for handling PokeAPI interactions."""

        def __init__(self):
                """Initialize the PokeAPIController."""

        def fetch_pokemon_varieties(self, pokemon_index: int) -> list[Variety]:
                """Get all varieties of a Pokémon given its index."""
                try:
                        raw_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_index}", timeout=TIMEOUT)
                        if raw_response.status_code == 200:
                                json_response = raw_response.json()
                                return [Variety.from_json(v) for v in json_response["varieties"]]
                except requests.ConnectionError as exc:
                        raise VarietyFetchError(f"Connection error happened when trying to fetch pokémon: {pokemon_index}") from exc
                except requests.Timeout as exc:
                        raise VarietyFetchError(f"Timeout error happened when trying to fetch pokémon: {pokemon_index}") from exc
                raise VarietyFetchError(f"Failed fetching with index {pokemon_index}. Response status code: {raw_response.status_code}")

        def fetch_variety_details(self, variety: Variety) -> VarietyDetails:
                """Get details of a variety."""
                try:
                        raw_response = requests.get(variety.url, timeout=TIMEOUT)
                        if raw_response.status_code == 200:
                                json_response = raw_response.json()
                                return VarietyDetails.from_json(json_response)
                except requests.ConnectionError as exc:
                        raise VarietyDetailsFetchError(f"Connection error happened trying to get details of variety: {variety}") from exc
                except requests.Timeout as exc:
                        raise VarietyDetailsFetchError(f"Timeout error happened trying to get details of variety: {variety}") from exc
                raise VarietyFetchError(f"Failed fetching variety details from variety: {variety} . Response status code: {raw_response.status_code}")

        def fetch_random_nature(self) -> Nature:
                """Get a random nature."""
                nature_index = random.randint(0, 25 - 1)  # TODO: Max index should be retrieved from api  # noqa: S311
                try:
                        response = requests.get(f"https://pokeapi.co/api/v2/nature/{nature_index}", timeout=TIMEOUT)
                        if response.status_code == 200:
                                return Nature.from_json(response.json())
                        raise requests.ConnectionError("Status code: %d", response.status_code)
                except requests.ConnectionError as exc:
                        raise NatureFetchError("Connection error trying to fetch a random nature") from exc
                except requests.Timeout as exc:
                        raise NatureFetchError("Timeout error happened trying to fetch a random nature.") from exc
