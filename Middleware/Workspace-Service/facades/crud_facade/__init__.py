"""Generic CRUD facade.

Orchestrates create/read/update/delete use cases by delegating to the ``tasks``
module, which in turn calls the service layer. One instance is created per entity
(see ``facades/registry.py``). Entity-specific facades can subclass this to add
richer, multi-step use cases while reusing the CRUD tasks.
"""
from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from common.facade.interfaces.base_facade import BaseFacadeInterface
from common.service.interfaces.base_service import BaseServiceInterface
from facades.crud_facade.tasks import crud_tasks

ModelT = TypeVar("ModelT")


class CrudFacade(BaseFacadeInterface[ModelT], Generic[ModelT]):
    def __init__(self, service: BaseServiceInterface[ModelT]) -> None:
        self.service = service

    def create(self, db: Session, data: dict[str, Any]) -> ModelT:
        return crud_tasks.create_entity(self.service, db, data)

    def get(self, db: Session, entity_id: UUID) -> Optional[ModelT]:
        return crud_tasks.get_entity(self.service, db, entity_id)

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict[str, Any]] = None,
    ) -> list[ModelT]:
        return crud_tasks.list_entities(self.service, db, skip, limit, filters)

    def update(self, db: Session, entity_id: UUID, data: dict[str, Any]) -> Optional[ModelT]:
        return crud_tasks.update_entity(self.service, db, entity_id, data)

    def delete(self, db: Session, entity_id: UUID) -> bool:
        return crud_tasks.delete_entity(self.service, db, entity_id)
