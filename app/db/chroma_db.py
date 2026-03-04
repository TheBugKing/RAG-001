"""
ChromaDB implementation of VectorStoreEngineInterface.
"""

import os
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings

from app.interfaces import VectorStoreEngineInterface

class ChromaDB(VectorStoreEngineInterface):
    def __init__(self, db_url: str | Path):
        self.db_url = str(db_url).strip()
        self.client = self.init_store()

    def init_store(self) -> None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data", "chroma")
        os.makedirs(data_dir, exist_ok=True)
        return chromadb.PersistentClient(path=self.db_url)

    def get_vector_store(self, collection_name: str) -> Any:
        try:
            yield self.client.get_or_create_collection(collection_name)
        except Exception as e:
            raise e
        finally:
            self.client.close()