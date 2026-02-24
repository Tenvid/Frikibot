"""
Script made by David Gómez.

This module contains the commands available in the Frikibot.
"""

import logging
import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from frikibot.controller.discord_controller import DiscordController

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    sys.exit("Error: DISCORD_TOKEN environment variable not found. Please set it in the .env file.")

bot = commands.Bot(command_prefix="-", intents=discord.flags.Intents().all())

logging.basicConfig(level="INFO", format="%(name)s-%(levelname)s-%(message)s")

if __name__ == "__main__":
    controller = DiscordController(bot)
    controller.start(TOKEN)
