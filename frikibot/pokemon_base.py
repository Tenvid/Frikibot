"""Contain Pokémon base definition"""
from sqlalchemy import Column, BigInteger, JSON, String

from frikibot.db_base import Base


class PokemonBase(Base):
    """Pokémon POJO definition"""
    __tablename__ = "CatchedPokemon"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False)
    name = Column(String(20), nullable=False)
    nature = Column(String(15), nullable=False)
    trainer_id = Column(String(100), nullable=False)

    def __str__(self):
        return f"""
                ID: {self.id}
                DATA: {self.data}
                TRAINER: {self.trainer_id}
                """

    def __init__(self, data: str, trainer_id: int, name: str, moves: [], nature:str):
        self.data = data
        self.trainer_id = trainer_id
        self.name = name
        self.moves = moves
        self.nature = nature
