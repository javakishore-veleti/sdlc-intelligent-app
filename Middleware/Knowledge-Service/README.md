# Knowledge-Service

FastAPI service — **knowledge / question answering**.

Serves the RAG assistant: metadata-filtered retrieval over ChromaDB plus LLM answer
generation with citations and conversational memory. Consumed by the `sdlc-nexus`
portal chatbot.

Follows the standard layered layout (`api` → `facades`/`tasks` → service → `dao`,
with interfaces in `common/`). See [`../README.md`](../README.md).
