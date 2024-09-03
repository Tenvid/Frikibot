from unittest.mock import Mock, MagicMock, patch

import pytest
from frikibot import pokemon_generator
from frikibot.stats import Stats
import random
import json


@patch("frikibot.pokemon_generator.get_pokemon_stats")
def test_get_stats_string_with_neutral_nature(mock_stats):
    mock_stats.return_value = Stats(0, 0, 0, 0, 0, 0, None, None)
    stats_string = pokemon_generator.get_stats_string("", None, None)

    assert isinstance(stats_string, str)
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


@patch("frikibot.pokemon_generator.get_pokemon_stats")
def test_get_stats_string_with_non_neutral_nature(mock_stats):
    mock_stats.return_value = Stats(0, 0, 0, 0, 0, 0, "special-attack", "defense")

    stats_string = pokemon_generator.get_stats_string("", "special-attack", "defense")

    assert isinstance(stats_string, str)
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


@patch("requests.get")
def test_get_pokemon_stats(mock_get):
    mock_get.return_value.text = """
    {"stats": [
    {
      "base_stat": 70
    },
    {
      "base_stat": 110
    },
    {
      "base_stat": 70
    },
    {
      "base_stat": 115
    },
    {
      "base_stat": 70
    },
    {
      "base_stat": 90
    }]
    }"""

    stats = pokemon_generator.get_pokemon_stats("lucario", None, None)
    assert type(stats) is Stats
    assert stats.hp == 70
    assert stats.attack == 110
    assert stats.defense == 70
    assert stats.special_attack == 115
    assert stats.special_defense == 70
    assert stats.speed == 90


@patch("frikibot.pokemon_generator.get_pokemon_moves")
def test_get_moves_string(mock_get):
    mock_get.return_value = ["Swords dance", "Aura sphere", "Close combat", "Iron head"]

    moves_string = pokemon_generator.get_moves_string("lucario")

    assert (
        moves_string
        == """```
Swords dance
Aura sphere
Close combat
Iron head```"""
    )


def test_get_changed_stats_non_neutral_nature():
    mocked_nature = {
        "increased_stat": {"name": "defense"},
        "decreased_stat": {"name": "special-attack"},
    }

    decreased, increased = pokemon_generator.get_changed_stats(mocked_nature)

    assert increased == "defense"
    assert decreased == "special-attack"

def test_correct_name_pikachu():
    varieties = []
    for i in range(15):
        varieties.append({"pokemon": {"name": f"pikachu{i}"}})

    for i in range(15):
        corrected = pokemon_generator.correct_name(
            f"pikachu{i}",
            varieties=varieties,
            variety={"pokemon": {"name": f"pikachu{i}"}},
        )

        assert (
            varieties.index({"pokemon": {"name": corrected}}) < 6
            or varieties.index({"pokemon": {"name": corrected}}) > 1
        ) and varieties.index({"pokemon": {"name": corrected}}) != 14


def test_correct_name_minior_meteor():
    varieties = [{"pokemon": {"name": "minior-meteor"}}]

    assert (
        pokemon_generator.correct_name("minior-foobar-meteor", varieties, varieties[0])
        == "minior-meteor"
    )


def test_correct_name_minior_core():
    varieties = [{"pokemon": {"name": "minior-example"}}]

    assert (
        pokemon_generator.correct_name("minior-example", varieties, varieties[0])
        == "minior-example-core"
    )


@patch("frikibot.pokemon_generator.randbelow")
def test_get_shiny_chance_shiny(mock_random):
    for i in range(10):
        mock_random.return_value = i

        colour = pokemon_generator.get_shiny_chance()
        assert colour == "shiny"


@patch("frikibot.pokemon_generator.randbelow")
def test_get_shiny_chance_not_shiny(mock_random):
    for i in range(11, 101):
        mock_random.return_value = i

        colour = pokemon_generator.get_shiny_chance()
        assert colour == "normal"


def test_get_random_move():
    move_list = [{"move": {"name": "my-move"}}]

    move = pokemon_generator.get_random_move(move_list)

    assert move == "My move"


@patch("requests.get")
def test_get_pokemon_moves(mock_get):
    mock_get.return_value.text = """
    {
      "moves" : [
        {
          "move" : {
            "name" : "Move1"
          }
        },
        {
          "move" : {
            "name" : "Move2"
          }
        },
        {
          "move" : {
            "name" : "Move3"
          }
        },
        {
          "move" : {
            "name" : "Move4"
          }
        }
      ]
    }
    """

    moves_list = ["Move1", "Move2", "Move3", "Move4"]

    moves = pokemon_generator.get_pokemon_moves("poke_name")

    for move in moves_list:
        assert move in moves


