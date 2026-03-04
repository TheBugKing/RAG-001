"""
Entry point for the FastAPI application.
"""

import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv(override=True)

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.sqlite_db import SQLiteDB
from app.repositories.sqlite_document_repository import SqliteDocumentRepository

# ---------------------------------------------------------------------------
# DB engine: one instance, used for init_db and to provide sessions
# ---------------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/rag.db")
db_engine = SQLiteDB(DATABASE_URL)
# ---------------------------------------------------------------------------
# App lifespan and routes
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database and create tables if needed
    print("Initializing database...")
    db_engine.init_db()
    print("Database initialized")
    yield
    # Shutdown: nothing to clean up yet
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health_check():
    return {"message": "OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
