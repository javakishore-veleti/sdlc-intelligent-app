"""Service-wide configuration for Ingest-Extract-Service."""
import os
from pathlib import Path

SERVICE_NAME = "Ingest-Extract-Service"
SERVICE_VERSION = "0.1.0"
API_V1_PREFIX = "/api/v1"

# ---- Storage (pluggable backend) --------------------------------------------------
# local (default) | aws_s3 | azure_blob  (only "local" implemented today)
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")
# Default datalake root: ~/runtime_data/sdlc-intelligent-app
DATALAKE_BASE_PATH = os.getenv(
    "DATALAKE_BASE_PATH", str(Path.home() / "runtime_data" / "sdlc-intelligent-app")
)
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(50 * 1024 * 1024)))

# ---- Airflow trigger --------------------------------------------------------------
AIRFLOW_BASE_URL = os.getenv("AIRFLOW_BASE_URL", "http://localhost:8080")
AIRFLOW_DAG_ID = os.getenv("AIRFLOW_DAG_ID", "ingest_sprint_docs_to_vector_db")
AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME", "admin")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD", "admin")
AIRFLOW_TRIGGER_ENABLED = os.getenv("AIRFLOW_TRIGGER_ENABLED", "true").lower() in (
    "1",
    "true",
    "yes",
)
