"""
Script made by David Gómez.

This module defines Paginated View for Discord Message.
"""

import math
import typing

import discord
from discord.ext import commands


class PaginatedView(discord.ui.View):
    """Definition of paginated view."""

    data: list
    current_page: int = 1
    separator: int = 5
    user: str = "User"

    def create_embed(self, data: list[tuple]) -> discord.Embed:
        """
        Generate list page.

        Args:
        ----
            data (list): Data list which will be shown in pages.

        Returns:
        -------
            discord.Embed: Selected list page.

        """
        embed = discord.Embed(title=f"{self.user.capitalize()} Pokémon list")
        for elem in data:
            embed.add_field(
                name=elem[1].replace("-", " ").capitalize(),
                value="\n".join([x.replace("-", " ").capitalize() for x in elem[5:9]]),
            )

        return embed

    async def send(self, ctx: commands.Context[typing.Any]) -> None:
        """
        Send message to text channel.

        Args:
        ----
            ctx (commands.Context[typing.Any]): Command context

        """
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[: self.separator])

    async def update_message(self, data: list) -> None:
        """
        Change page information when a button is pressed.

        Args:
        ----
            data (list): Data to be shown.

        """
        await self.message.edit(embed=self.create_embed(data), view=self)

    @discord.ui.button(label="<<-", style=discord.ButtonStyle.primary)
    async def first_page_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,  # noqa
    ):
        """
        Define button to return to first page.

        Args:
        ----
            interaction (discord.Interaction): User interaction with button.
            button (discord.ui.Button): Button instance.

        """
        await interaction.response.defer()
        self.current_page = 1
        last_element = self.current_page * self.separator
        starter_item = last_element - self.separator
        await self.update_message(self.data[starter_item:last_element])

    @discord.ui.button(label="<-", style=discord.ButtonStyle.primary)
    async def previous_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,  # noqa
    ):
        """
        Define button to go to previous page.

        Args:
        ----
            interaction (discord.Interaction): User interaction with button.
            button (discord.ui.Button): Button instance.

        """
        await interaction.response.defer()
        if self.current_page > 1:
            self.current_page -= 1
        last_element = self.current_page * self.separator
        starter_item = last_element - self.separator
        await self.update_message(self.data[starter_item:last_element])

    @discord.ui.button(label="->", style=discord.ButtonStyle.primary)
    async def next_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,  # noqa
    ):
        """
        Define button to go to next page.

        Args:
        ----
            interaction (discord.Interaction): User interaction with button.
            button (discord.ui.Button): Button instance.

        """
        await interaction.response.defer()
        self.current_page += 1
        last_element = self.current_page * self.separator
        if last_element > len(self.data):
            self.current_page -= 1
            last_element = self.current_page * self.separator

        starter_item = last_element - self.separator
        await self.update_message(self.data[starter_item:last_element])

    @discord.ui.button(label="->>", style=discord.ButtonStyle.primary)
    async def last_page_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,  # noqa
    ):
        """
        Define button to go to last page.

        Args:
        ----
            interaction (discord.Interaction): User interaction with button.
            button (discord.ui.Button): Button instance.

        """
        await interaction.response.defer()
        last_element = len(self.data)
        self.current_page = math.ceil(last_element / self.separator)
        starter_item = last_element - self.separator
        await self.update_message(self.data[starter_item:last_element])
