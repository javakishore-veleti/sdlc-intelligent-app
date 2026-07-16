"""Discrete steps of the ingest use case."""


def store_document(storage, ref_id: str, filename: str, content: bytes) -> str:
    return storage.save_file(ref_id, filename, content)


def write_manifest(storage, ref_id: str, manifest: dict) -> str:
    return storage.save_manifest(ref_id, manifest)


def create_ingest_log(dao, db, data: dict):
    return dao.create(db, data)


def trigger_airflow(trigger, conf: dict) -> dict:
    return trigger.trigger_ingestion(conf)
