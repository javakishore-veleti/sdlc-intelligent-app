"""Discrete steps of the ask use case: retrieve -> generate -> cite."""
from typing import Any


def retrieve_chunks(retrieval_service, question, framework, strategy, filters, top_k):
    return retrieval_service.retrieve(question, framework, strategy, filters, top_k)


def generate_answer(answer_generator, question, chunks):
    return answer_generator.generate(question, chunks)


def build_citations(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    citations = []
    for c in chunks:
        m = c.get("metadata") or {}
        page = m.get("chunk_index")
        citations.append(
            {
                "document": m.get("ref_id"),
                "application": m.get("project_id"),
                "sprint": m.get("project_sprint"),
                "page": int(page) if page is not None else None,
            }
        )
    return citations
