"""Use case for fetching a random nature from the PokeAPI."""

import random

import requests

from frikibot.entities.nature import Nature
from frikibot.shared.exceptions import NatureFetchError
from frikibot.shared.global_variables import TIMEOUT


class FetchRandomNatureUseCase:
    """Use case for fetching a random nature."""

    def execute(self):
        """Execute the use case to fetch a random nature."""
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
