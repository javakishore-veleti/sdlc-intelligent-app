"""Knowledge-Service — FastAPI application entrypoint.

Retrieval-Augmented Generation over the vector DB collections built by the ingestion
DAG (langchain__... / langgraph__...). No database of its own. OpenAPI/Swagger at /docs.
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.ask_router import router as ask_router
from common.constants.constants import API_V1_PREFIX, SERVICE_NAME, SERVICE_VERSION

tags_metadata = [
    {"name": "Assistant", "description": "Ask questions over ingested docs; compare frameworks."},
    {"name": "health", "description": "Service liveness."},
]

app = FastAPI(
    title=SERVICE_NAME,
    version=SERVICE_VERSION,
    description=(
        "RAG assistant: retrieves from ChromaDB (per-framework, per-strategy collections) "
        "and answers with citations. Answer generator is pluggable (extractive default; "
        "Ollama/Groq later)."
    ),
    openapi_tags=tags_metadata,
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

app.include_router(ask_router, prefix=API_V1_PREFIX)


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "service": SERVICE_NAME, "version": SERVICE_VERSION}
