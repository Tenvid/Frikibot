from unittest.mock import Mock, MagicMock, patch
import frikibot.pokemon_generator
import random


@patch("pokemon_generator.get_pokemon_stats")
def test_get_stats_string_with_neutral_nature(mock_stats):
    mock_stats.return_value = {
        "Attack": 0,
        "Defense": 0,
        "Special attack": 0,
        "Special defense": 0,
        "Speed": 0,
    }

    stats_string = pokemon_generator.get_stats_string("", None, None)

    assert isinstance(stats_string, str)
    assert (
        stats_string
        == "```ansi\nAttack: 0\nDefense: 0\nSpecial attack: 0\nSpecial defense: 0\nSpeed: 0\n```"
    )


@patch("pokemon_generator.get_pokemon_stats")
def test_get_stats_string_with_non_neutral_nature(mock_stats):
    mock_stats.return_value = {
        "Attack": 0,
        "Defense": 0,
        "Special attack": 0,
        "Special defense": 0,
        "Speed": 0,
    }

    stats_string = pokemon_generator.get_stats_string("", "Special attack", "Defense")

    assert isinstance(stats_string, str)
    assert (
        stats_string
        == "```ansi\nAttack: 0\n\x1b[0;31mDefense: 0 +\x1b[0;0m\n\x1b[0;34mSpecial attack: 0 -\x1b[0;0m\nSpecial defense: 0\nSpeed: 0\n```"
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

    stats = pokemon_generator.get_pokemon_stats("lucario")
    assert isinstance(stats, dict)
    assert stats["Hp"] == 70
    assert stats["Attack"] == 110
    assert stats["Defense"] == 70
    assert stats["Special attack"] == 115
    assert stats["Special defense"] == 70
    assert stats["Speed"] == 90


@patch("requests.get")
def test_get_moves_string(mock_get):
    mock_get.return_value.text = """
{
  "moves": [
    {
      "move": {
        "name": "swords-dance"
      }
    },
    {
      "move": {
        "name": "aura-sphere"
      }
    },
    {
      "move": {
        "name": "close-combat"
      }
    },
    {
      "move": {
        "name": "iron-head"
      }
    }
  ]
}
    """

    moves_string = pokemon_generator.get_moves_string("lucario")

    moves_list = moves_string.replace("`", "").split("\n")

    for move in moves_list:
        assert move in ["Swords dance", "Aura sphere", "Close combat", "Iron head"]


def test_get_changed_stats_non_neutral_nature():
    mocked_nature = {
        "increased_stat": {"name": "defense"},
        "decreased_stat": {"name": "special-attack"},
    }

    decreased, increased = pokemon_generator.get_changed_stats(mocked_nature)

    assert increased == "Defense"
    assert decreased == "Special attack"


def test_eliminate_invalid_forms():
    pass


@patch("requests.get")
def test_correct_name_pikachu(mock_get):
    mock_get.return_value.text = """
        {
    "varieties": [
        {
            "pokemon": {"name": "pikachu1"},
        },
        {
            "pokemon": {"name": "pikachu2"},
        },
        {
            "pokemon": {"name": "pikachu3"},
        },
        {
            "pokemon": {"name": "pikachu4"},
        },
        {
            "pokemon": {"name": "pikachu5"},
        },
        {
            "pokemon": {"name": "pikachu6"},
        },
        {
            "pokemon": {"name": "pikachu7"},
        },
        {
            "pokemon": {"name": "pikachu8"},
        },
        {
            "pokemon": {"name": "pikachu9"},
        },
        {
            "pokemon": {"name": "pikachu10"},
        },
        {
            "pokemon": {"name": "pikachu11"},
        },
        {
            "pokemon": {"name": "pikachu12"},
        },
        {
            "pokemon": {"name": "pikachu13"},
        },
        {
            "pokemon": {"name": "pikachu14"},
        },
        {
            "pokemon": {"name": "pikachu15"},
        },
        {
            "pokemon": {"name": "pikachu16"},
        },
    ]
  }
        """

    # varieties = [
    #     {
    #         "is_default": True,
    #         "pokemon": {
    #             "name": "pikachu",
    #             "url": "https://pokeapi.co/api/v2/pokemon/25/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-rock-star",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10080/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-belle",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10081/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-pop-star",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10082/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-phd",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10083/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-libre",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10084/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-cosplay",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10085/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-original-cap",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10094/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-hoenn-cap",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10095/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-sinnoh-cap",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10096/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-unova-cap",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10097/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-kalos-cap",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10098/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-alola-cap",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10099/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-partner-cap",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10148/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-starter",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10158/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-world-cap",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10160/",
    #         },
    #     },
    #     {
    #         "is_default": False,
    #         "pokemon": {
    #             "name": "pikachu-gmax",
    #             "url": "https://pokeapi.co/api/v2/pokemon/10199/",
    #         },
    #     },
    # ]

    varieties = [
        {
            "pokemon": {"name": "pikachu1"},
        },
        {
            "pokemon": {"name": "pikachu2"},
        },
        {
            "pokemon": {"name": "pikachu3"},
        },
        {
            "pokemon": {"name": "pikachu4"},
        },
        {
            "pokemon": {"name": "pikachu5"},
        },
        {
            "pokemon": {"name": "pikachu6"},
        },
        {
            "pokemon": {"name": "pikachu7"},
        },
        {
            "pokemon": {"name": "pikachu8"},
        },
        {
            "pokemon": {"name": "pikachu9"},
        },
        {
            "pokemon": {"name": "pikachu10"},
        },
        {
            "pokemon": {"name": "pikachu11"},
        },
        {
            "pokemon": {"name": "pikachu12"},
        },
        {
            "pokemon": {"name": "pikachu13"},
        },
        {
            "pokemon": {"name": "pikachu14"},
        },
        {
            "pokemon": {"name": "pikachu15"},
        },
        {
            "pokemon": {"name": "pikachu16"},
        },
    ]

    for variety in varieties:
        name = pokemon_generator.correct_name(
            variety["pokemon"]["name"], varieties=varieties, variety=variety
        )
        assert name != varieties[1]["pokemon"]["name"]
        assert name != varieties[2]["pokemon"]["name"]
        assert name != varieties[3]["pokemon"]["name"]
        assert name != varieties[4]["pokemon"]["name"]
        assert name != varieties[5]["pokemon"]["name"]
        assert name != varieties[6]["pokemon"]["name"]
        assert name != varieties[14]["pokemon"]["name"]


def test_correct_name_minior_meteor():
    varieties = [{"pokemon": {"name": "minior-foo-meteor"}}]

    name = pokemon_generator.correct_name(
        "minior-foo-meteor", varieties, random.choice(varieties)
    )

    assert name == "minior-meteor"


def test_correct_name_minior_core():
    varieties = [
        {"pokemon": {"name": "minior-foo"}},
        {"pokemon": {"name": "minior-bar"}},
    ]
    for variety in varieties:
        name = pokemon_generator.correct_name(
            variety["pokemon"]["name"], varieties, variety
        )

        assert name == variety["pokemon"]["name"] + "-core"


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


def test_generate_random_pokemon():
    pass


@patch("discord.ext.commands.Context")
def test_get_message_non_shiny(mock_mention):
    mock_mention.author.mention = "Author"
    msg = pokemon_generator.get_message(colour="normal", ctx=mock_mention)

    assert msg == "Author Here you have your Pokémon"


@patch("discord.ext.commands.Context")
def test_get_message_shiny(mock_mention):
    mock_mention.author.mention = "Author"
    msg = pokemon_generator.get_message(colour="shiny", ctx=mock_mention)

    assert msg == "Author Here you have your ✨SHINY✨ Pokémon"


def test_get_changed_stats_neutral_nature():
    mocked_nature = {
        "increased_stat": None,
        "decreased_stat": None,
    }

    decreased, increased = pokemon_generator.get_changed_stats(mocked_nature)

    assert decreased is None
    assert increased is None


@patch("requests.Response")
def test_load_pokemon(mock_loads):
    mock_loads.return_value.text = """{"name": "PokeName"}"""

    load = pokemon_generator.load_pokemon(pokemon_generator.requests.Response())

    assert load["name"] == "PokeName"


@patch("requests.get")
@patch("pokemon_generator.pick_nature")
def test_get_nature(mock_pick, mock_get):
    response_mock = MagicMock()

    response_mock.text = """
    {
        "results": [
            {
                "name": "Hardy",
                "decreases": "Attack",
                "increases": "Defense"
            },
            {
                "name": "Docile",
                "decreases": "None",
                "increases": "None"
            }
        ]
    }
    """

    mock_get.return_value = response_mock

    mock_pick.return_value = {
        "name": "Docile",
        "decreases": "None",
        "increases": "None",
    }

    nature = pokemon_generator.get_nature()

    assert isinstance(nature, dict)
    assert nature["increases"] == "None"
    assert nature["decreases"] == "None"


@patch("requests.get")
def test_pick_nature_neutral_nature(mock_get):
    natures = {
        "results": [
            {"name": "Hardy", "decreases": "Attack", "increases": "Defense", "url": ""},
            {"name": "Docile", "decreases": "None", "increases": "None", "url": ""},
        ]
    }

    response_mock = Mock()

    response_mock.text = '{"name": "Docile", "decreases": "None", "increases": "None"}'

    mock_get.return_value = response_mock
    nature = pokemon_generator.pick_nature(natures)

    assert isinstance(nature, dict)
    assert nature["name"] == "Docile"
    assert nature["decreases"] == "None"
    assert nature["increases"] == "None"


@patch("requests.get")
def test_pick_nature_non_neutral_nature(mock_get):
    natures = {
        "results": [
            {"name": "Hardy", "decreases": "Attack", "increases": "Defense", "url": ""},
            {"name": "Docile", "decreases": "None", "increases": "None", "url": ""},
        ]
    }

    response_mock = Mock()

    response_mock.text = (
        '{"name": "Hardy", "decreases": "Attack", "increases": "Defense", "url": ""}'
    )

    mock_get.return_value = response_mock
    nature = pokemon_generator.pick_nature(natures)

    assert isinstance(nature, dict)
    assert nature["name"] == "Hardy"
    assert nature["decreases"] == "Attack"
    assert nature["increases"] == "Defense"
