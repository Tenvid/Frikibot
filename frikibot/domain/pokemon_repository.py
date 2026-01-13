"""Abstract base class for Pokemon repository."""

import abc

from frikibot.db.models import pokemon


class PokemonRepository(abc.ABC):
    """Abstract base class for Pokemon repository."""

    @abc.abstractmethod
    def add(self, pokemon: pokemon.Pokemon):
        """
        Add a Pokemon to the repository.

        Args:
            pokemon (pokemon.Pokemon): The Pokemon to add.

        """

    @abc.abstractmethod
    def get_all_by_trainer(self, trainer_id: int) -> list[pokemon.Pokemon]:  # noqa
        """
        Get all Pokemons for a specific trainer.

        Args:
            trainer_id (int): The ID of the trainer.

        Returns:
            list[pokemon.Pokemon]: A list of Pokemons owned by the trainer.

        """
        ...
