"""CRUD router factory with per-user/admin project scoping.

For entities that carry ``project_id``: admins see/act on everything; non-admins are
limited to projects they belong to (403 otherwise). Identity comes from
``get_current_user``.
"""
from typing import Type
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.deps import get_db
from auth.current_user import CurrentUser, get_current_user
from common.constants.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from dao.base_dao_impl import BaseDao


def build_scoped_crud_router(
    *,
    prefix: str,
    tags: list[str],
    model,
    create_schema: Type[BaseModel],
    update_schema: Type[BaseModel],
    read_schema: Type[BaseModel],
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)
    dao = BaseDao(model)

    def ensure_access(user: CurrentUser, project_id) -> None:
        if not user.is_admin and project_id not in user.project_ids:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not permitted for this project")

    @router.post("", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    def create_item(
        payload: create_schema,  # type: ignore[valid-type]
        db: Session = Depends(get_db),
        user: CurrentUser = Depends(get_current_user),
    ):
        data = payload.model_dump(exclude_unset=True)
        ensure_access(user, data.get("project_id"))
        return dao.create(db, data)

    @router.get("", response_model=list[read_schema])
    def list_items(
        skip: int = Query(0, ge=0),
        limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
        db: Session = Depends(get_db),
        user: CurrentUser = Depends(get_current_user),
    ):
        if user.is_admin:
            return dao.list(db, skip, limit, None)
        return dao.list_by_projects(db, user.project_ids, skip, limit)

    @router.get("/{entity_id}", response_model=read_schema)
    def get_item(
        entity_id: UUID,
        db: Session = Depends(get_db),
        user: CurrentUser = Depends(get_current_user),
    ):
        obj = dao.get(db, entity_id)
        if obj is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
        ensure_access(user, obj.project_id)
        return obj

    @router.put("/{entity_id}", response_model=read_schema)
    def update_item(
        entity_id: UUID,
        payload: update_schema,  # type: ignore[valid-type]
        db: Session = Depends(get_db),
        user: CurrentUser = Depends(get_current_user),
    ):
        obj = dao.get(db, entity_id)
        if obj is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
        ensure_access(user, obj.project_id)
        data = payload.model_dump(exclude_unset=True)
        if data.get("project_id") is not None:
            ensure_access(user, data["project_id"])
        return dao.update(db, entity_id, data)

    @router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(
        entity_id: UUID,
        db: Session = Depends(get_db),
        user: CurrentUser = Depends(get_current_user),
    ):
        obj = dao.get(db, entity_id)
        if obj is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
        ensure_access(user, obj.project_id)
        dao.delete(db, entity_id)
        return None

    return router
