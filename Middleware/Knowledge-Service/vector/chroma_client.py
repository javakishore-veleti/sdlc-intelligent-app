"""ChromaDB client factory (cached singleton) + collection naming."""
import functools

import chromadb

from common.constants.constants import (
    CHROMA_HOST,
    CHROMA_MODE,
    CHROMA_PERSIST_DIR,
    CHROMA_PORT,
)


@functools.lru_cache(maxsize=1)
def get_chroma_client():
    if CHROMA_MODE == "ephemeral":
        return chromadb.EphemeralClient()
    if CHROMA_MODE == "persistent":
        return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)


def collection_name(framework: str, strategy: str) -> str:
    """Collections are named '<framework>__<strategy>' (as written by the DAG)."""
    return f"{framework}__{strategy}"


def list_collection_names() -> list[str]:
    client = get_chroma_client()
    return [getattr(c, "name", c) for c in client.list_collections()]
