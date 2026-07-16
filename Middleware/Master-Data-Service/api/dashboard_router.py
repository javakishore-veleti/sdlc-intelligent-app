"""Dashboard statistics endpoint (cached, configurable eviction)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_db
from common.constants.constants import DASHBOARD_CACHE_TTL_SECONDS
from dao.stats_dao_impl import StatsDao
from facades.dashboard_facade import DashboardFacade
from schemas.dashboard import DashboardStats
from services.dashboard_service_impl import DashboardService
from utils.cache import TTLCache

# Process-wide singletons so the cache is shared across requests.
_cache = TTLCache(ttl_seconds=DASHBOARD_CACHE_TTL_SECONDS)
_dashboard_facade = DashboardFacade(DashboardService(StatsDao()), _cache)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Return project count and top-10 tech stacks. Cached with a 6h (configurable) TTL."""
    return _dashboard_facade.get_stats(db)
