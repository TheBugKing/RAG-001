"""
Abstract CRUD-like interface for a vector store (e.g. ChromaDB).

This is intentionally separate from the relational CRUDInterface because
vector stores operate on embeddings and similarity search instead of
row-based filters only.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class VectorStoreCRUDInterface(ABC):
    """
    Contract for basic vector store operations:
    - add vectors
    - query nearest neighbors
    - delete vectors
    Implementations can wrap ChromaDB, FAISS, etc.
    """

    @abstractmethod
    def insert(
        self,
        ids: list[str],
        embeddings: list[list[float]] | None,
        metadatas: list[dict[str, Any]] | None = None,
        documents: list[str] | None = None,
    ) -> None:
        """
        Insert (or upsert) vectors into the store.
        All lists must be the same length.
        """
        ...

    @abstractmethod
    def select(
        self,
        query_embeddings: list[list[float]],
        n_results: int = 5,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Query nearest neighbors for the given query embeddings.

        Implementations should return a dict containing at least:
        - ids: list[list[str]]
        - distances: list[list[float]]  (or similar score)
        - metadatas: list[list[dict]]   (if available)
        - documents: list[list[str]]    (if available)
        """
        ...

    @abstractmethod
    def get(
        self,
        ids: list[str] | None = None,
        where: dict[str, Any] | None = None,
        include: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Fetch records by id and/or metadata filter without similarity search.

        Implementations should return a dict compatible with the underlying
        vector store's get API (e.g. Chroma's collection.get()).
        """
        ...

    @abstractmethod
    def upsert(
        self,
        ids: list[str],
        embeddings: list[list[float]] | None,
        metadatas: list[dict[str, Any]] | None = None,
        documents: list[str] | None = None,
    ) -> None:
        """
        Insert or update vectors in the store.

        Implementations can either:
        - call a native upsert API (as Chroma does), or
        - implement this as delete(ids) + insert(...)
        """
        ...

    @abstractmethod
    def delete(
        self,
        ids: list[str] | None = None,
        where: dict[str, Any] | None = None,
    ) -> None:
        """
        Delete vectors from the store by ids and/or metadata filter.
        """
        ...

