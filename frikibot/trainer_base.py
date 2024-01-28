"""Contain trainer base pojo"""
from typing import Any

from sqlalchemy import Column, String

from frikibot.db_base import Base


class TrainerBase(Base):
    """Trainer POJO definition"""
    __tablename__ = "Trainers"
    id = Column(String(100), primary_key=True)
    name = Column(String(100), nullable=False)

    def __init__(self, trainer_id: str, name: str, **kw: Any):
        super().__init__(**kw)
        self.id = trainer_id
        self.name = name
