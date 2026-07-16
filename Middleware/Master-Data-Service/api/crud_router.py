"""Factory that builds a standard CRUD ``APIRouter`` for any entity.

Given a facade and the entity's Create/Update/Read schemas, it produces the five
canonical endpoints (create, list, get, update, delete) with correct request/response
models so each appears fully typed in the OpenAPI/Swagger docs.
"""
from typing import Type
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import get_db
from common.constants.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from common.facade.interfaces.base_facade import BaseFacadeInterface


def build_crud_router(
    *,
    prefix: str,
    tags: list[str],
    facade: BaseFacadeInterface,
    create_schema: Type[BaseModel],
    update_schema: Type[BaseModel],
    read_schema: Type[BaseModel],
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)

    @router.post("", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    def create_item(payload: create_schema, db: Session = Depends(get_db)):  # type: ignore[valid-type]
        return facade.create(db, payload.model_dump(exclude_unset=True))

    @router.get("", response_model=list[read_schema])
    def list_items(
        skip: int = Query(0, ge=0),
        limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
        db: Session = Depends(get_db),
    ):
        return facade.list(db, skip, limit, None)

    @router.get("/{entity_id}", response_model=read_schema)
    def get_item(entity_id: UUID, db: Session = Depends(get_db)):
        obj = facade.get(db, entity_id)
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return obj

    @router.put("/{entity_id}", response_model=read_schema)
    def update_item(entity_id: UUID, payload: update_schema, db: Session = Depends(get_db)):  # type: ignore[valid-type]
        obj = facade.update(db, entity_id, payload.model_dump(exclude_unset=True))
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return obj

    @router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(entity_id: UUID, db: Session = Depends(get_db)):
        if not facade.delete(db, entity_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return None

    return router
