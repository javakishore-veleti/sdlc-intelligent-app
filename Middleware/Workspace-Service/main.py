"""Workspace-Service — FastAPI application entrypoint.

Applies Alembic migrations on startup, then serves project-scoped CRUD for agile
delivery artifacts (Epics, Features, Sprints, Releases, Stories) plus admin-managed
workspace memberships. OpenAPI/Swagger at /docs, /redoc.
"""
import logging
import os
import pathlib
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import api_router
from common.constants.constants import API_V1_PREFIX, SERVICE_NAME, SERVICE_VERSION

logger = logging.getLogger("workspace_service")
BASE_DIR = pathlib.Path(__file__).resolve().parent


def run_migrations() -> None:
    cfg = Config(str(BASE_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BASE_DIR / "alembic"))
    command.upgrade(cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


tags_metadata = [
    {"name": "Epics", "description": "Epics (top of the work hierarchy)."},
    {"name": "Features", "description": "Features under an epic."},
    {"name": "Sprints", "description": "Sprint time-boxes."},
    {"name": "Releases", "description": "Release time-boxes."},
    {"name": "Stories", "description": "Stories under a feature, assignable to a sprint/release."},
    {"name": "Memberships", "description": "User-to-project memberships (admin only)."},
    {"name": "health", "description": "Service liveness."},
]

app = FastAPI(
    title=SERVICE_NAME,
    version=SERVICE_VERSION,
    description=(
        "Agile delivery artifacts scoped per user by project membership (admins see all). "
        "Identity via the X-User-Email header (stub for real auth)."
    ),
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

_cors_origins = os.getenv(
    "CORS_ALLOW_ORIGINS", "http://localhost:4200,http://127.0.0.1:4200"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _cors_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=API_V1_PREFIX)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "service": SERVICE_NAME, "version": SERVICE_VERSION}
