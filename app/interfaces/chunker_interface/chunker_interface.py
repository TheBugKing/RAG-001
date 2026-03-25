"""
Abstract interface for chunking documents.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path

class ChunkerStrategyInterface(ABC):
    """
    Contract for chunking documents using a specific strategy.
    Implementations can use any chunking strategy, such as:
    - Sentence-based chunking
    - Paragraph-based chunking
    - Section-based chunking
    - etc.
    """
    
    @abstractmethod
    def load_document(self, document_path: Path) -> list[Any]:
        """
        Load a document into the chunker strategy.
        """
        pass

    @abstractmethod
    def chunk(self, documents: list[Any]) -> list[str]:
        """
        Chunk the documents into a list of chunks.
        """
        pass
