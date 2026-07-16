"""PDF upload endpoint."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from api.deps import get_db
from common.constants.constants import MAX_UPLOAD_BYTES
from facades.registry import build_ingest_facade
from schemas.ingest import IngestResponse

router = APIRouter(prefix="/ingest", tags=["Ingestion"])
_facade = build_ingest_facade()


@router.post("/uploads", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    file: UploadFile = File(...),
    project_id: UUID = Form(...),
    project_sprint: Optional[str] = Form(default=None),
    uploaded_by: Optional[str] = Form(default=None),
    db: Session = Depends(get_db),
):
    """Store a PDF in the datalake, log it (PENDING), and trigger Airflow ingestion."""
    name = (file.filename or "").strip()
    if not name.lower().endswith(".pdf") and file.content_type != "application/pdf":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Only PDF files are accepted")
    content = await file.read()
    if not content:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Empty file")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "File too large")

    return _facade.ingest_pdf(
        db,
        filename=name,
        content=content,
        project_id=project_id,
        project_sprint=project_sprint,
        uploaded_by=uploaded_by,
    )
