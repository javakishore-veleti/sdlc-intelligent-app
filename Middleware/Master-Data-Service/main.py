"""Master-Data-Service — FastAPI application entrypoint.

On startup the service applies any pending Alembic migrations (``upgrade head``), so
the database schema is brought up to date automatically whenever the app starts.

Interactive API docs (OpenAPI / Swagger) are served at:
    /docs          Swagger UI
    /redoc         ReDoc
    /openapi.json  raw OpenAPI schema
"""
import logging
import pathlib
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI

from api.dashboard_router import router as dashboard_router
from api.routes import api_router
from common.constants.constants import API_V1_PREFIX, SERVICE_NAME, SERVICE_VERSION

logger = logging.getLogger("master_data_service")
BASE_DIR = pathlib.Path(__file__).resolve().parent


def run_migrations() -> None:
    """Apply all pending migrations up to head (Liquibase-style auto-upgrade)."""
    cfg = Config(str(BASE_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BASE_DIR / "alembic"))
    logger.info("Applying database migrations (alembic upgrade head)...")
    command.upgrade(cfg, "head")
    logger.info("Database schema is up to date.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


tags_metadata = [
    {"name": "Employees", "description": "People who can be assigned to projects."},
    {"name": "Projects", "description": "Business applications / projects (one per microservice)."},
    {"name": "Project Roles", "description": "Roles defined within a project."},
    {"name": "Project Employees", "description": "Employee-to-project-role assignments."},
    {"name": "Project Artifacts", "description": "Artifacts produced by a project."},
    {"name": "Project Capabilities", "description": "Typed capabilities a project provides."},
    {"name": "Project Domains", "description": "Hierarchical business (sub)domains."},
    {"name": "Project Knowledge Bases", "description": "Knowledge-base entries for a project."},
    {"name": "Project Tech Stacks", "description": "Technologies used by a project."},
    {"name": "Project Dependency Groups", "description": "Groupings of inter-project dependencies."},
    {"name": "Project Dependencies", "description": "Dependencies on other projects' capabilities."},
    {"name": "Project Client Groups", "description": "Groupings of client relationships."},
    {"name": "Project Clients", "description": "Other projects consuming this project's capabilities."},
    {"name": "Dashboard", "description": "Aggregate statistics (cached, 6h configurable TTL)."},
    {"name": "health", "description": "Service liveness."},
]

app = FastAPI(
    title=SERVICE_NAME,
    version=SERVICE_VERSION,
    description=(
        "SDLC master-data management: CRUD for employees, projects, roles, "
        "assignments, artifacts, capabilities, domains, knowledge bases, tech stacks, "
        "dependencies, and clients."
    ),
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(api_router, prefix=API_V1_PREFIX)
app.include_router(dashboard_router, prefix=API_V1_PREFIX)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "service": SERVICE_NAME, "version": SERVICE_VERSION}
