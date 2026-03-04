"""
Entry point for the FastAPI application.
"""

import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.master_routes import main_routers

# ---------------------------------------------------------------------------
# DB engine: one instance, used for init_db and to provide sessions
# ---------------------------------------------------------------------------
from app.db.db_utils import db_engine, vector_store_engine
# ---------------------------------------------------------------------------
# App lifespan and routes
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database and create tables if needed
    print("Initializing database...")
    db_engine.init_db()
    print("Database initialized")
    print("Initializing vector store...")
    vector_store_engine.init_store()
    print("Vector store initialized")
    yield
    # Shutdown: nothing to clean up yet
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
[app.include_router(router) for router in main_routers]


@app.get("/")
async def health_check():
    return {"message": "OK"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
