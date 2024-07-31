"""
Script made by David Gómez.

This module contains a class for Pokémon entities
"""


class Pokemon:
    """Pokémon definition."""

    def __init__(
        self,
        *,
        name: str,
        pokedex_number: int,
        moves_list: list[str],
        nature: str,
        first_type: str,
        second_type: str,
        author_code: str,
    ):
        """
        Create Pokémon instance.

        Args:
        ----
            name (str): _description_
            pokedex_number (int): _description_
            moves_list (list): _description_
            nature (str): _description_
            first_type (str): _description_
            second_type (str): _description_
            author_code (str): _description_

        """
        self.name = name
        self.pokedex_number = pokedex_number
        self.moves_list = moves_list
        self.nature = nature
        self.first_type = first_type
        self.second_type = second_type
        self.author_code = author_code
