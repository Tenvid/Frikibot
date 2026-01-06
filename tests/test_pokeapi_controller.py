"""Tests for PokeAPIController."""

from unittest.mock import Mock, patch

import pytest

from frikibot.controller.pokeapi_controller import PokeAPIController
from frikibot.entities.variety import Variety
from frikibot.shared.exceptions import VarietyDetailsFetchError, VarietyFetchError


@pytest.fixture
def controller():
    """Fixture to create a PokeAPIController instance."""
    return PokeAPIController()


@pytest.fixture
def mock_variety():
    """Fixture to create a mock Variety object."""
    variety = Mock(spec=Variety)
    variety.url = "https://pokeapi.co/api/v2/pokemon/1/"
    return variety


@pytest.fixture
def mock_detailed_variety_response():
    return {
        "is_default": True,
        "name": "riolu",
        "species": {"url": "https://pokeapi.co/api/v2/pokemon-species/447/"},
        "abilities": [
            {"ability": {"name": "steadfast", "url": "https://pokeapi.co/api/v2/ability/80/"}, "is_hidden": False, "slot": 1},
            {"ability": {"name": "inner-focus", "url": "https://pokeapi.co/api/v2/ability/39/"}, "is_hidden": False, "slot": 2},
            {"ability": {"name": "prankster", "url": "https://pokeapi.co/api/v2/ability/158/"}, "is_hidden": True, "slot": 3},
        ],
        "moves": [{"move": {"name": "pound", "url": "https://pokeapi.co/api/v2/move/1/"}, "version_group_details": []}],
        "stats": [
            {"base_stat": 40, "effort": 0, "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"}},
            {"base_stat": 70, "effort": 0, "stat": {"name": "attack", "url": "https://pokeapi.co/api/v2/stat/2/"}},
            {"base_stat": 40, "effort": 0, "stat": {"name": "defense", "url": "https://pokeapi.co/api/v2/stat/3/"}},
            {"base_stat": 35, "effort": 0, "stat": {"name": "special-attack", "url": "https://pokeapi.co/api/v2/stat/4/"}},
            {"base_stat": 40, "effort": 0, "stat": {"name": "special-defense", "url": "https://pokeapi.co/api/v2/stat/5/"}},
            {"base_stat": 60, "effort": 1, "stat": {"name": "speed", "url": "https://pokeapi.co/api/v2/stat/6/"}},
        ],
        "types": [{"slot": 1, "type": {"name": "fighting", "url": "https://pokeapi.co/api/v2/type/2/"}}],
        "sprites": {
            "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/447.png",
            "back_female": None,
            "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/447.png",
            "back_shiny_female": None,
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/447.png",
            "front_female": None,
            "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/447.png",
            "front_shiny_female": None,
            "other": {
                "dream_world": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/447.svg",
                    "front_female": None,
                },
                "home": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/447.png",
                    "front_female": None,
                    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/447.png",
                    "front_shiny_female": None,
                },
                "official-artwork": {
                    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/447.png",
                    "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/447.png",
                },
            },
            "versions": {},
        },
    }


@patch("requests.get")
def test_fetch_variety_details_success(mock_get, controller, mock_variety, mock_detailed_variety_response):
    """Test successful fetch of variety details."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_detailed_variety_response
    mock_get.return_value = mock_response

    variety_details = controller.fetch_variety_details(mock_variety)

    mock_get.assert_called_once_with(mock_variety.url, timeout=10)
    assert variety_details.is_default == mock_detailed_variety_response["is_default"]
    assert variety_details.name == mock_detailed_variety_response["name"]
    assert variety_details.url == mock_detailed_variety_response["species"]["url"]
    assert variety_details.available_abilities == mock_detailed_variety_response["abilities"]
    assert variety_details.available_moves == mock_detailed_variety_response["moves"]
    assert variety_details.combat_stats == mock_detailed_variety_response["stats"]
    assert variety_details.types == mock_detailed_variety_response["types"]
    assert variety_details.available_sprites == mock_detailed_variety_response["sprites"]


@patch("requests.get")
def test_fetch_variety_details_connection_error(mock_get, controller, mock_variety):
    """Test that VarietyDetailsFetchError is raised on ConnectionError."""
    from requests import exceptions

    mock_get.side_effect = exceptions.ConnectionError("ConnectionError")

    with pytest.raises(VarietyDetailsFetchError) as exc_info:
        controller.fetch_variety_details(mock_variety)

    assert "Connection error happened trying to get details of variety" in str(exc_info.value)


@patch("requests.get")
def test_fetch_variety_details_timeout_error(mock_get, controller, mock_variety):
    """Test that VarietyDetailsFetchError is raised on Timeout."""
    from requests.exceptions import Timeout

    mock_get.side_effect = Timeout()

    with pytest.raises(VarietyDetailsFetchError) as exc_info:
        controller.fetch_variety_details(mock_variety)

    assert "Timeout error happened trying to get details of variety" in str(exc_info.value)


@patch("requests.get")
def test_fetch_variety_details_non_200_status(mock_get, controller, mock_variety):
    """Test that VarietyFetchError is raised when status code is not 200."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(VarietyFetchError) as exc_info:
        controller.fetch_variety_details(mock_variety)

    assert "Failed fetching variety details from variety" in str(exc_info.value)
    assert "Response status code: 404" in str(exc_info.value)
