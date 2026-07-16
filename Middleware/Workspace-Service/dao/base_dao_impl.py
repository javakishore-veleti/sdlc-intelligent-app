"""SQLAlchemy implementation of the generic CRUD DAO."""
from typing import Any, Generic, Optional, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.dao.interfaces.base_dao import BaseDaoInterface

ModelT = TypeVar("ModelT")


class BaseDao(BaseDaoInterface[ModelT], Generic[ModelT]):
    """Generic CRUD persistence for a single ORM model."""

    def __init__(self, model: Type[ModelT]) -> None:
        self.model = model

    def create(self, db: Session, data: dict[str, Any]) -> ModelT:
        obj = self.model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(self, db: Session, entity_id: UUID) -> Optional[ModelT]:
        return db.get(self.model, entity_id)

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[ModelT]:
        stmt = select(self.model)
        if filters:
            for field, value in filters.items():
                if value is not None and hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)
        stmt = stmt.offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def list_by_projects(
        self,
        db: Session,
        project_ids,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelT]:
        """List rows whose ``project_id`` is in ``project_ids`` (for access scoping)."""
        if not project_ids:
            return []
        stmt = (
            select(self.model)
            .where(self.model.project_id.in_(list(project_ids)))
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())

    def update(self, db: Session, entity_id: UUID, data: dict[str, Any]) -> Optional[ModelT]:
        obj = db.get(self.model, entity_id)
        if obj is None:
            return None
        for field, value in data.items():
            setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, entity_id: UUID) -> bool:
        obj = db.get(self.model, entity_id)
        if obj is None:
            return False
        db.delete(obj)
        db.commit()
        return True
