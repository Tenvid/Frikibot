from dataclasses import dataclass


@dataclass
class Movement:
    """Movement definition."""

    name: str
    accuracy: int
    description: str
    move_type: str
    category: str
    power: int
