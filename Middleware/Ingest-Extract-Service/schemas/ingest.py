"""Request/response schemas for ingestion."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from models.enums import IngestProcessStatus, IngestType, StorageType


class Manifest(BaseModel):
    id: str
    project_id: Optional[str] = None
    pdf_file_name: str
    project_sprint: Optional[str] = None
    uploaded_by: Optional[str] = None
    datetime: str
    storage_type: str
    storage_location: str
    size_bytes: int


class AirflowTriggerResult(BaseModel):
    triggered: bool
    dag_run_id: Optional[str] = None
    detail: Optional[str] = None


class IngestLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ref_id: UUID
    project_id: Optional[UUID] = None
    project_sprint: Optional[str] = None
    uploaded_by: Optional[str] = None
    file_name: str
    ingest_type: IngestType
    storage_type: StorageType
    storage_location: Optional[str] = None
    size_bytes: Optional[int] = None
    ingest_process_status: IngestProcessStatus
    ingest_dt: Optional[datetime] = None
    ingest_process_start_dt: Optional[datetime] = None
    ingest_process_complete_dt: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class IngestResponse(BaseModel):
    ingest_log: IngestLogRead
    manifest: Manifest
    airflow: AirflowTriggerResult
