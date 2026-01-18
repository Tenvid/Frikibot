"""SQLAlchemy implementation of the Pokemon repository."""

import sqlalchemy
from sqlalchemy.orm import Session

from frikibot.db.models import pokemon
from frikibot.domain import pokemon_repository


class SQLAlchemyPokemonRepository(pokemon_repository.PokemonRepository):
    """Concrete implementation of PokemonRepository using SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with a SQLAlchemy session."""
        self.session = session

    def add(self, pokemon: pokemon.Pokemon) -> None:
        """
        Add a Pokemon to the repository.

        Args:
            pokemon (pokemon_repository.Pokemon): The Pokemon to add.

        """
        try:
            self.session.add(pokemon)
            self.session.commit()
        except sqlalchemy.exc.SQLAlchemyError:
            self.session.rollback()

    def get_all_by_trainer(self, trainer_id: int) -> list[pokemon.Pokemon]:
        """
        Get all Pokemons for a specific trainer.

        Args:
            trainer_id (int): The ID of the trainer.

        Returns:
            list[pokemon.Pokemon]: A list of Pokemons owned by the trainer.

        """
        return self.session.query(pokemon.Pokemon).filter(pokemon.Pokemon.trainer_id == trainer_id).all()
