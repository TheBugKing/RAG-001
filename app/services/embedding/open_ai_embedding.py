"""
Embedding service.
"""

from __future__ import annotations

import asyncio
from typing import Any

from langchain_openai import OpenAIEmbeddings

from app.interfaces import EmbeddingStrategyInterface


class OpenAIEmbedding(EmbeddingStrategyInterface):
    """
    OpenAI embedding service. One client instance, batch embedding via embed_documents.
    """
    def __init__(self, embedding_model: str, *args: Any, **kwargs: Any) -> None:
        self._client = OpenAIEmbeddings(model=embedding_model, **kwargs)

    async def embed(self, chunks: list[str]) -> list[dict[str, Any]]:
        """
        Embed chunks in one batch. Returns one mapping per chunk:
        [{"chunk": str, "embedding": list[float]}, ...].
        """
        if not chunks:
            return []
        embeddings = await asyncio.to_thread(self._client.embed_documents, chunks)
        return [{"chunk": c, "embedding": e} for c, e in zip(chunks, embeddings)]