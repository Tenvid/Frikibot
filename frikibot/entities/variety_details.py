"""Representation of variety details."""

import logging
from typing import Any

from frikibot.entities.variety import Variety

logger = logging.getLogger("VarietyDetails")


class VarietyDetails(Variety):
        """Representation of variety details."""

        def __init__(
                self,
                is_default: bool,  # noqa: FBT001
                name: str,
                url: str,
                available_abilities: list[dict[str, Any]],
                available_moves: list[dict[str, Any]],
                combat_stats: list[dict[str, Any]],
                types: list[dict[str, Any]],
                available_sprites: dict[str, Any],
        ):
                """
                Initialize a VarietyDetails instance.

                Args:
                ----
                        is_default (bool): Whether this variety is the default one.
                        name (str): The name of the variety.
                        url (str): The URL associated with the variety.
                        available_abilities (list[dict]): List of available abilities.
                        available_moves (list[dict]): List of available moves.
                        combat_stats (list[dict]): List of combat stats.
                        types (list[dict]): List of types.
                        available_sprites (dict): Dictionary of available sprites.

                """
                super().__init__(is_default, name, url)
                self.__available_abilities = available_abilities
                self.__available_moves = available_moves
                self.__combat_stats = combat_stats
                self.__types = types
                self.__available_sprites = available_sprites

        @property
        def available_abilities(self) -> list[dict[str, Any]]:
                """Return the available abilities."""
                return self.__available_abilities

        @available_abilities.setter
        def available_abilities(self, value: list[dict[str, Any]]) -> None:
                """Set a new value for available_abilities."""
                if not isinstance(value, list):
                        raise TypeError(f"Entered value: {value} is not valid for available_abilities")
                self.__available_abilities = value

        @property
        def available_moves(self) -> list[dict[str, Any]]:
                """Return the available moves."""
                return self.__available_moves

        @available_moves.setter
        def available_moves(self, value: list[dict[str, Any]]) -> None:
                """Set a new value for available_moves."""
                if not isinstance(value, list):
                        raise TypeError(f"Entered value: {value} is not valid for available_moves")
                self.__available_moves = value

        @property
        def combat_stats(self) -> list[dict[str, Any]]:
                """Return the combat stats."""
                return self.__combat_stats

        @combat_stats.setter
        def combat_stats(self, value: list[dict[str, Any]]) -> None:
                """Set a new value for combat_stats."""
                if not isinstance(value, list):
                        raise TypeError(f"Entered value: {value} is not valid for combat_stats")
                self.__combat_stats = value

        @property
        def types(self) -> list[dict[str, Any]]:
                """Return the types."""
                return self.__types

        @types.setter
        def types(self, value: list[dict[str, Any]]) -> None:
                """Set a new value for types."""
                if not isinstance(value, list):
                        raise TypeError(f"Entered value: {value} is not valid for types")
                self.__types = value

        @property
        def available_sprites(self) -> dict[str, Any]:
                """Return the available sprites."""
                return self.__available_sprites

        @available_sprites.setter
        def available_sprites(self, value: dict[str, Any]) -> None:
                """Set a new value for available_sprites."""
                if not isinstance(value, dict):
                        raise TypeError(f"Entered value: {value} is not valid for available_sprites")
                self.__available_sprites = value

        @classmethod
        def from_json(cls, json_data: dict[str, Any]) -> "VarietyDetails":
                """Create a VarietyDetails instance from JSON data."""
                is_default = json_data.get("is_default", False)
                name = json_data.get("name") or "NONAME"
                url = json_data.get("species", {}).get("url", "")
                available_abilities = json_data.get("abilities", [])
                available_moves = json_data.get("moves", [])
                combat_stats = json_data.get("stats", {})
                types = json_data.get("types", [])
                available_sprites = json_data.get("sprites", [])
                return cls(
                        is_default=is_default,
                        name=name,
                        url=url,
                        available_abilities=available_abilities,
                        available_moves=available_moves,
                        combat_stats=combat_stats,
                        types=types,
                        available_sprites=available_sprites,
                )

        def get_official_artwork_sprite(self, color: str) -> str | None:
                """
                Select the official artwork from the available sprites.

                Args:
                ----
                color (str): Sprite color, ["default", "shiny"]

                Returns:
                -------
                str: Sprite url

                """
                sprite = None
                try:
                        sprite = self.available_sprites["other"]["official-artwork"][f"front_{color}"]
                except KeyError:
                        logger.error(
                                "No official artwork could be obtained for %s \n available_sprites: %s",
                                self.name,
                                self.available_sprites,
                        )
                return sprite
