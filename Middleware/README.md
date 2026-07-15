# Middleware

FastAPI services that make up the API plane of the SDLC Intelligent App.

| Service | Role |
|---|---|
| **MasterDataAPI** | Admin write plane — business applications (projects), sprints, agendas |
| **DevLifeCycleAPI** | Customer read plane — fetch applications and sprints |
| **Ingest-API** | Receives uploaded PDFs and triggers Airflow ingestion |
| **QnA-API** | LangChain retrieval + LLM question answering over ChromaDB |

See [`../PRD.md`](../PRD.md) for the full API surface and architecture.
