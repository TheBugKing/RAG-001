"""
Abstract interface for vector store engine / client configuration.

This is the analogue of DatabaseEngineInterface, but for vector stores
like ChromaDB. It is responsible for:
- Initializing the underlying client / storage on startup
- Exposing a vector-store object that higher layers can use
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class VectorStoreEngineInterface(ABC):
    """
    Contract for vector store setup and access.

    Concrete implementations (e.g. Chroma engine) should:
    - Initialize the client / collections in init_store()
    - Return a repository-like object for vector operations
      from get_vector_store()
    """

    @abstractmethod
    def init_store(self) -> None:
        """
        Initialize the vector store.

        Examples:
        - Ensure persistence directory exists
        - Create or load collections
        Call once at application startup.
        """
        ...

    @abstractmethod
    def get_vector_store(self) -> Any:
        """
        Return an object that implements vector db session for vector data
        (e.g. a Chroma-backed implementation for embeddings).

        This is analogous to get_db() for relational storage, but returns
        a higher-level vector-store abstraction instead of a Session.
        """
        ...

