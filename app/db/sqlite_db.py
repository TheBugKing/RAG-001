import os
from pathlib import Path
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.interfaces.database_engine_interface import DatabaseEngineInterface


class SQLiteDB(DatabaseEngineInterface):
    def __init__(self, db_url: str | Path):
        self.db_url = str(db_url).strip()
        self.engine = self.create_db_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_db_engine(self) -> Engine:
        return create_engine(self.db_url, connect_args={"check_same_thread": False})

    def init_db(self) -> None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data", "sqlite")
        os.makedirs(data_dir, exist_ok=True)
        from app.models import document_model  # noqa: F401 - register Document with Base
        Base.metadata.create_all(bind=self.engine)

    def get_db(self) -> Session:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()