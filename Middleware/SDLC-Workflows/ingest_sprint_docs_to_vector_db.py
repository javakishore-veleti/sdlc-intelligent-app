"""Airflow DAG: ingest a sprint document into the vector database (ChromaDB).

Triggered on demand (e.g., by Ingest-Extract-Service) with a document reference in
``dag_run.conf``, for example::

    {"document_id": "...", "document_path": "/data/uploads/pricing_sprint9.pdf",
     "application": "Pricing", "sprint": "Sprint 9"}

The steps below form the ingestion pipeline. They currently log their intent; the
concrete extraction/embedding/upsert implementation lands with Ingest-Extract-Service
and Knowledge-Service.
"""
from __future__ import annotations

import logging
from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context

log = logging.getLogger(__name__)


@dag(
    dag_id="ingest_sprint_docs_to_vector_db",
    schedule=None,  # triggered on demand via the REST API / UI
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ingestion", "vector-db", "sdlc"],
)
def ingest_sprint_docs_to_vector_db():
    @task
    def extract() -> dict:
        ctx = get_current_context()
        conf = (ctx["dag_run"].conf or {}) if ctx.get("dag_run") else {}
        document_path = conf.get("document_path", "sample.pdf")
        log.info("Extracting text (per page) from %s", document_path)
        return {
            "document_id": conf.get("document_id"),
            "document_path": document_path,
            "application": conf.get("application"),
            "sprint": conf.get("sprint"),
            "pages": [],  # [{"page": 1, "text": "..."}, ...]
        }

    @task
    def chunk(payload: dict) -> dict:
        log.info("Chunking %s into ~2000-token chunks", payload.get("document_path"))
        payload["chunks"] = []  # [{"text": "...", "page": 1, "chunk_index": 0}, ...]
        return payload

    @task
    def embed(payload: dict) -> dict:
        log.info("Embedding %d chunks", len(payload.get("chunks", [])))
        return payload

    @task
    def upsert_to_vector_db(payload: dict) -> None:
        log.info(
            "Upserting %d chunks into ChromaDB (application=%s, sprint=%s)",
            len(payload.get("chunks", [])),
            payload.get("application"),
            payload.get("sprint"),
        )

    upsert_to_vector_db(embed(chunk(extract())))


ingest_sprint_docs_to_vector_db()
