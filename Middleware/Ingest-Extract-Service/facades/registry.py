"""Wires the ingest facade with its storage backend, DAO, and Airflow trigger."""
from dao.ingest_log_dao import IngestLogDao
from facades.ingest_facade import IngestFacade
from services.airflow_trigger_impl import AirflowTrigger
from storage.factory import get_storage_backend


def build_ingest_facade() -> IngestFacade:
    return IngestFacade(
        storage=get_storage_backend(),
        ingest_log_dao=IngestLogDao(),
        airflow_trigger=AirflowTrigger(),
    )
