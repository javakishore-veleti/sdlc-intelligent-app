# SDLC Intelligent App

> Turn a software team's evolving sprint documentation into an instantly queryable,
> citation-backed knowledge base.

Software teams generate a continuous stream of requirement and feature documents —
sprint after sprint, across many microservice applications. That knowledge quickly
becomes scattered and hard to search, trace, or reason about. **SDLC Intelligent App**
makes it **searchable, current-aware, and traceable**, organized around the natural
SDLC hierarchy of *application → sprint → feature*.

## What it does

- **Manage SDLC master data** — register the business applications (microservices)
  under development and define their sprints (with agendas).
- **Ingest sprint documents** — upload feature/requirement PDFs; they are parsed,
  chunked, embedded, and indexed automatically.
- **Ask questions across all sprints** — a Retrieval-Augmented Generation (RAG)
  assistant answers natural-language questions with **explicit citations** back to the
  source document, application, sprint, and page.
- **Stay current-aware** — when a rule or feature evolves across sprints, the assistant
  surfaces the evolution and identifies the most recent version.

## Who it's for

Two portals serve two persona groups:

| Portal | Users | Purpose |
|---|---|---|
| **SoftwareDev-Admin** | Administrators | Register applications; define sprints and agendas |
| **RequirementsEngineering** | Developers, Product Owners, Product Managers, Project Managers | Upload sprint PDFs, browse applications/sprints, and ask the assistant |

## Architecture at a glance

```
Angular portals (admin + requirements-engineering)
        │  REST/JSON
FastAPI middleware
   MasterDataAPI · DevLifeCycleAPI · Ingest-API · QnA-API
        │
Apache Airflow (ingestion) ──► ChromaDB (vectors + metadata)
PostgreSQL (master data)          LangChain RAG ──► LLM (local or hosted)
```

- **Separation of planes** — `MasterDataAPI` (admin writes) vs. `DevLifeCycleAPI`
  (customer reads).
- **Pluggable ingestion source** — manual portal entry now; an automated source can
  plug into the same interface later.
- **Provenance-first RAG** — metadata (application, sprint, page, document) travels with
  every chunk so every answer can be cited.

## Repository layout

```
sdlc-intelligent-app/
├── PRD.md                          # full Product Requirements Document
├── portals/                        # Angular front-ends (admin + requirements-engineering)
├── Middleware/                     # FastAPI services (MasterData, DevLifeCycle, Ingest, QnA)
├── airflow/                        # ingestion DAG(s): parse → chunk → embed → ChromaDB
├── corpus/                         # synthetic sample sprint documents
├── infra/                          # container/compose definitions, env templates
└── docs/                           # architecture, design, and presentation material
```

## Status

Early stage. The product is specified in the **[Product Requirements Document](./PRD.md)**;
implementation is planned to proceed in phases, starting with a thin end-to-end vertical
slice (one application → one sprint → one uploaded document → one cited answer).

## Documentation

- **[PRD.md](./PRD.md)** — complete requirements, architecture, data model, API surface,
  RAG design, roadmap, and open decisions.

## Note on data

All sample domain content in this repository is **synthetic and illustrative**. No real,
proprietary, or confidential data is included.
