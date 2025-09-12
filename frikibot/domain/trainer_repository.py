"""Generic interface for Trainer repository."""

from abc import ABC, abstractmethod


class TrainerRepository(ABC):
    """Generic interface for Trainer repository."""

    @abstractmethod
    def add(self, trainer_name: str, trainer_code: str):
        """
        Add a new trainer to the repository.

        Args:
        ----
            trainer_name (str): Trainer name. Same as Discord username.
            trainer_code (str): Trainer primary key. Same as Discord inner id.

        """
