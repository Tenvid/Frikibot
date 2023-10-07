import os
from discord.ext import commands
import logging

from dotenv import load_dotenv

import pokemon_generator

load_dotenv()
# Bot token obtained from the environment variable
TOKEN = os.getenv("DISCORD_TOKEN")
# Bot instance
bot = pokemon_generator.bot


logging.basicConfig(level="INFO", format='%(process)d-%(levelname)s-%(message)s')


# Event realised when the bot is connected
@bot.event
async def on_ready():
    print("Connected")


# -hello
@bot.command(name='hello', help='Says hello to user,')
@commands.cooldown(1, 5, commands.BucketType.user)
async def hello(ctx):
    await ctx.send(f'Hola, {ctx.author.mention}!')


@bot.command(name="test", help="test_command")
async def test(ctx):
    await ctx.send("""
  ```ansi
\u001b[0;31mAttack\u001b[0;0m
```
""")


@commands.cooldown(1, 5, commands.BucketType.guild)
@bot.command(name="pokemon", help="Generates a random Pokémon")
async def pokemon(ctx):
    embed, message = await pokemon_generator.generate_random_pokemon(ctx)

    await ctx.send(message, embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f' {ctx.author.mention} This command is actually on cooldown, you can use it in'
            f' {round(error.retry_after, 2)} seconds.'
        )

# Bot start
bot.run(TOKEN)
