"""
ChromaDB-backed implementation of VectorStoreCRUDInterface.

This repository wraps a single Chroma collection and exposes a simple,
vector-store-oriented CRUD API for:
- inserting vectors
- querying nearest neighbors
- deleting vectors
"""

from __future__ import annotations

from typing import Any

from chromadb.api.models.Collection import Collection

from app.interfaces import VectorStoreCRUDInterface

class ChromaDBRepository(VectorStoreCRUDInterface):
    """
    Thin adapter around a Chroma collection.

    The collection is injected (composition) so that engine/setup concerns
    live in app.db.chroma_db, and this class only handles per-operation logic.
    """

    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def insert(
        self,
        ids: list[str],
        embeddings: list[list[float]] | None,
        metadatas: list[dict[str, Any]] | None = None,
        documents: list[str] | None = None,
    ) -> None:
        """
        Insert (or upsert) vectors into the Chroma collection.
        """
        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents,
        )

    def select(
        self,
        query_embeddings: list[list[float]],
        n_results: int = 5,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Query nearest neighbors from the Chroma collection.
        """
        return self._collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where,
        )

    def get(
        self,
        ids: list[str] | None = None,
        where: dict[str, Any] | None = None,
        include: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Fetch records directly from the Chroma collection by ids and/or where.
        This does not perform similarity search; it wraps collection.get().
        """
        if include is None:
            include = ["embeddings", "metadatas", "documents"]
        return self._collection.get(
            ids=ids,
            where=where,
            include=include,
        )

    def upsert(
        self,
        ids: list[str],
        embeddings: list[list[float]] | None,
        metadatas: list[dict[str, Any]] | None = None,
        documents: list[str] | None = None,
    ) -> None:
        """
        Upsert vectors in the Chroma collection.
        """
        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents,
        )
      
      
    def delete(
        self,
        ids: list[str] | None = None,
        where: dict[str, Any] | None = None,
    ) -> None:
        """
        Delete vectors from the Chroma collection.
        """
        self._collection.delete(ids=ids, where=where)

