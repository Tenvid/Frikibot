"""SQLAlchemy implementation of TrainerRepository."""

import sqlalchemy

from frikibot.db.models.trainer import Trainer
from frikibot.domain.trainer_repository import TrainerRepository


class SQLAlchemyTrainerRepository(TrainerRepository):
    """Concrete implementation of TrainerRepository using SQLAlchemy."""

    def __init__(self, session):
        """Initialize the repository with a SQLAlchemy session."""
        self.session = session

    def add(self, trainer):
        """
        Add a Trainer to the repository.

        Args:
            trainer (trainer_repository.Trainer): The Trainer to add.

        """
        try:
            self.session.add(trainer)
            self.session.commit()
        except sqlalchemy.exc.SQLAlchemyError:
            self.session.rollback()

    def get_by_code(self, trainer_code: str) -> Trainer | None:
        """
        Get a Trainer by their ID.

        Args:
            trainer_code (str): The Trainer's code.

        Returns:
            trainer_repository.Trainer | None: The Trainer if found, else None.

        """
        return self.session.query(Trainer).filter_by(code=trainer_code).first()
