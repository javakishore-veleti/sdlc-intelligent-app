"""Tasks invoked by the dashboard facade."""
from typing import Any

from sqlalchemy.orm import Session

from common.service.interfaces.dashboard_service import DashboardServiceInterface


def compute_dashboard_stats(service: DashboardServiceInterface, db: Session) -> dict[str, Any]:
    return service.compute_stats(db)
