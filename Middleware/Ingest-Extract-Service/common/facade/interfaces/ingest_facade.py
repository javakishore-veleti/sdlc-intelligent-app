"""Facade contract for the ingest use case."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session


class IngestFacadeInterface(ABC):
    @abstractmethod
    def ingest_pdf(
        self,
        db: Session,
        *,
        filename: str,
        content: bytes,
        project_id: Optional[UUID],
        project_sprint: Optional[str],
        uploaded_by: Optional[str],
    ) -> dict: ...
