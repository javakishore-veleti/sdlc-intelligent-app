"""Airflow DAG: ingest a document into the vector DB via two frameworks.

Flow (triggered on demand by Ingest-Extract-Service with a document reference in
``dag_run.conf``):

    mark_in_progress -> extract_text ->  [ langchain_ingest , langgraph_ingest ] -> mark_completed
                                              (on any failure) -> mark_failed

- ``extract_text``     reads the PDF with **pypdf**.
- ``langchain_ingest`` chunks + embeds with **LangChain** and upserts into a
  ``langchain__<strategy>`` collection.
- ``langgraph_ingest`` runs the same steps orchestrated as a **LangGraph** state graph
  and upserts into a separate ``langgraph__<strategy>`` collection.

Keeping each framework in its own collection lets you compare LangChain vs LangGraph
(and, later, multiple chunking strategies — one collection per strategy).

``dag_run.conf`` keys: ingest_log_id, ref_id, document_path, project_id,
project_sprint, uploaded_by.

Heavy libraries (pypdf / langchain / langgraph / chromadb) are imported *inside* the
tasks so the DAG file parses even where those libs aren't installed. Requires, at run
time: pypdf, langchain-text-splitters, langchain-core, langgraph, chromadb, plus a
reachable Chroma and the ingest Postgres DB.
"""
from __future__ import annotations

import hashlib
import logging
import os
from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.utils.trigger_rule import TriggerRule

log = logging.getLogger(__name__)

# ---- Configuration ----------------------------------------------------------------
INGEST_DATABASE_URL = os.getenv(
    "INGEST_DATABASE_URL", "postgresql+psycopg2://sdlc:sdlc@postgres:5432/ingest"
)
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "256"))

# Registry of chunking strategies. Add entries here to ingest the same document under
# multiple strategies, each into its own pair of collections.
CHUNKING_STRATEGIES = [
    {"name": "recursive_char_2000_200", "chunk_size": 2000, "chunk_overlap": 200},
]


# ---- Small helpers (kept dependency-light; heavy imports live in the tasks) --------
def _conf() -> dict:
    ctx = get_current_context()
    dag_run = ctx.get("dag_run")
    return (dag_run.conf or {}) if dag_run else {}


def _set_status(ingest_log_id, status, **timestamps) -> None:
    """Update the ingest_log row via SQLAlchemy core (no ORM models needed here)."""
    if not ingest_log_id:
        log.warning("No ingest_log_id in conf; skipping status update to %s", status)
        return
    from sqlalchemy import create_engine, text

    engine = create_engine(INGEST_DATABASE_URL, future=True)
    sets = ["ingest_process_status = :status"]
    params = {"status": status, "id": ingest_log_id}
    for col, val in timestamps.items():
        sets.append(f"{col} = :{col}")
        params[col] = val
    stmt = text(f"UPDATE ingest_log SET {', '.join(sets)} WHERE id = :id")
    with engine.begin() as conn:
        conn.execute(stmt, params)


def _deterministic_embedding(chunk: str) -> list[float]:
    """Placeholder embedding: deterministic hash -> vector. Swap for a real embedder
    (Ollama / HuggingFace / OpenAI) when moving beyond the learning skeleton."""
    vec = [0.0] * EMBEDDING_DIM
    digest = hashlib.sha256(chunk.encode("utf-8")).digest()
    for i, byte in enumerate(digest):
        vec[i % EMBEDDING_DIM] += byte / 255.0
    return vec


def _upsert_to_chroma(collection_name: str, chunks: list[str], base_meta: dict) -> int:
    import chromadb

    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    collection = client.get_or_create_collection(collection_name)
    ids = [f"{base_meta.get('ref_id', 'doc')}-{i}" for i in range(len(chunks))]
    metadatas = [{**base_meta, "chunk_index": i} for i in range(len(chunks))]
    embeddings = [_deterministic_embedding(c) for c in chunks]
    collection.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)
    return len(chunks)


