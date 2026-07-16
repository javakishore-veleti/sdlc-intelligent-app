"""Service-wide configuration for Knowledge-Service."""
import os

SERVICE_NAME = "Knowledge-Service"
SERVICE_VERSION = "0.1.0"
API_V1_PREFIX = "/api/v1"

# ---- Vector DB (ChromaDB) ----------------------------------------------------------
# http (default) connects to a Chroma server; ephemeral/persistent run in-process.
CHROMA_MODE = os.getenv("CHROMA_MODE", "http")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma-data")

# Must match the embedding the ingestion DAG used to index the chunks.
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "256"))

# ---- Retrieval defaults ------------------------------------------------------------
# Collections are named "<framework>__<strategy>"; pick which to query by default.
DEFAULT_FRAMEWORK = os.getenv("DEFAULT_FRAMEWORK", "langchain")  # langchain | langgraph
DEFAULT_STRATEGY = os.getenv("DEFAULT_STRATEGY", "recursive_char_2000_200")
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "4"))

# ---- Answer generation -------------------------------------------------------------
# extractive (default, no external deps) | ollama | groq (future)
ANSWER_BACKEND = os.getenv("ANSWER_BACKEND", "extractive")
