"""Wires the QA facade with its retrieval service and answer generator."""
from facades.qa_facade import QaFacade
from services.answer_factory import get_answer_generator
from services.retrieval_service_impl import RetrievalService


def build_qa_facade() -> QaFacade:
    return QaFacade(
        retrieval_service=RetrievalService(),
        answer_generator=get_answer_generator(),
    )
