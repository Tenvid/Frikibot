from typing import Any

from frikibot.variety_data import VarietyData


class VarietyDataBuilder:
    def __init__(self) -> None:
        self.available_abilities = [
            {
                "ability": {
                    "name": "steadfast",
                    "url": "https://pokeapi.co/api/v2/ability/80/",
                },
                "is_hidden": False,
                "slot": 1,
            },
            {
                "ability": {
                    "name": "inner-focus",
                    "url": "https://pokeapi.co/api/v2/ability/39/",
                },
                "is_hidden": False,
                "slot": 2,
            },
            {
                "ability": {
                    "name": "justified",
                    "url": "https://pokeapi.co/api/v2/ability/154/",
                },
                "is_hidden": True,
                "slot": 3,
            },
        ]

        self.available_moves = [
            {
                "move": {
                    "name": "mega-punch",
                    "url": "https://pokeapi.co/api/v2/move/5/",
                },
                "version_group_details": [
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "sword-shield",
                            "url": "https://pokeapi.co/api/v2/version-group/20/",
                        },
                    }
                ],
            },
            {
                "move": {
                    "name": "ice-punch",
                    "url": "https://pokeapi.co/api/v2/move/8/",
                },
                "version_group_details": [
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "platinum",
                            "url": "https://pokeapi.co/api/v2/version-group/9/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "heartgold-soulsilver",
                            "url": "https://pokeapi.co/api/v2/version-group/10/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "black-2-white-2",
                            "url": "https://pokeapi.co/api/v2/version-group/14/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "omega-ruby-alpha-sapphire",
                            "url": "https://pokeapi.co/api/v2/version-group/16/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "ultra-sun-ultra-moon",
                            "url": "https://pokeapi.co/api/v2/version-group/18/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "sword-shield",
                            "url": "https://pokeapi.co/api/v2/version-group/20/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "scarlet-violet",
                            "url": "https://pokeapi.co/api/v2/version-group/25/",
                        },
                    },
                ],
            },
            {
                "move": {
                    "name": "thunder-punch",
                    "url": "https://pokeapi.co/api/v2/move/9/",
                },
                "version_group_details": [
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "platinum",
                            "url": "https://pokeapi.co/api/v2/version-group/9/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "heartgold-soulsilver",
                            "url": "https://pokeapi.co/api/v2/version-group/10/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "black-2-white-2",
                            "url": "https://pokeapi.co/api/v2/version-group/14/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "omega-ruby-alpha-sapphire",
                            "url": "https://pokeapi.co/api/v2/version-group/16/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "tutor",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/3/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "ultra-sun-ultra-moon",
                            "url": "https://pokeapi.co/api/v2/version-group/18/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "sword-shield",
                            "url": "https://pokeapi.co/api/v2/version-group/20/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "scarlet-violet",
                            "url": "https://pokeapi.co/api/v2/version-group/25/",
                        },
                    },
                ],
            },
            {
                "move": {
                    "name": "swords-dance",
                    "url": "https://pokeapi.co/api/v2/move/14/",
                },
                "version_group_details": [
                    {
                        "level_learned_at": 33,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "diamond-pearl",
                            "url": "https://pokeapi.co/api/v2/version-group/8/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "diamond-pearl",
                            "url": "https://pokeapi.co/api/v2/version-group/8/",
                        },
                    },
                    {
                        "level_learned_at": 33,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "platinum",
                            "url": "https://pokeapi.co/api/v2/version-group/9/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "platinum",
                            "url": "https://pokeapi.co/api/v2/version-group/9/",
                        },
                    },
                    {
                        "level_learned_at": 33,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "heartgold-soulsilver",
                            "url": "https://pokeapi.co/api/v2/version-group/10/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "heartgold-soulsilver",
                            "url": "https://pokeapi.co/api/v2/version-group/10/",
                        },
                    },
                    {
                        "level_learned_at": 37,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "black-white",
                            "url": "https://pokeapi.co/api/v2/version-group/11/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "black-white",
                            "url": "https://pokeapi.co/api/v2/version-group/11/",
                        },
                    },
                    {
                        "level_learned_at": 37,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "black-2-white-2",
                            "url": "https://pokeapi.co/api/v2/version-group/14/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "black-2-white-2",
                            "url": "https://pokeapi.co/api/v2/version-group/14/",
                        },
                    },
                    {
                        "level_learned_at": 19,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "x-y",
                            "url": "https://pokeapi.co/api/v2/version-group/15/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "x-y",
                            "url": "https://pokeapi.co/api/v2/version-group/15/",
                        },
                    },
                    {
                        "level_learned_at": 19,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "omega-ruby-alpha-sapphire",
                            "url": "https://pokeapi.co/api/v2/version-group/16/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "omega-ruby-alpha-sapphire",
                            "url": "https://pokeapi.co/api/v2/version-group/16/",
                        },
                    },
                    {
                        "level_learned_at": 19,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "sun-moon",
                            "url": "https://pokeapi.co/api/v2/version-group/17/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "sun-moon",
                            "url": "https://pokeapi.co/api/v2/version-group/17/",
                        },
                    },
                    {
                        "level_learned_at": 19,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "ultra-sun-ultra-moon",
                            "url": "https://pokeapi.co/api/v2/version-group/18/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "ultra-sun-ultra-moon",
                            "url": "https://pokeapi.co/api/v2/version-group/18/",
                        },
                    },
                    {
                        "level_learned_at": 40,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "sword-shield",
                            "url": "https://pokeapi.co/api/v2/version-group/20/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "sword-shield",
                            "url": "https://pokeapi.co/api/v2/version-group/20/",
                        },
                    },
                    {
                        "level_learned_at": 40,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "brilliant-diamond-and-shining-pearl",
                            "url": "https://pokeapi.co/api/v2/version-group/23/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "brilliant-diamond-and-shining-pearl",
                            "url": "https://pokeapi.co/api/v2/version-group/23/",
                        },
                    },
                    {
                        "level_learned_at": 40,
                        "move_learn_method": {
                            "name": "level-up",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "scarlet-violet",
                            "url": "https://pokeapi.co/api/v2/version-group/25/",
                        },
                    },
                    {
                        "level_learned_at": 0,
                        "move_learn_method": {
                            "name": "machine",
                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                        },
                        "order": None,
                        "version_group": {
                            "name": "scarlet-violet",
                            "url": "https://pokeapi.co/api/v2/version-group/25/",
                        },
                    },
                ],
            },
        ]
        self.name = "lucario"
        self.combat_stats = [
            {
                "base_stat": 70,
                "effort": 0,
                "stat": {
                    "name": "hp",
                    "url": "https://pokeapi.co/api/v2/stat/1/",
                },
            },
            {
                "base_stat": 110,
                "effort": 1,
                "stat": {
                    "name": "attack",
                    "url": "https://pokeapi.co/api/v2/stat/2/",
                },
            },
            {
                "base_stat": 70,
                "effort": 0,
                "stat": {
                    "name": "defense",
                    "url": "https://pokeapi.co/api/v2/stat/3/",
                },
            },
            {
                "base_stat": 115,
                "effort": 1,
                "stat": {
                    "name": "special-attack",
                    "url": "https://pokeapi.co/api/v2/stat/4/",
                },
            },
            {
                "base_stat": 70,
                "effort": 0,
                "stat": {
                    "name": "special-defense",
                    "url": "https://pokeapi.co/api/v2/stat/5/",
                },
            },
            {
                "base_stat": 90,
                "effort": 0,
                "stat": {
                    "name": "speed",
                    "url": "https://pokeapi.co/api/v2/stat/6/",
                },
            },
        ]
        self.types = [
            {
                "slot": 1,
                "type": {
                    "name": "fighting",
                    "url": "https://pokeapi.co/api/v2/type/2/",
                },
            },
            {
                "slot": 2,
                "type": {
                    "name": "steel",
                    "url": "https://pokeapi.co/api/v2/type/9/",
                },
            },
        ]
        self.available_sprites = {
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/448.png",
            "back_female": None,
            "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/448.png",
            "back_shiny_female": None,
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/448.png",
            "front_female": None,
            "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/448.png",
            "front_shiny_female": None,
            "other": {
                "dream_world": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/448.svg",
                    "front_female": None,
                },
                "home": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/448.png",
                    "front_female": None,
                    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/448.png",
                    "front_shiny_female": None,
                },
                "official-artwork": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
                    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/448.png",
                },
                "showdown": {
                    "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/448.gif",
                    "back_female": None,
                    "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/back/shiny/448.gif",
                    "back_shiny_female": None,
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/448.gif",
                    "front_female": None,
                    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/shiny/448.gif",
                    "front_shiny_female": None,
                },
            },
        }

    def build(self):
        return VarietyData(
            available_abilities=self.available_abilities,
            available_moves=self.available_moves,
            name=self.name,
            combat_stats=self.combat_stats,
            types=self.types,
            available_sprites=self.available_sprites,
        )

    def with_available_sprites(self, value: Any):
        self.available_sprites = value
        return self


def test_sprite_url_should_be_official_artwork_default():
    variety = VarietyDataBuilder().build()
    assert (
        variety.get_official_artwork_sprite("default")
        == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png"
    )


def test_sprite_url_should_be_official_artwork_shiny():
    variety = VarietyDataBuilder().build()
    assert (
        variety.get_official_artwork_sprite("shiny")
        == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/448.png"
    )


def test_sprite_url_should_return_none_if_there_is_no_official_artwork():
    variety = VarietyDataBuilder().with_available_sprites({}).build()
    assert variety.get_official_artwork_sprite("default") is None
