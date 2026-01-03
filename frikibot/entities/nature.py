"""Nature representation."""

from typing import Any


class Nature:
        """Nature representation."""

        def __init__(self, *, name: str, decreased: str | None, increased: str | None):
                """Create a Nature."""
                self.__name = name
                self.__decreased = decreased
                self.__increased = increased

        @property
        def decreased(self) -> str | None:
                """The decreased stat."""
                return self.__decreased

        @property
        def increased(self) -> str | None:
                """The increased stat."""
                return self.__increased

        @property
        def name(self) -> str:
                """The name of the nature."""
                return self.__name

        @staticmethod
        def from_json(data: dict[str, Any]) -> "Nature":
                """Get an instance from JSON."""
                name = data["name"]
                decreased_stat = data.get("decreased_stat")
                increased_stat = data.get("increased_stat")

                return Nature(
                        name=name,
                        decreased=decreased_stat["name"] if decreased_stat else None,
                        increased=increased_stat["name"] if increased_stat else None,
                )

        def __repr__(self) -> str:
                """Return a string representation of the Nature."""
                return f"""
                Name: {self.name}
                Decreased stat: {self.decreased}
                Increased stat: {self.increased}
                """
