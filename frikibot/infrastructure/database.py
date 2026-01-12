"""SQLAlchemy database configuration module."""

import logging
from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from collections.abc import Generator

    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine
engine = create_engine("sqlite:///db/pokemon.db")

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Flag to track if database has been initialized
_db_initialized = True


def initialize_database() -> None:
    """
    Initialize the database schema.

    This function should be called once when the application starts.
    It ensures all tables defined in the models are created in the database.

    """
    global _db_initialized

    if not _db_initialized:
        # Import here to avoid circular imports
        # The models module imports Base from this module

        logger.info("Initializing database schema")

        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized")

        _db_initialized = True
    else:
        logger.debug("Database already initialized")


def get_db() -> "Generator[Session, None, None]":
    """
    Get a database session.

    Yields
    ------
    Session
        A SQLAlchemy session

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
