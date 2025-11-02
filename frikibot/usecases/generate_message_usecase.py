"""Usecase for generating Discord Messages."""


class GenerateMessageUseCase:
        """Usecase for generating Discord Messages."""

        def __init__(self, ctx, color: str):
                """Initialize the use case with the command context and color."""
                self.__ctx = ctx
                self.__color = color

        def execute(self):
                """Execute the usecase."""
                message = f"{self.__ctx.author.mention} Here you have your Pokémon"

                if self.__color == "shiny":
                        message = message.replace("Pokémon", "✨SHINY✨ Pokémon")
                return message
