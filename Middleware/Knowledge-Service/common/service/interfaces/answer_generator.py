"""Contract for turning retrieved chunks into an answer."""
from abc import ABC, abstractmethod
from typing import Any


class AnswerGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, question: str, chunks: list[dict[str, Any]]) -> str: ...