@patch("requests.get")
def test_get_pokemon_moves_index_error(
    mock_get,
):  # TODO: Make test more realistic (requests.get cannot raise IndexError)
    mock_get.side_effect = IndexError

    foo = pokemon_generator.get_pokemon_moves("foo")
    assert not foo


@patch("frikibot.pokemon_generator.get_message")
@patch("frikibot.pokemon_generator.build_embed")
def test_generate_random_pokemon(mock_embed: MagicMock, mock_message: MagicMock):
    mock_context = MagicMock()
    mock_embed.return_value = None
    mock_message.return_value = None
    _, _ = pokemon_generator.generate_random_pokemon(mock_context)
    mock_embed.assert_called_once()
    mock_message.assert_called_once()



@patch("frikibot.pokemon_generator.randbelow")
@patch("frikibot.pokemon_generator.create_pokemon")
@patch("frikibot.pokemon_generator.generate_pokemon_types")
@patch("frikibot.pokemon_generator.get_pokemon_stats")
@patch("frikibot.pokemon_generator.get_pokemon_moves")
@patch("frikibot.pokemon_generator.correct_name")
@patch("frikibot.pokemon_generator.get_nature")
@patch("requests.get")
def test_build_embed(
    mock_get: MagicMock,
    mock_nature: MagicMock,
    mock_name: MagicMock,
    mock_moves: MagicMock,
    mock_pokemon_stats: MagicMock,
    mock_types: MagicMock,
    mock_create_pokemon: MagicMock,
    mock_randbelow: MagicMock,
):
    mock_create_pokemon.return_value = None

    mock_context = MagicMock()
    mock_context.author.id = "author_id"

    mock_randbelow.return_value = 0

    mock_get.return_value.text = """
    {
        "varieties": [
            {
                "pokemon": {
                    "name": "Pokexample"
                }
            }
        ]
    }
    """

    mock_nature.return_value = {
        "name": "pokemon_nature",
        "decreased_stat": None,
        "increased_stat": None,
    }

    mock_name.return_value = "pokemon_name"

    mock_moves.return_value = ["A", "B", "C", "D"]

    mock_pokemon_stats.return_value = Stats(0, 0, 0, 0, 0, 0, None, None)

    mock_types.return_value = [{"type": {"name": "type1"}}, {"type": {"name": "type2"}}]

    embed = pokemon_generator.build_embed("normal", mock_context)

    mock_create_pokemon.assert_called_once()

    fields = embed.fields

    assert fields[0].name == "Moves"
    assert (
        fields[0].value
        == """```
A
B
C
D```"""
    )
    assert fields[1].name == "Stats"
    assert (
        fields[1].value
        == """```ansi
Hp: 0
Attack: 0
Defense: 0
Special attack: 0
Special defense: 0
Speed: 0```"""
    )

    assert embed.title == f"# 1 *Pokemon_nature* Pokexample"
    assert (
        embed.image.url
        == "https://img.pokemondb.net/sprites/home/normal/pokemon_name.png"
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


def test_get_changed_stats_neutral_nature():
    mocked_nature = {
        "increased_stat": None,
        "decreased_stat": None,
    }

    decreased, increased = pokemon_generator.get_changed_stats(mocked_nature)

    assert decreased is None
    assert increased is None


@patch("frikibot.pokemon_generator.pick_nature")
def test_get_nature(mock_get):
    mock_get.return_value = {"name": "n1", "url": "some-url.com"}

    nature = pokemon_generator.get_nature()
    assert nature["name"] == "n1"


@patch("requests.get")
def test_pick_nature(mock_get):
    natures = {
        "results": [{"name": "hardy", "url": "https://pokeapi.co/api/v2/nature/1/"}]
    }

    mock_get.return_value.text = '{"name": "hardy"}'

    nature = pokemon_generator.pick_nature(natures)
    assert nature["name"] == "hardy"


@patch("requests.get")
def test_generate_pokemon_types(mock_get):
    mock_get.return_value.text = """{
    "types": [
            {"type": {"name": "fire"}},
            {"type": {"name": "water"}}
        ]
        }
    """
    types = pokemon_generator.generate_pokemon_types({"pokemon": {"url": ""}})
    assert types[0]["type"]["name"] == "fire" or "water"
    assert types[1]["type"]["name"] == "fire" or "water"


@patch("requests.get")
def test_generate_pokemon_types_key_error(mock_get):
    mock_get.side_effect = KeyError

    foo = pokemon_generator.generate_pokemon_types(dict())

    assert foo is None
