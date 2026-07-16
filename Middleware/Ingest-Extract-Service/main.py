"""Ingest-Extract-Service — FastAPI application entrypoint.

Applies Alembic migrations on startup (creates/updates the ingest_log table), then
serves the upload + ingest-log endpoints. OpenAPI/Swagger at /docs, /redoc.
"""
import logging
import os
import pathlib
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.ingest_log_router import router as ingest_log_router
from api.upload_router import router as upload_router
from common.constants.constants import API_V1_PREFIX, SERVICE_NAME, SERVICE_VERSION

logger = logging.getLogger("ingest_extract_service")
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
    {"name": "Ingestion", "description": "Upload a PDF into the datalake and trigger ingestion."},
    {"name": "Ingest Logs", "description": "Track ingestion lifecycle records."},
    {"name": "health", "description": "Service liveness."},
]

app = FastAPI(
    title=SERVICE_NAME,
    version=SERVICE_VERSION,
    description=(
        "Accepts document uploads (PDF), stores them in a pluggable datalake backend "
        "(local now; S3/Azure later), records an ingest_log, and triggers the Airflow "
        "ingestion DAG that loads content into the vector database."
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

app.include_router(upload_router, prefix=API_V1_PREFIX)
app.include_router(ingest_log_router, prefix=API_V1_PREFIX)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "service": SERVICE_NAME, "version": SERVICE_VERSION}
