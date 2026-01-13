"""SQLAlchemy implementation of the Pokemon repository."""

from sqlalchemy.orm import Session

from frikibot.db.models import pokemon
from frikibot.domain import pokemon_repository
from frikibot.infrastructure.database import SESSION


class SQLAlchemyPokemonRepository(pokemon_repository.PokemonRepository):
    """Concrete implementation of PokemonRepository using SQLAlchemy."""

    def __init__(self, session: Session = SESSION) -> None:
        """Initialize the repository with a SQLAlchemy session."""
        self.session = session

    def add(self, pokemon: pokemon.Pokemon) -> None:
        """
        Add a Pokemon to the repository.

        Args:
            pokemon (pokemon_repository.Pokemon): The Pokemon to add.

        """
        self.session.add(pokemon)
        self.session.commit()
