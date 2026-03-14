# app/db/db_utils.py
import os
from app.db.sqlite_db import SQLiteDB
from app.db.chroma_db import ChromaDB
from app.models.repositories import ChromaDBRepository, SqliteDocumentRepository

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/sqlite/rag_001.db")
VECTOR_STORE_URL = os.getenv("VECTOR_STORE_URL", "./data/chroma/rag_vector_001.db")

# Create single engines here
db_engine = SQLiteDB(db_url=DATABASE_URL)          # from settings/env
vector_store_engine = ChromaDB(db_url=VECTOR_STORE_URL)  # from settings/env

def get_db():
    # delegate to SQLiteDB; its get_db() already manages session lifetime
    yield from db_engine.get_db()

def get_document_repository():
    session = next(db_engine.get_db())           # or use Depends(get_db) pattern
    db = SqliteDocumentRepository(session=session)
    return db

def get_vector_store(collection_name: str):
    collection = next(vector_store_engine.get_vector_store(collection_name=collection_name))
    return ChromaDBRepository(collection=collection)   # no client.close() here