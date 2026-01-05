"""Custom exceptions."""


class VarietyFetchError(Exception):
    """Raises when failing trying to fetch varieties of a Pokémon."""

    def __init__(self, *args: object):
        """Init."""
        super().__init__(*args)


class VarietyDetailsFetchError(Exception):
    """Raises when failing trying to fetch details of a variety."""

    def __init__(self, *args: object):
        """Init."""
        super().__init__(*args)


class NatureFetchError(Exception):
    """Raises when failing trying to fetch nature data."""

    def __init__(self, *args: object):
        """Init."""
        super().__init__(*args)
