"""Reusable declarative mixins: UUID primary key and created/updated timestamps.

Columns declared on a mixin are copied onto each mapped subclass by SQLAlchemy's
declarative system, so a fresh Column instance is created per model.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Uuid


class UUIDPkMixin:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
