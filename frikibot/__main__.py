"""
Script made by David Gómez.

This module contains the commands available in the Frikibot.
"""

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from frikibot.controller.discord_controller import DiscordController
from frikibot.database_handler import create_database

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="-", intents=discord.flags.Intents().all())

logging.basicConfig(level="INFO", format="%(name)s-%(levelname)s-%(message)s")


if __name__ == "__main__":
        create_database()
        controller = DiscordController(bot)
        controller.start(TOKEN)
