"""Trainer ORM model."""

import sqlalchemy

from frikibot.infrastructure import database


class Trainer(database.Base):
    """Trainer ORM model."""

    __tablename__ = "trainer"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    trainer_name = sqlalchemy.Column(sqlalchemy.String, index=True)
    trainer_code = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    enabled = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
