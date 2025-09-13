"""Interface for a Pokemon repository."""

from abc import ABC, abstractmethod

from frikibot.domain.pokemon import Pokemon


class PokemonRepository(ABC):
    """Interface for a Pokemon repository."""

    @abstractmethod
    def add(self, poke: Pokemon) -> None:
        """
        Insert a Pokémon in database.

        Args:
        ----
            poke (Pokemon): Generated Pokémon

        Raises:
        ------
            NonExistingElementException: Raise when POKEMON_TABLE not in .env

        """
