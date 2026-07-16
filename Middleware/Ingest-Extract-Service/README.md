# Ingest-Extract-Service

FastAPI service — **document intake**. Accepts a PDF, stores it in a pluggable datalake,
records an `ingest_log`, and triggers the Airflow ingestion DAG.

## Flow

```
POST /api/v1/ingest/uploads (PDF + project_id, project_sprint, uploaded_by)
   1. store file + manifest.json   -> <datalake>/datalake/pdfs/<UUID>/
   2. INSERT ingest_log (PENDING, ingest_dt)   -> Postgres
   3. trigger Airflow DAG (conf: ingest_log_id, ref_id, document_path, ...)
   -> the DAG sets IN_PROGRESS/COMPLETED and loads content into the vector DB
```

## Storage backends (pluggable)

`common/storage/interfaces/storage_backend.py` defines the contract. Implemented:
- **local** — `~/runtime_data/sdlc-intelligent-app/datalake/pdfs/<UUID>/` (default)

Future backends (same interface): `aws_s3`, `azure_blob`. Select via `STORAGE_BACKEND`.

## ingest_log

| Field | Notes |
|---|---|
| `ref_id` | datalake UUID |
| `ingest_type` | PDF / EXCEL / CSV / IMAGE / OTHER |
| `storage_type` | LOCAL_FILE_SYSTEM / AWS_S3 / AZURE_BLOB / OTHER |
| `ingest_process_status` | PENDING → IN_PROGRESS → COMPLETED / FAILED |
| `ingest_dt` | upload time |
| `ingest_process_start_dt` / `ingest_process_complete_dt` | set by the DAG |

Schema is versioned with Alembic and auto-applied on startup.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8003    # http://localhost:8003/docs
```

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./ingest.db` | ingest_log store (Postgres in containers) |
| `STORAGE_BACKEND` | `local` | `local` \| `aws_s3` \| `azure_blob` |
| `DATALAKE_BASE_PATH` | `~/runtime_data/sdlc-intelligent-app` | datalake root |
| `AIRFLOW_BASE_URL` | `http://localhost:8080` | Airflow REST endpoint |
| `AIRFLOW_TRIGGER_ENABLED` | `true` | set `false` to skip triggering |

## API

- `POST /api/v1/ingest/uploads` — multipart: `file` (PDF), `project_id`, `project_sprint`, `uploaded_by`
- `GET  /api/v1/ingest-logs` — list ingest logs
- `GET  /api/v1/ingest-logs/{id}` — one ingest log
- Swagger at `/docs`.

The ingestion DAG that consumes uploads lives in `../SDLC-Workflows`.
