"""Selects the answer generator from configuration."""
from common.constants.constants import ANSWER_BACKEND
from common.service.interfaces.answer_generator import AnswerGeneratorInterface
from services.extractive_answer import ExtractiveAnswerGenerator


def get_answer_generator() -> AnswerGeneratorInterface:
    if ANSWER_BACKEND == "extractive":
        return ExtractiveAnswerGenerator()
    # Future: "ollama" -> OllamaAnswerGenerator(), "groq" -> GroqAnswerGenerator()
    raise ValueError(f"Unsupported ANSWER_BACKEND: {ANSWER_BACKEND!r}")
