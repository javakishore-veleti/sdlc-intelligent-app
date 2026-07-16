"""Generic service implementation.

Delegates persistence to a DAO. Entity-specific business rules (validation,
cross-entity checks, events) belong in subclasses that override these methods.
"""
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from common.dao.interfaces.base_dao import BaseDaoInterface
from common.service.interfaces.base_service import BaseServiceInterface

ModelT = TypeVar("ModelT")


class BaseService(BaseServiceInterface[ModelT], Generic[ModelT]):
    def __init__(self, dao: BaseDaoInterface[ModelT]) -> None:
        self.dao = dao

    def create(self, db: Session, data: dict[str, Any]) -> ModelT:
        return self.dao.create(db, data)

    def get(self, db: Session, entity_id: UUID) -> Optional[ModelT]:
        return self.dao.get(db, entity_id)

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[ModelT]:
        return self.dao.list(db, skip, limit, filters)

    def update(self, db: Session, entity_id: UUID, data: dict[str, Any]) -> Optional[ModelT]:
        return self.dao.update(db, entity_id, data)

    def delete(self, db: Session, entity_id: UUID) -> bool:
        return self.dao.delete(db, entity_id)
