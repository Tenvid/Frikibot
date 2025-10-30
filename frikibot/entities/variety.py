"""Representation of a variety."""


class Variety:
        """Representation of a variety."""

        def __init__(self, is_default: bool, name: str, url: str):  # noqa: FBT001
                """
                Initialize a Variety instance.

                Args:
                ----
                        is_default (bool): Whether this variety is the default one.
                        name (str): The name of the variety.
                        url (str): The URL associated with the variety.

                """
                self.__is_default = is_default
                self.__name = name
                self.__url = url

        @property
        def is_default(self):
                """Return if variety is default."""
                return self.__is_default

        @is_default.setter
        def is_default(self, value: bool):
                """Set a new value for is_default."""
                if not isinstance(value, bool):
                        raise TypeError(f"Entered value: {value} is not valid for is_default")
                self.__is_default = value

        @property
        def name(self):
                """Return the name."""
                return self.__name

        @name.setter
        def name(self, value: str):
                """Set a new value for name."""
                if not isinstance(value, str):
                        raise TypeError(f"Entered value: {value} is not valid for name")
                self.__name = value

        @property
        def url(self):
                """Return the url."""
                return self.__url

        @url.setter
        def url(self, value: str):
                """Set a new value for url."""
                if not isinstance(value, str):
                        raise TypeError(f"Entered value: {value} is not valid for url")
                self.__url = value

        @classmethod
        def from_json(cls, json_data: dict):
                """Create a Variety instance from JSON data."""
                return cls(is_default=json_data["is_default"], name=json_data["pokemon"]["name"], url=json_data["pokemon"]["url"])
