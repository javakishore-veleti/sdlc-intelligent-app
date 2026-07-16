"""ORM models for Ingest-Extract-Service."""
from sqlalchemy import Column, DateTime, Enum as SAEnum, Integer, String, Text, Uuid

from db.base import Base
from models.enums import IngestProcessStatus, IngestType, StorageType
from models.mixins import TimestampMixin, UUIDPkMixin


class IngestLog(UUIDPkMixin, TimestampMixin, Base):
    """One row per uploaded document, tracking its ingestion lifecycle.

    Created as PENDING on upload; the Airflow DAG advances it to IN_PROGRESS
    (setting ``ingest_process_start_dt``) and then COMPLETED / FAILED
    (setting ``ingest_process_complete_dt``).
    """
    __tablename__ = "ingest_log"

    # The datalake UUID the physical file + manifest are stored under.
    ref_id = Column(Uuid, nullable=False, index=True)

    # Source metadata (project comes from Master-Data-Service; referenced by id).
    project_id = Column(Uuid, nullable=True, index=True)
    project_sprint = Column(String(200))
    uploaded_by = Column(String(200))  # user id / employee id
    file_name = Column(String(512), nullable=False)

    ingest_type = Column(SAEnum(IngestType), nullable=False, default=IngestType.PDF)
    storage_type = Column(
        SAEnum(StorageType), nullable=False, default=StorageType.LOCAL_FILE_SYSTEM
    )
    storage_location = Column(String(1024))
    size_bytes = Column(Integer)

    ingest_process_status = Column(
        SAEnum(IngestProcessStatus),
        nullable=False,
        default=IngestProcessStatus.PENDING,
        index=True,
    )
    ingest_dt = Column(DateTime)  # when the file was uploaded
    ingest_process_start_dt = Column(DateTime)  # DAG started processing
    ingest_process_complete_dt = Column(DateTime)  # DAG finished
    error = Column(Text)
