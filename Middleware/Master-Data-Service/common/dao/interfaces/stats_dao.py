"""DAO-layer contract for aggregate/statistics queries."""
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session


class StatsDaoInterface(ABC):
    @abstractmethod
    def count_projects(self, db: Session) -> int: ...

    @abstractmethod
    def top_tech_stacks(self, db: Session, limit: int = 10) -> list[dict[str, Any]]: ...
