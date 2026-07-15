# Middleware

FastAPI-based microservices that make up the API plane of the SDLC Intelligent App.

## Services

| Service | Role |
|---|---|
| **[Master-Data-Service](./Master-Data-Service)** | Admin write plane — business applications (projects), sprints, agendas |
| **[Workspace-Service](./Workspace-Service)** | Customer read/workspace plane — browse applications, sprints, and documents |
| **[Ingest-Extract-Service](./Ingest-Extract-Service)** | Receives uploaded PDFs, extracts content, and drives ingestion (Airflow) |
| **[Knowledge-Service](./Knowledge-Service)** | LangChain retrieval + LLM question answering over ChromaDB |

## Standard service layout

Every `*-Service` follows the same layered structure. Dependencies point **inward**
toward interfaces defined in `common/`, so implementations can vary without changing
callers.

```
<Service>/                       # project root (hyphenated; not a Python package)
├── api/                         # FastAPI routers / endpoints (delegates to facades)
├── facades/                     # facade implementations (orchestration)
│   └── <feature>_facade/        # each facade is its own package...
│       └── tasks/               # ...containing a tasks module (unit-of-work steps)
├── dao/                         # DAO implementations (data access)
├── common/
│   ├── service/interfaces/      # service-layer interfaces (contracts)
│   ├── facade/interfaces/       # facade-layer interfaces (contracts)
│   ├── dao/interfaces/          # DAO-layer interfaces (contracts)
│   └── constants/               # shared constants
└── utils/                       # cross-cutting utilities
```

### Layering convention

```
api  ──►  facades (+ tasks)  ──►  service impls  ──►  dao
              │                        │                │
              └────────── depend on interfaces in common/ ──────────┘
```

- **api** — thin HTTP layer; validates input, calls a facade, shapes the response.
- **facades** — orchestrate a use case; each facade is a package with a `tasks/`
  module holding the discrete steps of that use case.
- **service interfaces** (`common/service/interfaces`) — business-logic contracts.
- **dao** — persistence; implements `common/dao/interfaces`.
- **common/constants**, **utils** — shared, dependency-free helpers.

> To add a facade: create `facades/<feature>_facade/` with an `__init__.py` and a
> `tasks/` subpackage, implement the matching interface in
> `common/facade/interfaces/`, and wire it from `api/`.

See [`../PRD.md`](../PRD.md) for the API surface and end-to-end architecture.
