"""Deterministic hash embedding.

MUST match the embedding used by the ingestion DAG (SDLC-Workflows) so that a query
vector lands in the same space as the indexed chunk vectors. Swap both sides for a real
embedder (Ollama / HuggingFace / OpenAI) together.
"""
import hashlib

from common.constants.constants import EMBEDDING_DIM


def deterministic_embedding(text: str) -> list[float]:
    vec = [0.0] * EMBEDDING_DIM
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    for i, byte in enumerate(digest):
        vec[i % EMBEDDING_DIM] += byte / 255.0
    return vec
