"""Trainer repository interface definition."""

import abc

from frikibot.db.models.trainer import Trainer


class TrainerRepository(abc.ABC):
    """Trainer repository interface."""

    @abc.abstractmethod
    def add(self, trainer: Trainer) -> None:  # noqa
        """
        Add a trainer to the repository.

        Args:
        ----
            trainer (Trainer): Trainer to add

        """

    @abc.abstractmethod
    def get_by_code(self, trainer_code: str) -> Trainer | None:
        """
        Get a trainer by their code.

        Args:
        ----
            trainer_code (str): Trainer code

        Returns:
        -------
            Trainer | None: Trainer if found, else None

        """
