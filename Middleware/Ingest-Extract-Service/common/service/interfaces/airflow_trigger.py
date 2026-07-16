"""Contract for triggering the Airflow ingestion DAG."""
from abc import ABC, abstractmethod


class AirflowTriggerInterface(ABC):
    @abstractmethod
    def trigger_ingestion(self, conf: dict) -> dict:
        """Trigger a DAG run with ``conf``; return a small result dict.

        Must not raise on transport errors — return a result indicating failure so
        the upload itself still succeeds.
        """
