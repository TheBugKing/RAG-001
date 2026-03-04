"""
Shared SQLAlchemy Base for all ORM models.
Import this in models so table definitions are registered for create_all().
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
