"""Main script from Frikibot"""
import os
import logging
import discord
from dotenv import load_dotenv
from discord.ext import commands
from frikibot import pokemon_generator
from frikibot.database_handler import get_all_pokemon_from_trainer

load_dotenv()
# Bot token obtained from the environment variable
TOKEN = os.getenv("DISCORD_TOKEN")
# Bot instance
bot = commands.Bot(command_prefix="-", intents=discord.flags.Intents().all())

logging.basicConfig(level="DEBUG", format='%(process)d-%(levelname)s-%(message)s')


# Event realised when the bot is connected
@bot.event
async def on_ready():
    """Announce the bot has been connected"""
    print("Connected")


# -hello
@bot.command(name='hello', help='Says hello to user,')
@commands.cooldown(1, 5, commands.BucketType.user)
async def hello(ctx):
    """Say hello to a user"""
    await ctx.send(f'Hola, {ctx.author.mention}!')


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command(name="pokemon", help="Generates a random Pokémon")
async def pokemon(ctx):
    """Create a pokemon and the embed message with its data"""
    embed, message = pokemon_generator.generate_random_pokemon(ctx)

    await ctx.send(message, embed=embed)


@bot.command(name="pokeList", help="Shows the list of Pokémon of the trainer")
async def my_pokemon_list(ctx):
    """Print all Pokémon of a user"""
    await ctx.send(get_all_pokemon_from_trainer(ctx.author.id))


@bot.event
async def on_command_error(ctx, error):
    """Event raised when an error happens"""
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f' {ctx.author.mention} This command is actually on cooldown, you can use it in'
            f' {round(error.retry_after, 2)} seconds.'
        )


# Bot start
bot.run(TOKEN)
