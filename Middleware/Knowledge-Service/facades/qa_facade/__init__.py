"""QA facade: retrieve from the vector DB, generate an answer, attach citations."""
from typing import Any, Optional

from common.facade.interfaces.qa_facade import QaFacadeInterface
from facades.qa_facade.tasks import qa_tasks


class QaFacade(QaFacadeInterface):
    def __init__(self, retrieval_service, answer_generator) -> None:
        self.retrieval_service = retrieval_service
        self.answer_generator = answer_generator

    def ask(
        self,
        question: str,
        framework: str,
        strategy: str,
        filters: Optional[dict[str, Any]] = None,
        top_k: int = 4,
    ) -> dict[str, Any]:
        chunks = qa_tasks.retrieve_chunks(
            self.retrieval_service, question, framework, strategy, filters, top_k
        )
        answer = qa_tasks.generate_answer(self.answer_generator, question, chunks)
        citations = qa_tasks.build_citations(chunks)
        return {
            "answer": answer,
            "framework": framework,
            "strategy": strategy,
            "citations": citations,
            "retrieved": chunks,
        }
