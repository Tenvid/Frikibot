"""Module for building Discord Embed objects."""

from discord import Embed


class DiscordEmbedBuilder:
        """Builder for Discord Embed objects."""

        def __init__(self) -> None:
                """Initialize the DiscordEmbedBuilder."""
                self.__embed = Embed()

        def with_title(self, title: str) -> "DiscordEmbedBuilder":
                """Set the title of the embed."""
                self.__embed.title = title
                return self

        def with_description(self, description: str) -> "DiscordEmbedBuilder":
                """Set the description of the embed."""
                self.__embed.description = description
                return self

        def with_image(self, url: str | None) -> "DiscordEmbedBuilder":
                """Set the image of the embed."""
                self.__embed.set_image(url=url)
                return self

        def with_field(self, name: str, value: str) -> "DiscordEmbedBuilder":
                """Add a field to the embed."""
                self.__embed.add_field(name=name, value=value)
                return self

        def build(self) -> Embed:
                """Build and return the Discord Embed object."""
                return self.__embed
