"""Facade-layer contract for dashboard statistics (with caching)."""
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session


class DashboardFacadeInterface(ABC):
    @abstractmethod
    def get_stats(self, db: Session) -> dict[str, Any]: ...

    @abstractmethod
    def invalidate(self) -> None: ...
