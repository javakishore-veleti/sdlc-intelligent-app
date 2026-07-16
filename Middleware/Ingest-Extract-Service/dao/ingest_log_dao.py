"""DAO for the ingest_log table."""
from dao.base_dao_impl import BaseDao
from models.entities import IngestLog


class IngestLogDao(BaseDao[IngestLog]):
    def __init__(self) -> None:
        super().__init__(IngestLog)
