# Knowledge-Service

FastAPI service — **RAG assistant**. Answers questions from the ingested documentation
and returns citations. Consumed by the `sdlc-nexus` portal's Assistant.

## How it works

```
POST /api/v1/ask {question, framework?, strategy?, project_id?, project_sprint?, top_k?}
  1. embed the question (same deterministic embedding the ingestion DAG used)
  2. query ChromaDB collection  <framework>__<strategy>  (metadata-filtered)
  3. generate an answer from the top chunks (pluggable generator)
  4. return answer + citations (document, application, sprint, chunk)
```

Because LangChain and LangGraph ingest into **separate collections**, you can ask the
same question against `framework=langchain` vs `framework=langgraph` and compare.

- **Embedding** must match the DAG (`EMBEDDING_DIM`, same hash function) — swap both together.
- **Answer generator** is pluggable (`ANSWER_BACKEND`): `extractive` (default, no LLM) →
  returns the most relevant chunk; `ollama` / `groq` slot in for synthesized answers.

## API

- `POST /api/v1/ask` — ask a question (body above) → `{answer, framework, strategy, citations, retrieved}`
- `GET  /api/v1/collections` — list vector-DB collections (e.g. `langchain__…`, `langgraph__…`)
- Swagger at `/docs`.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8004     # http://localhost:8004/docs
```

| Variable | Default | Purpose |
|---|---|---|
| `CHROMA_MODE` | `http` | `http` (server) \| `ephemeral` \| `persistent` |
| `CHROMA_HOST` / `CHROMA_PORT` | `localhost` / `8000` | Chroma server |
| `EMBEDDING_DIM` | `256` | must equal the DAG's |
| `DEFAULT_FRAMEWORK` | `langchain` | which collections to query by default |
| `ANSWER_BACKEND` | `extractive` | `extractive` \| `ollama` \| `groq` |
