"""Module for PokeAPIController class."""


from frikibot.entities.nature import Nature
from frikibot.entities.variety import Variety
from frikibot.entities.variety_details import VarietyDetails
from frikibot.usecases import fetch_pokemon_varieties_usecase, fetch_random_nature_usecase, fetch_variety_details_usecase


class PokeAPIController:
    """Controller for handling PokeAPI interactions."""

    def fetch_pokemon_varieties(self, pokemon_index: int) -> list[Variety]:
        """Get all varieties of a Pokémon given its index."""
        return fetch_pokemon_varieties_usecase.FetchPokemonVarietiesUseCase().execute(pokemon_index)

    def fetch_variety_details(self, variety: Variety) -> VarietyDetails:
        """Get details of a variety."""
        return fetch_variety_details_usecase.FetchVarietyDetailsUseCase().execute(variety)

    def fetch_random_nature(self) -> Nature:
        """Get a random nature."""
        return fetch_random_nature_usecase.FetchRandomNatureUseCase().execute()
