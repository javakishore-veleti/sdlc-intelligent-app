"""Contract for vector retrieval."""
from abc import ABC, abstractmethod
from typing import Any, Optional


class RetrievalServiceInterface(ABC):
    @abstractmethod
    def retrieve(
        self,
        question: str,
        framework: str,
        strategy: str,
        filters: Optional[dict[str, Any]] = None,
        top_k: int = 4,
    ) -> list[dict[str, Any]]:
        """Return top-k chunks: [{text, metadata, distance}, ...]."""
