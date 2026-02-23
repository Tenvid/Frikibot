"""Pokemon ORM model definition."""

import sqlalchemy

from frikibot.infrastructure import database


class Pokemon(database.Base):
    """Pokemon ORM model."""

    __tablename__ = "pokemon"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
    first_type = sqlalchemy.Column(sqlalchemy.String, index=True)
    second_type = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    author_code = sqlalchemy.Column(sqlalchemy.String, index=True)
    move1 = sqlalchemy.Column(sqlalchemy.String, index=True)
    move2 = sqlalchemy.Column(sqlalchemy.String, index=True)
    move3 = sqlalchemy.Column(sqlalchemy.String, index=True)
    move4 = sqlalchemy.Column(sqlalchemy.String, index=True)
    nature_name = sqlalchemy.Column(sqlalchemy.String, index=True)
