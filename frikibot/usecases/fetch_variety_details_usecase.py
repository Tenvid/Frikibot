"""Use case for fetching variety details."""

import requests

from frikibot.entities.variety import Variety
from frikibot.entities.variety_details import VarietyDetails
from frikibot.shared.exceptions import VarietyDetailsFetchError, VarietyFetchError
from frikibot.shared.global_variables import TIMEOUT


class FetchVarietyDetailsUseCase:
    """Use case for fetching variety details."""

    def execute(self, variety: Variety) -> VarietyDetails:
        """
        Execute the use case to fetch variety details.

        Args:
        ----
            variety (Variety): The variety to fetch details for.

        Returns:
        -------
            VarietyDetails: The details of the variety.

        """
        try:
            raw_response = requests.get(variety.url, timeout=TIMEOUT)
            if raw_response.status_code == 200:
                json_response = raw_response.json()
                return VarietyDetails.from_json(json_response)
        except requests.ConnectionError as exc:
            raise VarietyDetailsFetchError(f"Connection error happened trying to get details of variety: {variety}") from exc
        except requests.Timeout as exc:
            raise VarietyDetailsFetchError(f"Timeout error happened trying to get details of variety: {variety}") from exc
        raise VarietyFetchError(f"Failed fetching variety details from variety: {variety} . Response status code: {raw_response.status_code}")
