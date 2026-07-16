"""Route registration.

- Agile entities (Epic/Feature/Sprint/Release/Story) are project-scoped per user.
- Workspace memberships are admin-only master data (generic CRUD behind require_admin).
"""
from fastapi import APIRouter, Depends

from api.crud_router import build_crud_router
from api.scoped_crud_router import build_scoped_crud_router
from auth.current_user import require_admin
from facades.registry import build_facade
from models import entities as m
from schemas import entities as s

api_router = APIRouter()

# ---- Project-scoped agile entities ------------------------------------------------
_SCOPED = [
    ("/epics", "Epics", m.Epic, s.EpicCreate, s.EpicUpdate, s.EpicRead),
    ("/features", "Features", m.Feature, s.FeatureCreate, s.FeatureUpdate, s.FeatureRead),
    ("/sprints", "Sprints", m.Sprint, s.SprintCreate, s.SprintUpdate, s.SprintRead),
    ("/releases", "Releases", m.Release, s.ReleaseCreate, s.ReleaseUpdate, s.ReleaseRead),
    ("/stories", "Stories", m.Story, s.StoryCreate, s.StoryUpdate, s.StoryRead),
]
for prefix, tag, model, create_schema, update_schema, read_schema in _SCOPED:
    api_router.include_router(
        build_scoped_crud_router(
            prefix=prefix,
            tags=[tag],
            model=model,
            create_schema=create_schema,
            update_schema=update_schema,
            read_schema=read_schema,
        )
    )

# ---- Memberships (admin-only) -----------------------------------------------------
api_router.include_router(
    build_crud_router(
        prefix="/memberships",
        tags=["Memberships"],
        facade=build_facade(m.WorkspaceMembership),
        create_schema=s.WorkspaceMembershipCreate,
        update_schema=s.WorkspaceMembershipUpdate,
        read_schema=s.WorkspaceMembershipRead,
    ),
    dependencies=[Depends(require_admin)],
)
