# Ingest-Extract-Service

FastAPI service — **document intake and extraction**.

Receives uploaded sprint PDFs from the `sdlc-nexus` portal, extracts their content,
and drives ingestion (parse → chunk → embed → index) by triggering the Airflow
pipeline. Tracks and reports ingestion status.

Follows the standard layered layout (`api` → `facades`/`tasks` → service → `dao`,
with interfaces in `common/`). See [`../README.md`](../README.md).
