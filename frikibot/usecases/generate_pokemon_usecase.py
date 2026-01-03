"""Use case for generating a random Pokémon."""

import typing

from discord.ext import commands

from frikibot import pokemon_generator
from frikibot.pokemon import Pokemon


class GeneratePokemonUseCase:
        """Use case for generating a random Pokémon."""

        def __init__(self, context: commands.Context[typing.Any], color: str) -> None:
                """Initialize the use case with the command context."""
                self.__context = context
                self.__color = color

        def execute(self) -> Pokemon:
                """Execute the use case to generate a random Pokémon."""
                return pokemon_generator.generate_random_pokemon(self.__context, self.__color)
