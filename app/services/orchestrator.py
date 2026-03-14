"""
Orchestrator service (function-based).
"""

from __future__ import annotations

import asyncio
import os
import uuid
from pathlib import Path
from typing import Callable

from app.services import TextChunker, OpenAIEmbedding
from app.interfaces import ChunkerStrategyInterface, EmbeddingStrategyInterface, VectorStoreCRUDInterface
from app.db import get_vector_store, get_document_repository as _get_document_repository
from app.models.repositories.sqlite_document_repository import SqliteDocumentRepository
from settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    OPENAI_EMBEDDING_MODEL,
    VECTOR_STORE_COLLECTION,
    EMBEDDING_BATCH_SIZE,
)

# Mime type by extension for document table
_DEFAULT_MIME = "application/octet-stream"
_EXT_TO_MIME = {
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
}


def _normalize_paths(document_paths: list[str | Path]) -> list[Path]:
    out: list[Path] = []
    for p in document_paths:
        if isinstance(p, str):
            out.append(Path(p))
        elif isinstance(p, Path):
            out.append(p)
        else:
            raise ValueError(f"Invalid document path: {p}")
    return out


def _chunk_texts(chunks: list) -> list[str]:
    """Extract plain text from chunk objects (LangChain Document or str)."""
    if not chunks:
        return []
    if hasattr(chunks[0], "page_content"):
        return [c.page_content for c in chunks]
    return [str(c) for c in chunks]


def _batch_list(items: list, batch_size: int) -> list[list]:
    """Split list into batches of up to batch_size."""
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def _document_record(document_path: Path, document_id: str, status: str = "indexed") -> dict:
    """Build a document dict for SQLite insert (id, original_filename, file_path, file_size_bytes, mime_type, status)."""
    try:
        file_size = os.path.getsize(document_path)
    except OSError:
        file_size = 0
    ext = (document_path.suffix or "").lower()
    mime_type = _EXT_TO_MIME.get(ext, _DEFAULT_MIME)
    return {
        "id": document_id,
        "original_filename": document_path.name,
        "file_path": str(document_path),
        "file_size_bytes": file_size,
        "mime_type": mime_type,
        "status": status,
    }


async def _process_one_document(
    document_path: Path,
    chunker: ChunkerStrategyInterface,
    embedding: EmbeddingStrategyInterface,
    vector_store: VectorStoreCRUDInterface,
    get_document_repository: Callable[[], SqliteDocumentRepository],
) -> list[list[float]]:
    """Load, chunk, embed, insert into vector store and SQLite. Sync steps run in thread pool."""
    print(f"Processing document {document_path}")
    documents = await asyncio.to_thread(chunker.load_document, document_path)
    chunks = await asyncio.to_thread(chunker.chunk, documents)
    chunk_texts = _chunk_texts(chunks)
    if not chunk_texts:
        return []

    # One document_id for both SQLite and Chroma (link DB row and vector chunks)
    document_id = str(uuid.uuid4())

    # Run embedding in parallel batches (many texts at a time)
    batches = _batch_list(chunk_texts, EMBEDDING_BATCH_SIZE)
    batch_results = await asyncio.gather(*[embedding.embed(batch) for batch in batches])
    mapped = [m for batch in batch_results for m in batch]

    # Chroma: chunk ids and metadata use same document_id so we can query/delete by document
    chunk_ids = [f"{document_id}_{i}" for i in range(len(mapped))]
    embeddings = [m["embedding"] for m in mapped]
    documents_list = [m["chunk"] for m in mapped]
    metadatas = [{"document_id": document_id} for _ in mapped]

    await asyncio.to_thread(
        vector_store.insert,
        ids=chunk_ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents_list,
    )

    # SQLite: same document_id as primary key (close session when done)
    doc_repo = get_document_repository()
    try:
        record = _document_record(document_path, document_id=document_id, status="indexed")
        await asyncio.to_thread(doc_repo.insert, record)
    finally:
        doc_repo.close()


async def orchestrate_indexing(
    document_paths: list[str | Path],
    chunker: ChunkerStrategyInterface | None = None,
    embedding: EmbeddingStrategyInterface | None = None,
    vector_store: VectorStoreCRUDInterface | None = None,
    get_document_repository: Callable[[], SqliteDocumentRepository] | None = None,
) -> list[list[list[float]]]:
    """
    Chunk, embed, insert into vector store and SQLite. Processes documents concurrently.
    Returns embeddings per document (list of list of vectors).
    """
    paths = _normalize_paths(document_paths)
    if not paths:
        return []

    chunker = chunker or TextChunker(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    embedding = embedding or OpenAIEmbedding(embedding_model=OPENAI_EMBEDDING_MODEL)
    vector_store = vector_store or get_vector_store(collection_name=VECTOR_STORE_COLLECTION)
    get_doc_repo = get_document_repository or _get_document_repository

    results = await asyncio.gather(
        *[
            _process_one_document(p, chunker, embedding, vector_store, get_doc_repo)
            for p in paths
        ]
    )
    get_doc_repo.close()
    vector_store.close()
    return list(results)
