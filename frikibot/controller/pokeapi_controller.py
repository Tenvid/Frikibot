"""Module for PokeAPIController class."""

import requests

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

        def fetch_all_natures(self):
                """Get all available natures."""

                def _get_natures_list() -> list[dict[str, str]] | None:
                        try:
                                response = requests.get("https://pokeapi.co/api/v2/nature", timeout=TIMEOUT)
                                if response.status_code == 200:
                                        return response.json()["results"]
                        except requests.ConnectionError as exc:
                                raise NatureFetchError("Connection error tryinh to fetch all natures") from exc
                        except requests.Timeout as exc:
                                raise NatureFetchError("Timeout error happened tryinh to fetch all natures.") from exc
