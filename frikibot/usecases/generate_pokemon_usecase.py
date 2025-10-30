"""Use case for generating a random Pokémon."""

import typing

import discord
from discord.ext import commands

from frikibot import pokemon_generator


class GeneratePokemonUseCase:
        """Use case for generating a random Pokémon."""

        def __init__(self, context: commands.Context[typing.Any]) -> None:
                """Initialize the use case with the command context."""
                self.__context = context

        def execute(self) -> tuple[discord.Embed, str]:
                """Execute the use case to generate a random Pokémon."""
                return pokemon_generator.generate_random_pokemon(self.__context)
