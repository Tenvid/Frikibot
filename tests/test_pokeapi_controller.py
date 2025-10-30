"""Tests for PokeAPIController."""

from unittest.mock import Mock, patch

import pytest

from frikibot.controller.pokeapi_controller import PokeAPIController
from frikibot.entities.variety import Variety
from frikibot.exceptions import VarietyDetailsFetchError, VarietyFetchError


@pytest.fixture()
def controller():
        """Fixture to create a PokeAPIController instance."""
        return PokeAPIController()


@pytest.fixture()
def mock_variety():
        """Fixture to create a mock Variety object."""
        variety = Mock(spec=Variety)
        variety.url = "https://pokeapi.co/api/v2/pokemon/1/"
        return variety


@patch("requests.get")
def test_fetch_variety_details_success(mock_get, controller, mock_variety):
        """Test successful fetch of variety details."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "bulbasaur", "id": 1}
        mock_get.return_value = mock_response

        result = controller.fetch_variety_details(mock_variety)

        assert result == {"name": "bulbasaur", "id": 1}


@patch("requests.get")
def test_fetch_variety_details_connection_error(mock_get, controller, mock_variety):
        """Test that VarietyDetailsFetchError is raised on ConnectionError."""
        from requests.exceptions import ConnectionError

        mock_get.side_effect = ConnectionError("ConnectionError")

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
