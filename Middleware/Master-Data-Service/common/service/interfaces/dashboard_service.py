"""Service-layer contract for dashboard statistics."""
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session


class DashboardServiceInterface(ABC):
    @abstractmethod
    def compute_stats(self, db: Session) -> dict[str, Any]: ...
