"""Script made by David Gómez."""

from enum import StrEnum

MAX_INDEX = 1010  # Pokedex number of the last Pokemon in Pokédex

TIMEOUT = 10  # HTTP request timeout


class Loggers(StrEnum):
        """Logger names."""

        MAIN = "main"
        STATS = "stats"
        POKEMON_GENERATOR = "generator"
        DATABASE_HANDLER = "database-handler"
        POKEMON_CLASS = "pokemon"
        VARIETY_DATA = "variety"
