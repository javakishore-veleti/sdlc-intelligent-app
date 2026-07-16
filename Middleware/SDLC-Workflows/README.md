# SDLC-Workflows

Apache Airflow **DAGs** for the SDLC Intelligent App.

This folder is mounted into the Airflow containers as the DAGs directory
(`/opt/airflow/dags`) by `infra/docker-compose.yml`. Any `*.py` DAG placed here is
picked up automatically by the scheduler.

## Purpose

Airflow orchestrates **ingestion of sprint documents into the vector database
(ChromaDB)**: extract → chunk → embed → upsert. Runs are triggered on demand
(e.g., by `Ingest-Extract-Service` when a document is uploaded) via the Airflow REST
API, with the document reference passed in `dag_run.conf`.

## DAGs

| DAG id | Purpose |
|---|---|
| `ingest_sprint_docs_to_vector_db` | Extract a sprint PDF, chunk it, embed the chunks, and upsert them into ChromaDB with metadata |

> The current DAG is a **structured skeleton** (each step logs its intent). The real
> extraction/embedding/upsert logic lands together with `Ingest-Extract-Service` and
> `Knowledge-Service`.
