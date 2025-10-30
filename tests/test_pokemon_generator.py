from unittest.mock import MagicMock, patch

import pytest
import requests

from frikibot import pokemon_generator
from frikibot.exceptions import VarietyFetchError
from frikibot.pokemon import Pokemon
from frikibot.stats import Stats


class PokemonBuilder:
        _instance: Pokemon

        def __init__(self) -> None:
                self.name = "Example"
                self.list_index = -1
                self.nature = {
                        "name": "none",
                        "decreased_stat": None,
                        "increased_stat": None,
                }
                self.first_type = "water"
                self.second_type = None
                self.author_code = "some_code"
                self.available_abilities = [{"ability": {"name": "A"}}]
                self.available_moves = [
                        {"move": {"name": "A"}},
                        {"move": {"name": "B"}},
                        {"move": {"name": "C"}},
                        {"move": {"name": "D"}},
                ]

                self.stats_data = [
                        {"base_stat": 0},
                        {"base_stat": 0},
                        {"base_stat": 0},
                        {"base_stat": 0},
                        {"base_stat": 0},
                        {"base_stat": 0},
                ]
                self.sprite = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png"

        def with_stats(self, stats: list[dict[str, int]]) -> "PokemonBuilder":
                self.stats_data = stats
                return self

        def with_nature(self, nature: dict) -> "PokemonBuilder":
                self.nature = nature
                return self

        def build(self) -> Pokemon:
                return Pokemon(
                        name=self.name,
                        first_type=self.first_type,
                        second_type=self.second_type,
                        author_code=self.author_code,
                        available_abilities=self.available_abilities,
                        available_moves=self.available_moves,
                        list_index=self.list_index,
                        nature=self.nature,
                        stats_data=self.stats_data,
                        sprite=self.sprite,
                )


def test_pokemon_instance_attributes_are_correct():
        pokemon = PokemonBuilder().build()

        assert pokemon.ability == "A"
        assert pokemon.name == "Example"
        assert pokemon.pokedex_number == -1
        assert pokemon.nature == {
                "decreased_stat": None,
                "increased_stat": None,
                "name": "none",
        }
        assert pokemon.nature_name == "none"
        assert pokemon.first_type == "water"
        assert pokemon.second_type is None
        assert pokemon.author_code == "some_code"
        for move in pokemon.moves_list:
                assert move in ["A", "B", "C", "D"]
        assert pokemon.stats.hp == 0
        assert pokemon.stats.attack == 0
        assert pokemon.stats.defense == 0
        assert pokemon.stats.special_attack == 0
        assert pokemon.stats.special_defense == 0
        assert pokemon.stats.speed == 0


def test_get_stats_string_with_neutral_nature():
        fake_pokemon = PokemonBuilder().build()
        stats_string = str(fake_pokemon.stats)
        assert (
                stats_string
                == """```ansi
Hp: 0
Attack: 0
Defense: 0
Special attack: 0
Special defense: 0
Speed: 0```"""
        )


def test_get_stats_string_with_non_neutral_nature():
        fake_pokemon = (
                PokemonBuilder()
                .with_nature(
                        {
                                "name": "impish",
                                "increased_stat": {"name": "defense"},
                                "decreased_stat": {"name": "special-attack"},
                        }
                )
                .build()
        )
        stats_string = str(fake_pokemon.stats)
        assert (
                stats_string
                == """```ansi
Hp: 0
Attack: 0
\x1b[0;31mDefense:0+\x1b[0;0m
\x1b[0;34mSpecial attack: 0-\x1b[0;0m
Special defense: 0
Speed: 0```"""
        )


def test_get_pokemon_stats():
        fake_pokemon = (
                PokemonBuilder()
                .with_stats(
                        [
                                {"base_stat": 70},
                                {"base_stat": 110},
                                {"base_stat": 70},
                                {"base_stat": 115},
                                {"base_stat": 70},
                                {"base_stat": 90},
                        ]
                )
                .build()
        )

        stats = fake_pokemon.stats
        assert type(stats) is Stats
        assert stats.hp == 70
        assert stats.attack == 110
        assert stats.defense == 70
        assert stats.special_attack == 115
        assert stats.special_defense == 70
        assert stats.speed == 90


def test_get_moves_string():
        move_list = ["swords-dance", "aura-sphere", "close-combat", "iron-head"]

        moves_string = pokemon_generator.get_moves_string(move_list)

        assert (
                moves_string
                == """```
Swords dance
Aura sphere
Close combat
Iron head```"""
        )


def test_get_message_normal():
        context = MagicMock()
        context.author.mention = "Author"
        message = pokemon_generator.get_message("normal", context)
        assert message == "Author Here you have your Pokémon"


def test_get_message_shiny():
        context = MagicMock()
        context.author.mention = "Author"
        message = pokemon_generator.get_message("shiny", context)
        assert message == "Author Here you have your ✨SHINY✨ Pokémon"


@patch("requests.get")
def test_get_varieties_request_code_is_not_200(mock_get: MagicMock):
        mock_get.return_value.status_code = 404

        with pytest.raises(VarietyFetchError):
                assert pokemon_generator.build_embed("normal", MagicMock()).title == "Error generating Pokémon data"


@patch("requests.get")
def test_get_varieties_when_connection_error(mock_get: MagicMock):
        mock_get.side_effect = requests.ConnectionError

        with pytest.raises(VarietyFetchError):
                assert pokemon_generator.build_embed("normal", MagicMock()).title == "Error generating Pokémon data"


@patch("requests.get")
def test_get_varieties_when_timeout_error(mock_get: MagicMock):
        mock_get.side_effect = requests.Timeout
        with pytest.raises(VarietyFetchError):
                assert pokemon_generator.build_embed("normal", MagicMock()).title == "Error generating Pokémon data"


def test_pokemon_creation_if_error_obtaining_nature():
        pokemon = PokemonBuilder().with_nature({}).build()

        assert pokemon.nature_name == "Unknown nature"
        assert pokemon.stats.increased is None
        assert pokemon.stats.decreased is None


def test_sprite_should_be_official_artwork():
        pokemon = PokemonBuilder().build()
        if pokemon.sprite is not None:
                assert "official-artwork" in pokemon.sprite
