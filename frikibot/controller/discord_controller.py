"""Controller to route Discord commands."""

import logging
import random
import typing

from discord.ext import commands

from frikibot.database_handler import (
    create_trainer,
    read_pokemon_by_trainer,
    read_trainer,
)
from frikibot.infrastructure.paginated_view import PaginatedView
from frikibot.usecases.generate_embed_usecase import GenerateEmbedUseCase
from frikibot.usecases.generate_message_usecase import GenerateMessageUseCase
from frikibot.usecases.generate_pokemon_usecase import GeneratePokemonUseCase

logger = logging.getLogger(__name__)


class DiscordController:
    """Controller to route Discord commands."""

    def __init__(self, bot: commands.Bot):
        """Initialize the DiscordController with the bot and set up commands."""
        self.__bot = bot

        @self.__bot.event
        async def on_ready() -> None:
            """Print a message when bot is connected."""
            logger.info("Connected")

        @commands.cooldown(1, 5, commands.BucketType.user)
        @self.__bot.command(name="pokemon", help="Generates a random Pokémon")
        async def pokemon(
            ctx: commands.Context[typing.Any],
        ) -> None:
            """
            Generate random Pokémon.

            Args:
            ----
                    ctx (commands.Context): Command context

            """
            color = "shiny" if random.randint(0, 101) <= 10 else "default"  # noqa: S311

            pokemon = GeneratePokemonUseCase(ctx, color).execute()
            logger.info("Pokemon generated")
            embed = GenerateEmbedUseCase(pokemon).execute()
            logger.info("Embed generated")
            message = GenerateMessageUseCase(ctx, color).execute()
            logger.info("Message created")

            if not read_trainer(str(ctx.author.id)):
                logger.info("Trainer added")
                create_trainer(ctx.author.name, str(ctx.author.id))
            await ctx.send(message, embed=embed)

        @commands.cooldown(1, 5, commands.BucketType.user)
        @self.__bot.command(
            name="dex",
            help="List all Pokémon from user",
        )
        async def dex(ctx: commands.Context[typing.Any]) -> None:
            """
            List all Pokémon from user and show them in a paginated view.

            Args:
            ----
                    ctx (commands.Context[typing.Any]): Message context

            """
            view = PaginatedView()
            view.data = read_pokemon_by_trainer(str(ctx.author.id))
            view.user = ctx.author.name
            await view.send(ctx)

        @self.__bot.event
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
                    f" {ctx.author.mention} This command is actually on cooldown, wait {round(error.retry_after, 2)} seconds.",
                )

    def start(self, token: str) -> None:
        """
        Start the bot with the given token.

        Args:
        ----
                token (str): Discord bot token

        """
        self.__bot.run(token)
