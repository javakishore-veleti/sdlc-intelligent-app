"""Extractive answer generator (no external LLM).

Returns the most relevant retrieved chunk as the grounded answer. This is the zero-dependency
default; Ollama / Groq generators implement the same interface to produce synthesized answers.
"""
from typing import Any

from common.service.interfaces.answer_generator import AnswerGeneratorInterface

_NOT_FOUND = "I couldn't find anything relevant in the ingested documentation."


class ExtractiveAnswerGenerator(AnswerGeneratorInterface):
    def generate(self, question: str, chunks: list[dict[str, Any]]) -> str:
        if not chunks:
            return _NOT_FOUND
        top = (chunks[0].get("text") or "").strip()
        return top[:1500] if top else _NOT_FOUND
