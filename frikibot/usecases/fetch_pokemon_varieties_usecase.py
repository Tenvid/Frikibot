"""Use case to fetch all varieties of a Pokémon given its index."""

import requests

from frikibot.entities.variety import Variety
from frikibot.shared.exceptions import VarietyFetchError
from frikibot.shared.global_variables import TIMEOUT


class FetchPokemonVarietiesUseCase:
    """Use case to fetch all varieties of a Pokémon given its index."""

    def execute(self, pokemon_index: int) -> list[Variety]:
        """Execute the use case to fetch Pokémon varieties."""
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
