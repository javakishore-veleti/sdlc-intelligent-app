"""Computes dashboard statistics from the stats DAO."""
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from common.constants.constants import DASHBOARD_CACHE_TTL_SECONDS
from common.dao.interfaces.stats_dao import StatsDaoInterface
from common.service.interfaces.dashboard_service import DashboardServiceInterface


class DashboardService(DashboardServiceInterface):
    def __init__(self, stats_dao: StatsDaoInterface) -> None:
        self.stats_dao = stats_dao

    def compute_stats(self, db: Session) -> dict[str, Any]:
        return {
            "project_count": self.stats_dao.count_projects(db),
            "top_tech_stacks": self.stats_dao.top_tech_stacks(db, limit=10),
            "generated_at": datetime.utcnow(),
            "cache_ttl_seconds": DASHBOARD_CACHE_TTL_SECONDS,
        }
