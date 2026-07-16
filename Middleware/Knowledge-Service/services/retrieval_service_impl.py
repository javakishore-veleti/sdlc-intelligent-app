"""ChromaDB-backed retrieval using the shared deterministic embedding."""
from typing import Any, Optional

from common.service.interfaces.retrieval_service import RetrievalServiceInterface
from vector.chroma_client import collection_name, get_chroma_client
from vector.embedding import deterministic_embedding


def _build_where(filters: Optional[dict[str, Any]]):
    conds = [{k: v} for k, v in (filters or {}).items() if v is not None]
    if not conds:
        return None
    return conds[0] if len(conds) == 1 else {"$and": conds}


class RetrievalService(RetrievalServiceInterface):
    def retrieve(self, question, framework, strategy, filters=None, top_k=4):
        client = get_chroma_client()
        collection = client.get_or_create_collection(collection_name(framework, strategy))
        result = collection.query(
            query_embeddings=[deterministic_embedding(question)],
            n_results=top_k,
            where=_build_where(filters),
        )
        documents = (result.get("documents") or [[]])[0]
        metadatas = (result.get("metadatas") or [[]])[0]
        distances = (result.get("distances") or [[]])[0]
        chunks = []
        for i, text in enumerate(documents):
            chunks.append(
                {
                    "text": text,
                    "metadata": metadatas[i] if i < len(metadatas) else {},
                    "distance": distances[i] if i < len(distances) else None,
                }
            )
        return chunks
