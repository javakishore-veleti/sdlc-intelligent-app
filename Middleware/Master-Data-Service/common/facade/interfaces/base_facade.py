"""Facade-layer contract: the use-case surface the API calls into."""
from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseFacadeInterface(ABC, Generic[ModelT]):
    @abstractmethod
    def create(self, db: Session, data: dict[str, Any]) -> ModelT: ...

    @abstractmethod
    def get(self, db: Session, entity_id: UUID) -> Optional[ModelT]: ...

    @abstractmethod
    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[ModelT]: ...

    @abstractmethod
    def update(self, db: Session, entity_id: UUID, data: dict[str, Any]) -> Optional[ModelT]: ...

    @abstractmethod
    def delete(self, db: Session, entity_id: UUID) -> bool: ...
