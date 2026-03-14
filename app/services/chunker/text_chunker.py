"""
Chunker service.
"""

from __future__ import annotations

from typing import Any
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, DocumentLoader
import os


from app.interfaces import ChunkerStrategyInterface


class TextChunker(ChunkerStrategyInterface):
    """
    Chunker service that chunks documents into text chunks.
    """

    def __init__(self, chunk_size: int = 100, chunk_overlap: int = 0,
                 *args: Any, **kwargs: Any) -> None:
        self.__chunk_size = chunk_size
        self.__chunk_overlap = chunk_overlap
        self.__args = args
        self.__kwargs = kwargs

    def load_document(self, document_path: Path) -> None:
        """
        Load a document into the chunker strategy.
        """
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document path {document_path} does not exist")

        if not document_path.split(".")[-1] in ["pdf", "docx", "doc"]:
            raise ValueError(f"Document path {document_path} is not a PDF, DOCX, or DOC file")

        loader = PyMuPDFLoader(document_path)
        documents = loader.load()
        print(f"Documents loaded: {len(documents)} documents")
        return documents

    def chunk(self, documents: list[DocumentLoader]) -> list[str]:
        """
        Chunk the documents into a list of chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.__chunk_size, chunk_overlap=self.__chunk_overlap)
        chunks = text_splitter.split_documents(documents)
        print(f"Chunks: {len(chunks)} chunks")
        return chunks
