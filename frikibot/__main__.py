"""
Script made by David Gómez.

This module contains the commands available in the Frikibot.
"""

import logging
import os
import typing

import discord
from discord.ext import commands
from dotenv import load_dotenv

from frikibot import pokemon_generator
from frikibot.database_handler import create_database
from frikibot.domain.paginated_view import PaginatedView
from frikibot.infrastructure.sqlite3_pokemon_repository import SQLite3PokemonRepository
from frikibot.infrastructure.sqlite3_trainer_repository import SQLite3TrainerRepository

load_dotenv()

# Bot token obtained from the environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot instance
bot = commands.Bot(command_prefix="-", intents=discord.flags.Intents().all())

logging.basicConfig(level="INFO", format="%(name)s-%(levelname)s-%(message)s")

logger = logging.getLogger("main")

trainer_repository = SQLite3TrainerRepository()
pokemon_repository = SQLite3PokemonRepository()


# Event realised when the bot is connected
@bot.event
async def on_ready() -> None:
    """Print a message when bot is connected."""
    logger.info("Connected")


@commands.cooldown(1, 5, commands.BucketType.user)  # type: ignore
@bot.command(name="pokemon", help="Generates a random Pokémon")
async def pokemon(
    ctx: commands.Context[typing.Any],
) -> None:
    """
    Generate random Pokémon.

    Args:
    ----
        ctx (commands.Context): Command context

    """
    embed, message = pokemon_generator.generate_random_pokemon(ctx)
    if not trainer_repository.get_by_id(str(ctx.author.id)):
        try:
            trainer_repository.add(ctx.author.name, str(ctx.author.id))
            logger.info("Trainer added")
        except Exception as e:
            logger.error(f"Failed to add trainer: {e}")
    await ctx.send(message, embed=embed)


@commands.cooldown(1, 5, commands.BucketType.user)  # type: ignore
@bot.command(
    name="dex", help="List all Pokémon from user and show them in a paginated view"
)
async def dex(ctx: commands.Context[typing.Any]) -> None:
    """
    List all Pokémon from user and show them in a paginated view.

    Args:
    ----
        ctx (commands.Context[typing.Any]): Message context

    """
    view = PaginatedView()
    view.data = pokemon_repository.get_by_trainer_id(str(ctx.author.id))
    view.user = ctx.author.name
    await view.send(ctx)


@bot.event
async def on_command_error(
    ctx: commands.Context[typing.Any],
    error: commands.CommandError,
) -> None:
    """
    Handle commands errors depending on its type.

    Args:
    ----
        ctx (commands.Context): Context of the command
        error (commands.CommandError): Error of the command

    """
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f" {ctx.author.mention} This command is actually on cooldown, wait "
            f" {round(error.retry_after, 2)} seconds.",
        )


if __name__ == "__main__":
    create_database()

# Bot start
if TOKEN:
    bot.run(TOKEN)
