"""Pokemon ORM model definition."""

import sqlalchemy

from frikibot.infrastructure import database


class Pokemon(database.Base):
    """Pokemon ORM model."""

    __tablename__ = "pokemon"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column("Name", sqlalchemy.String, index=True)
    first_type = sqlalchemy.Column("Tipo1", sqlalchemy.String, index=True)
    second_type = sqlalchemy.Column("Tipo2", sqlalchemy.String, index=True, nullable=True)
    author_code = sqlalchemy.Column("Entrenador", sqlalchemy.String, index=True)
    move1 = sqlalchemy.Column("Move1", sqlalchemy.String, index=True)
    move2 = sqlalchemy.Column("Move2", sqlalchemy.String, index=True)
    move3 = sqlalchemy.Column("Move3", sqlalchemy.String, index=True)
    move4 = sqlalchemy.Column("Move4", sqlalchemy.String, index=True)
    nature_name = sqlalchemy.Column("Naturaleza", sqlalchemy.String, index=True)
