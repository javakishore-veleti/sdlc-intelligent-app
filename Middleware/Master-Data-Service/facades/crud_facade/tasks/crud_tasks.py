"""Discrete unit-of-work steps invoked by the CRUD facade.

Keeping each operation as a small task function makes the facade's orchestration
explicit and gives a natural place to insert pre/post steps (auditing, events,
cross-entity validation) without changing the API or service contracts.
"""
from typing import Any, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from common.service.interfaces.base_service import BaseServiceInterface


def create_entity(service: BaseServiceInterface, db: Session, data: dict[str, Any]):
    return service.create(db, data)


def get_entity(service: BaseServiceInterface, db: Session, entity_id: UUID):
    return service.get(db, entity_id)


def list_entities(
    service: BaseServiceInterface,
    db: Session,
    skip: int,
    limit: int,
    filters: Optional[dict[str, Any]],
):
    return service.list(db, skip, limit, filters)


def update_entity(service: BaseServiceInterface, db: Session, entity_id: UUID, data: dict[str, Any]):
    return service.update(db, entity_id, data)


def delete_entity(service: BaseServiceInterface, db: Session, entity_id: UUID) -> bool:
    return service.delete(db, entity_id)
