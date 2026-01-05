"""Usecase for generating Embed for Discord messages."""

from discord import Embed

from frikibot.domain.discord_embed_builder import DiscordEmbedBuilder
from frikibot.pokemon import Pokemon


class GenerateEmbedUseCase:
    """Usecase for generating Embed for Discord messages."""

    def __init__(self, pokemon: Pokemon):
        """Initialize the use case with a pokemon."""
        self.__pokemon = pokemon

    def execute(self) -> Embed:
        """Execute the usecase."""
        return (
            DiscordEmbedBuilder()
            .with_title(
                f"# {self.__pokemon.pokedex_number} *{self.__pokemon.nature.name.capitalize() if self.__pokemon.nature else 'Serious'}*"
                f" {self.__pokemon.name.capitalize()}"
            )
            .with_description(f"Ability: {self.__pokemon.ability.replace('-', ' ').capitalize()}")
            .with_image(self.__pokemon.sprite)
            .with_field(name="Moves", value=self.__get_moves_string(self.__pokemon.moves_list))
            .with_field(name="Stats", value=str(self.__pokemon.stats))
            .build()
        )

    def __get_moves_string(self, moves_list: list[str]) -> str:
        """
        Generate a string with the moves of the Pokémon from the possible ones.

        Args:
        ----
        moves_list (list[str]): List with raw names of moves

        Returns:
        -------
        str: String with moves in a list form

        """
        moves_list = [move.replace("-", " ").capitalize() for move in moves_list]
        ret = "```\n"

        for move in moves_list:
            ret += f"{move}"
            if move == moves_list[-1]:
                break
            ret += "\n"

        ret += "```"

        return ret
