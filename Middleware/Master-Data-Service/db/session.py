"""Database engine and session factory.

The database URL is read from the ``DATABASE_URL`` environment variable. It defaults
to a local SQLite file so the service runs with zero external dependencies; point it
at PostgreSQL in a containerized/production environment, e.g.::

    DATABASE_URL=postgresql+psycopg2://user:pass@postgres:5432/master_data
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./master_data.db")

# SQLite needs check_same_thread disabled for use across FastAPI's threadpool.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    """FastAPI dependency that yields a scoped session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
