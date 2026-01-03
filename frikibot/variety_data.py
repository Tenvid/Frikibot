"""
Script made by David Gómez.

This module contains the defition for the class VarietyData.
"""

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger("VarietyData")


@dataclass(kw_only=True)
class VarietyData:
        """Variety representation."""

        available_abilities: list[dict[str, Any]]
        available_moves: list[dict[str, Any]]
        name: str
        combat_stats: list[dict[str, Any]]
        types: list[dict[str, Any]]
        available_sprites: dict[str, Any]

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
