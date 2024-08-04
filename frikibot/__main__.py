"""
Script made by David Gómez.

This module contains the commands available in the Frikibot.
"""

import logging
import os
import typing

from discord.ext import commands
from dotenv import load_dotenv

from frikibot import pokemon_generator
from frikibot.database_handler import create_trainer, read_trainer

load_dotenv()
# Bot token obtained from the environment variable
TOKEN = os.getenv("DISCORD_TOKEN")
# Bot instance
bot = pokemon_generator.bot

logging.basicConfig(level="INFO", format="%(process)d-%(levelname)s-%(message)s")


# Event realised when the bot is connected
@bot.event
async def on_ready() -> None:
    """Print a log message when bot is connected."""
    print("Connected")


# -hello
@bot.command(name="hello", help="Says hello to user,")
@commands.cooldown(1, 5, commands.BucketType.user)
async def hello(ctx: commands.Context[typing.Any]) -> None:
    """
    Greet user.

    Args:
    ----
        ctx (commands.Context[typing.Any]): Command context

    """
    await ctx.send(f"Hola, {ctx.author.mention}!")


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command(name="pokemon", help="Generates a random Pokémon")
async def pokemon(ctx: commands.Context[typing.Any]) -> None:
    """
    Generate random Pokémon.

    Args:
    ----
        ctx (commands.Context): Command context

    """
    embed, message = pokemon_generator.generate_random_pokemon(ctx)
    if not read_trainer(str(ctx.author.id)):
        logging.info("Trainer added")
        create_trainer(ctx.author.name, str(ctx.author.id))
    await ctx.send(message, embed=embed)


@bot.event
async def on_command_error(
    ctx: commands.Context[typing.Any], error: commands.CommandError
) -> None:
    """
    Tell the user that an error happened.

    Args:
    ----
        ctx (commands.Context): Context of the command
        error (commands.CommandError): Error of the command

    """
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f" {ctx.author.mention} This command is actually on cooldown, wait "
            f" {round(error.retry_after, 2)} seconds."
        )


# Bot start
if TOKEN:
    bot.run(TOKEN)
