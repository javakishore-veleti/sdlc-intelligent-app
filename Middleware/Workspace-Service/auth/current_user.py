"""Per-user / admin access scoping.

Identity is taken from the ``X-User-Email`` request header (a stub for real JWT auth,
which would replace ``get_current_user`` without touching the routers). Admins (emails
in ``ADMIN_EMAILS``) see all projects; everyone else is limited to the projects they
are a member of (``workspace_memberships``).
"""
import os
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.deps import get_db
from models.entities import WorkspaceMembership

ADMIN_EMAILS = {
    e.strip().lower()
    for e in os.getenv("ADMIN_EMAILS", "admin@example.com").split(",")
    if e.strip()
}


@dataclass
class CurrentUser:
    email: str
    is_admin: bool
    project_ids: set[UUID]


def get_current_user(
    x_user_email: Optional[str] = Header(default="demo@example.com", alias="X-User-Email"),
    db: Session = Depends(get_db),
) -> CurrentUser:
    email = (x_user_email or "demo@example.com").strip().lower()
    is_admin = email in ADMIN_EMAILS
    project_ids: set[UUID] = set()
    if not is_admin:
        rows = db.execute(
            select(WorkspaceMembership.project_id).where(
                WorkspaceMembership.user_email == email
            )
        ).all()
        project_ids = {row[0] for row in rows}
    return CurrentUser(email=email, is_admin=is_admin, project_ids=project_ids)


def require_admin(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin only")
    return user
