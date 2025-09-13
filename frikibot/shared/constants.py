"""Script made by David Gómez."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
MAX_INDEX = 1010  # Pokedex number of the last Pokemon in Pokédex

TIMEOUT = 10  # HTTP request timeout

POKEMON_TABLE = os.getenv("POKEMON_TABLE")

DATABASE_FOLDER: Path = Path(
    str(os.getenv("DATABASE_FOLDER")) if os.getenv("DATABASE_FOLDER") else "db"
)

TRAINER_TABLE = os.getenv("TRAINER_TABLE")

if not DATABASE_FOLDER.exists():
    DATABASE_FOLDER.mkdir()

DATABASE: Path = Path(
    DATABASE_FOLDER / str(os.getenv("DATABASE"))
    if os.getenv("DATABASE")
    else "pokemon.db"
)
