"""Triggers the Airflow ingestion DAG via the Airflow REST API."""
import httpx

from common.constants.constants import (
    AIRFLOW_BASE_URL,
    AIRFLOW_DAG_ID,
    AIRFLOW_PASSWORD,
    AIRFLOW_TRIGGER_ENABLED,
    AIRFLOW_USERNAME,
)
from common.service.interfaces.airflow_trigger import AirflowTriggerInterface


class AirflowTrigger(AirflowTriggerInterface):
    def trigger_ingestion(self, conf: dict) -> dict:
        if not AIRFLOW_TRIGGER_ENABLED:
            return {"triggered": False, "detail": "Airflow trigger disabled"}
        url = f"{AIRFLOW_BASE_URL}/api/v1/dags/{AIRFLOW_DAG_ID}/dagRuns"
        try:
            resp = httpx.post(
                url,
                json={"conf": conf},
                auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
                timeout=10.0,
            )
            resp.raise_for_status()
            return {"triggered": True, "dag_run_id": resp.json().get("dag_run_id")}
        except Exception as exc:  # network/auth issues must not fail the upload
            return {"triggered": False, "detail": f"trigger failed: {exc}"}
