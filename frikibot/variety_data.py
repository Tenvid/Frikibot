"""
Script made by David Gómez.

This module contains the defition for the class VarietyData.
"""

from dataclasses import dataclass


@dataclass(kw_only=True)
class VarietyData:
    """Variety representation."""

    available_abilities: list[dict]
    available_moves: list[dict]
    name: str
    combat_stats: list[dict]
    types: list[dict]
    sprite: str
