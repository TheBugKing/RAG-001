"""
Abstract interface for embedding documents.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class EmbeddingStrategyInterface(ABC):
    """
    Contract for embedding documents using a specific strategy.
    """

    @abstractmethod
    def __init__(self, embedding_model: str, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the embedding strategy.
        """
        pass
    
    @abstractmethod
    def embed(self, chunks: list[str]) -> list[list[float]]:
        """
        Embed chunks into a list of embeddings.
        """
        pass

    
