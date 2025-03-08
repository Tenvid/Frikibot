from dataclasses import dataclass


@dataclass(kw_only=True)
class VarietyData:
    available_abilities: list[dict]
    available_moves: list[dict]
    name: str
    combat_stats: list[dict]
    types: list[dict]
    sprite: str
