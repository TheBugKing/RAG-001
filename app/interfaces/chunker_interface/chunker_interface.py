"""
Abstract interface for chunking documents.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path
from langchain_community.document_loaders import DocumentLoader

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
    def load_document(self, document_path: Path) -> None:
        """
        Load a document into the chunker strategy.
        """
        pass

    @abstractmethod
    def chunk(self, documents: list[DocumentLoader]) -> list[str]:
        """
        Chunk the documents into a list of chunks.
        """
        pass