@dag(
    dag_id="ingest_sprint_docs_to_vector_db",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ingestion", "vector-db", "langchain", "langgraph", "sdlc"],
)
def ingest_sprint_docs_to_vector_db():
    @task
    def mark_in_progress() -> dict:
        conf = _conf()
        _set_status(
            conf.get("ingest_log_id"),
            "IN_PROGRESS",
            ingest_process_start_dt=datetime.utcnow(),
        )
        return conf

    @task
    def extract_text(conf: dict) -> dict:
        from pypdf import PdfReader

        path = conf.get("document_path")
        log.info("Extracting text from %s with pypdf", path)
        reader = PdfReader(path)
        pages = [(page.extract_text() or "") for page in reader.pages]
        return {
            "conf": conf,
            "text": "\n".join(pages),
            "num_pages": len(pages),
        }

    @task
    def langchain_ingest(extracted: dict) -> dict:
        """LangChain branch: split with LangChain, upsert per strategy."""
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        conf = extracted["conf"]
        base_meta = {
            "ref_id": conf.get("ref_id"),
            "project_id": conf.get("project_id"),
            "project_sprint": conf.get("project_sprint"),
            "framework": "langchain",
        }
        results = {}
        for strat in CHUNKING_STRATEGIES:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=strat["chunk_size"], chunk_overlap=strat["chunk_overlap"]
            )
            chunks = splitter.split_text(extracted["text"])
            collection = f"langchain__{strat['name']}"
            n = _upsert_to_chroma(collection, chunks, {**base_meta, "strategy": strat["name"]})
            log.info("LangChain upserted %d chunks into %s", n, collection)
            results[collection] = n
        return results

    @task
    def langgraph_ingest(extracted: dict) -> dict:
        """LangGraph branch: same steps orchestrated as a state graph, separate collections."""
        from typing import TypedDict

        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langgraph.graph import END, START, StateGraph

        conf = extracted["conf"]

        class State(TypedDict):
            text: str
            strategy: dict
            collection: str
            chunks: list
            upserted: int
            base_meta: dict

        def chunk_node(state: State) -> State:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=state["strategy"]["chunk_size"],
                chunk_overlap=state["strategy"]["chunk_overlap"],
            )
            state["chunks"] = splitter.split_text(state["text"])
            return state

        def upsert_node(state: State) -> State:
            state["upserted"] = _upsert_to_chroma(
                state["collection"], state["chunks"], state["base_meta"]
            )
            return state

        builder = StateGraph(State)
        builder.add_node("chunk", chunk_node)
        builder.add_node("upsert", upsert_node)
        builder.add_edge(START, "chunk")
        builder.add_edge("chunk", "upsert")
        builder.add_edge("upsert", END)
        graph = builder.compile()

        results = {}
        for strat in CHUNKING_STRATEGIES:
            collection = f"langgraph__{strat['name']}"
            base_meta = {
                "ref_id": conf.get("ref_id"),
                "project_id": conf.get("project_id"),
                "project_sprint": conf.get("project_sprint"),
                "framework": "langgraph",
                "strategy": strat["name"],
            }
            final = graph.invoke(
                {
                    "text": extracted["text"],
                    "strategy": strat,
                    "collection": collection,
                    "chunks": [],
                    "upserted": 0,
                    "base_meta": base_meta,
                }
            )
            log.info("LangGraph upserted %d chunks into %s", final["upserted"], collection)
            results[collection] = final["upserted"]
        return results

    @task
    def mark_completed(extracted: dict, lc: dict, lg: dict) -> None:
        conf = extracted["conf"]
        _set_status(
            conf.get("ingest_log_id"),
            "COMPLETED",
            ingest_process_complete_dt=datetime.utcnow(),
        )
        log.info("Ingestion complete. LangChain=%s LangGraph=%s", lc, lg)

    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def mark_failed() -> None:
        conf = _conf()
        _set_status(
            conf.get("ingest_log_id"),
            "FAILED",
            ingest_process_complete_dt=datetime.utcnow(),
        )

    conf = mark_in_progress()
    extracted = extract_text(conf)
    lc = langchain_ingest(extracted)
    lg = langgraph_ingest(extracted)
    done = mark_completed(extracted, lc, lg)

    # If any upstream task fails, mark the log FAILED.
    [extracted, lc, lg, done] >> mark_failed()


ingest_sprint_docs_to_vector_db()
