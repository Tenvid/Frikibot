"""
Script made by David Gómez.

This module contains the definition for class Stats.
"""

import math


class Stats:
    """Pokémon stats definition."""

    hp: int | None
    attack: int | None
    defense: int | None
    special_attack: int | None
    special_defense: int | None
    speed: int | None

    def __init__(
        self,
        data: dict | None,
        decreased: str | None = None,
        increased: str | None = None,
        *,
        hp: int | None,
        attack: int | None,
        defense: int | None,
        special_attack: int | None,
        special_defense: int | None,
        speed: int | None,
    ):
        """
        Pokémon stats constructor.

        Args:
        ----
            hp (int): Base hp stat
            attack (int): Base attack stat
            defense (int): Base defense stat
            special_attack (int): Base special attack stat
            special_defense (int): Base special defense stat
            speed (int): Base speed stat
            decreased (str | None, optional): Stat decreased by nature. Defaults to None.
            increased (str | None, optional): Stat increased by nature. Defaults to None.

        """
        if data:
            self.hp = data[0]["base_stat"]
            self.attack = data[1]["base_stat"]
            self.defense = data[2]["base_stat"]
            self.special_attack = data[3]["base_stat"]
            self.special_defense = data[4]["base_stat"]
            self.speed = data[5]["base_stat"]
        else:
            self.hp = hp
            self.attack = attack
            self.defense = defense
            self.special_attack = special_attack
            self.special_defense = special_defense
            self.speed = speed
        self.decreased = decreased
        self.increased = increased

    def __str__(self) -> str:
        """
        Create string version of self.

        Returns
        -------
            str: Self made string.

        """
        return "\n".join(
            [self.add_color_nature(stat_tuple=x) for x in self.get_stats_list()]
        )

    def add_color_nature(self, stat_tuple: tuple[str, int]) -> str:
        """
        Add color to stats modified by nature.

        Args:
        ----
            stat_tuple (tuple[str, int]): Tuple [stat_name, stat_value]

        Returns:
        -------
            str: 'stat_name: stat_value' with color if needed

        """
        if self.decreased and stat_tuple[0] == self.decreased:
            return (
                f"\u001b[0;34m{stat_tuple[0].replace('-', ' ').capitalize()}:"
                f" {math.floor(stat_tuple[1] * 0.9)}-\u001b[0;0m"
            )
        if self.increased and stat_tuple[0] == self.increased:
            return (
                f"\u001b[0;31m{stat_tuple[0].replace('-', ' ').capitalize()}:"
                f"{math.floor(stat_tuple[1] * 1.1)}+\u001b[0;0m"
            )

        return f"{stat_tuple[0].replace('-', ' ').capitalize()}: {stat_tuple[1]}"

    def get_stats_list(self) -> list:
        """
        Generate a list of tuples with stat names and their values.

        Returns
        -------
            list: List of tuples [stat_name: stat_value]

        """
        return [
            ("hp", self.hp),
            ("attack", self.attack),
            ("defense", self.defense),
            ("special-attack", self.special_attack),
            ("special-defense", self.special_defense),
            ("speed", self.speed),
        ]
