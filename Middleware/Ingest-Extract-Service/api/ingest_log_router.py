"""Read endpoints for ingest logs."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.deps import get_db
from dao.ingest_log_dao import IngestLogDao
from schemas.ingest import IngestLogRead

router = APIRouter(prefix="/ingest-logs", tags=["Ingest Logs"])
_dao = IngestLogDao()


@router.get("", response_model=list[IngestLogRead])
def list_ingest_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return _dao.list(db, skip, limit, None)


@router.get("/{log_id}", response_model=IngestLogRead)
def get_ingest_log(log_id: UUID, db: Session = Depends(get_db)):
    obj = _dao.get(db, log_id)
    if obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    return obj
