"""Ingest facade: store file + manifest, log it (PENDING), and trigger Airflow."""
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from common.facade.interfaces.ingest_facade import IngestFacadeInterface
from facades.ingest_facade.tasks import ingest_tasks
from models.enums import IngestProcessStatus, IngestType, StorageType


class IngestFacade(IngestFacadeInterface):
    def __init__(self, storage, ingest_log_dao, airflow_trigger) -> None:
        self.storage = storage
        self.dao = ingest_log_dao
        self.trigger = airflow_trigger

    def ingest_pdf(
        self,
        db: Session,
        *,
        filename: str,
        content: bytes,
        project_id: Optional[UUID],
        project_sprint: Optional[str],
        uploaded_by: Optional[str],
    ) -> dict:
        ref_id = uuid.uuid4()
        now = datetime.utcnow()
        storage_type = StorageType(self.storage.storage_type)

        # 1) persist the physical file
        location = ingest_tasks.store_document(self.storage, str(ref_id), filename, content)

        # 2) build + persist the manifest sidecar
        manifest = {
            "id": str(ref_id),
            "project_id": str(project_id) if project_id else None,
            "pdf_file_name": filename,
            "project_sprint": project_sprint,
            "uploaded_by": uploaded_by,
            "datetime": now.isoformat(),
            "storage_type": storage_type.value,
            "storage_location": location,
            "size_bytes": len(content),
        }
        ingest_tasks.write_manifest(self.storage, str(ref_id), manifest)

        # 3) create the ingest_log row (PENDING)
        log = ingest_tasks.create_ingest_log(
            self.dao,
            db,
            {
                "ref_id": ref_id,
                "project_id": project_id,
                "project_sprint": project_sprint,
                "uploaded_by": uploaded_by,
                "file_name": filename,
                "ingest_type": IngestType.PDF,
                "storage_type": storage_type,
                "storage_location": location,
                "size_bytes": len(content),
                "ingest_process_status": IngestProcessStatus.PENDING,
                "ingest_dt": now,
            },
        )

        # 4) trigger the Airflow ingestion DAG with the UUID location
        conf = {
            "ingest_log_id": str(log.id),
            "ref_id": str(ref_id),
            "document_path": location,
            "storage_type": storage_type.value,
            "project_id": manifest["project_id"],
            "project_sprint": project_sprint,
            "uploaded_by": uploaded_by,
        }
        airflow_result = ingest_tasks.trigger_airflow(self.trigger, conf)

        return {"ingest_log": log, "manifest": manifest, "airflow": airflow_result}
