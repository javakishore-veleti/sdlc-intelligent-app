"""Facade contract for the question-answering use case."""
from abc import ABC, abstractmethod
from typing import Any, Optional


class QaFacadeInterface(ABC):
    @abstractmethod
    def ask(
        self,
        question: str,
        framework: str,
        strategy: str,
        filters: Optional[dict[str, Any]] = None,
        top_k: int = 4,
    ) -> dict[str, Any]: ...
