"""Dashboard facade: returns cached stats, recomputing after the TTL elapses."""
from typing import Any

from sqlalchemy.orm import Session

from common.facade.interfaces.dashboard_facade import DashboardFacadeInterface
from common.service.interfaces.dashboard_service import DashboardServiceInterface
from facades.dashboard_facade.tasks import dashboard_tasks
from utils.cache import TTLCache

_CACHE_KEY = "dashboard_stats"


class DashboardFacade(DashboardFacadeInterface):
    def __init__(self, service: DashboardServiceInterface, cache: TTLCache) -> None:
        self.service = service
        self.cache = cache

    def get_stats(self, db: Session) -> dict[str, Any]:
        return self.cache.get_or_set(
            _CACHE_KEY, lambda: dashboard_tasks.compute_dashboard_stats(self.service, db)
        )

    def invalidate(self) -> None:
        self.cache.invalidate(_CACHE_KEY)
