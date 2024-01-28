"""Manager of database"""
import enum
import json
import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from frikibot.db_base import Base
from frikibot.pokemon_base import PokemonBase
from frikibot.trainer_base import TrainerBase

load_dotenv()


class DBElements(enum.Enum):
    """Enum containing the elements of the database url"""
    HOST: str = os.getenv("DATABASE_HOST")
    PORT: int = os.getenv("DATABASE_PORT")
    DATABASE: str = os.getenv("DATABASE_DATABASE")
    USER: str = os.getenv("DATABASE_USER")
    PASSWORD: str = os.getenv("DATABASE_PASSWORD")


DATABASE_NAME = DBElements.DATABASE.value

engine = create_engine(
    f"postgresql://{DBElements.USER.value}:{DBElements.PASSWORD.value}@{DBElements.HOST.value}"
    f":{DBElements.PORT.value}/{DATABASE_NAME}"
    )

Session = sessionmaker(bind=engine)
session = Session()


def _create_tables(connection, model: Base):
    """Create all the tables"""
    model.metadata.drop_all(connection)
    model.metadata.create_all(connection)


def _insert_pokemon(pokemon_data: str, trainer_code: int, move_list, nature):
    """Create a Pokémon and insert into the database."""
    data_dict = json.loads(pokemon_data)
    _name = str(data_dict["name"]).capitalize()
    _moves = move_list
    _nature = nature
    session.add(PokemonBase(data=pokemon_data,
                            trainer_id=trainer_code,
                            name=_name,
                            moves=_moves,
                            nature=_nature)
                            )
    session.commit()
    logging.info("Pokemon added to database")


def _insert_trainer(trainer_name: str, trainer_id: str):
    """
    Inserts a trainer in the database
    :param trainer_name: Name of the trainer
    :param trainer_id: Discord id of the trainer
    """
    statement = session.query(TrainerBase).where(TrainerBase.id == str(trainer_id))
    logging.debug("Statement done")

    result = session.execute(statement)
    logging.debug("Result obtained")

    if len(result.scalars().all()) < 1:
        session.add(TrainerBase(name=trainer_name, trainer_id=trainer_id))
        session.commit()
        logging.info("Trainer added to database")
    else:
        logging.info(f"Trainer {trainer_name}: {trainer_id} Already exists, omitting insertion")


def insert_registry(author, pokemon_data, move_list, nature):
    """Insert Pokémon and trainer."""

    _insert_trainer(trainer_name=author.global_name, trainer_id=author.id)
    _insert_pokemon(pokemon_data=pokemon_data,
                    trainer_code=author.id,
                    move_list=move_list,
                    nature=nature)

def get_all_pokemon_from_trainer(trainer_id: str):
    """Query the database to get all Pokémon from a trainer."""
    msg = ""
    statement = session.query(PokemonBase).where(PokemonBase.trainer_id == str(trainer_id))
    result = session.execute(statement)

    for item in result.scalars().all():
        msg += str(item.id) + "\n"

    return msg
