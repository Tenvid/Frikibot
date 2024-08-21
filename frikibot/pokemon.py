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
        list_index: int,
        moves_list: list[str],
        nature: str,
        first_type: str,
        second_type: str | None,
        author_code: str,
    ):
        """
        Create Pokémon instance.

        Args:
        ----
            name (str): Pokémon name
            list_index (int): Pokémon number in list
            moves_list (list): List of movements
            nature (str): Pokémon nature
            first_type (str): Primary type
            second_type (str): Secondary type if there is
            author_code (str): Trainer id

        """
        self.name = name
        self.pokedex_number = list_index
        self.moves_list = moves_list
        self.nature = nature
        self.first_type = first_type
        self.second_type = second_type
        self.author_code = author_code

    @classmethod
    def from_tuple(cls: type["Pokemon"], pokemon_data: tuple) -> "Pokemon":
        """
        Generate Pokémon data using tuple data from database.

        Args:
        ----
            pokemon_data (tuple): Pokémon data obtained from database.

        Returns:
        -------
            Pokemon: Pokemon instance

        """
        return cls(
            list_index=pokemon_data[0],
            name=pokemon_data[1],
            first_type=pokemon_data[2],
            second_type=pokemon_data[3],
            author_code=pokemon_data[4],
            moves_list=[
                pokemon_data[5],
                pokemon_data[6],
                pokemon_data[7],
                pokemon_data[8],
            ],
            nature=pokemon_data[9],
        )
