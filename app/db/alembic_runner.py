"""
almebic runner to manage the database migrations
automatically updates the database schema when the model changes
it uses the alembic library to manage the migrations
"""
from pathlib import Path

from alembic import command
from alembic.config import Config

def run_migrations() -> None:
    # Point to alembic.ini at project root
    base_dir = Path(__file__).resolve().parent.parent.parent # adjust if needed
    alembic_cfg = Config(str(base_dir / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")