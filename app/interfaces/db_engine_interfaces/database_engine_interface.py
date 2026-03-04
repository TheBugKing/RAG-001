"""
Abstract interface for database configuration and session provision.

Implementations: SQLite (engine + SessionLocal), MongoDB (MongoClient), etc.
CRUD (create/get/update/delete) is done via repositories that use the session
returned by get_db(); this interface only defines how to configure the DB
and obtain a session.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import Any


class DatabaseEngineInterface(ABC):
    """
    Contract for database setup and session provision.
    Concrete implementations (SQLite, MongoDB, Postgres, etc.) implement
    init_db() and get_db(); repositories then use the session for ORM/CRUD.
    """

    @abstractmethod
    def init_db(self) -> None:
        """
        Initialize the database (create tables, ensure dirs exist, etc.).
        Call once at application startup.
        """
        ...

    @abstractmethod
    def create_db_engine(self) -> None:
        """
        Create a database engine.
        """
        ...

    @abstractmethod
    def get_db(self) -> Generator[Any, None, None]:
        """
        Yield a session/connection for the current request.
        Caller (or FastAPI Depends) must consume once and will get the same
        session until the generator is exhausted; implementation should close
        the session in a finally block.
        """
        ...