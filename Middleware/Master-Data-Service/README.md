# Master-Data-Service

FastAPI service — **admin write plane**. CRUD for the SDLC master data consumed by the
`sdlc-admin` portal.

## Entities

| Group | Entity | Notes |
|---|---|---|
| People | **Employee** | |
| Core | **Project** | one per microservice / business application |
| Roles | **ProjectRole** | roles defined within a project |
| Assignment | **ProjectEmployee** | (project × employee × role); an employee may hold multiple roles and belong to multiple projects |
| Assets | **ProjectArtifact**, **ProjectKnowledgeBase** | many per project |
| Capabilities | **ProjectCapability** | typed: `API`, `EVENT_PUBLISH`, `EVENT_CONSUMER`, `ETL`, `VECTOR_DATABASE`, `MCP_SERVER` |
| Structure | **ProjectDomain** | hierarchical sub-domains (self-referencing) |
| Tech | **ProjectTechStack** | typed: `LANGUAGE`, `FRAMEWORK`, `DATABASE`, `RULE_ENGINE`, … |
| Dependencies | **ProjectDependency**, **ProjectDependencyGroup** | a dependency targets another project's capability; groups bundle related dependencies |
| Clients | **ProjectClient**, **ProjectClientGroup** | another project consuming this project's capability; groups bundle related clients |

## Layered layout

```
api/            FastAPI routers (generic CRUD router factory)
facades/        crud_facade/  -> tasks/   (orchestration)
services/       service implementations
dao/            SQLAlchemy CRUD implementation
common/
  service/interfaces/   facade/interfaces/   dao/interfaces/   constants/
utils/
models/         SQLAlchemy ORM models + enums
schemas/        Pydantic request/response models
db/             engine + session + declarative base
alembic/        versioned DB migrations
```

Dependency direction: `api → facades (+ tasks) → services → dao`, with all cross-layer
contracts declared as interfaces under `common/`.

## Database migrations (Alembic)

The schema is **versioned** and **auto-applied on startup** — the app runs
`alembic upgrade head` in its lifespan hook, so the database is brought up to date every
time the service starts (the Liquibase-style behavior requested).

```bash
# after changing models, generate a new versioned migration:
alembic revision --autogenerate -m "describe change"
# apply migrations manually (also runs automatically at app startup):
alembic upgrade head
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# defaults to a local SQLite DB; override with DATABASE_URL for Postgres
uvicorn main:app --reload --port 8001
```

## API docs (OpenAPI / Swagger)

Once running:

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc
- **OpenAPI JSON:** http://localhost:8001/openapi.json
- **Health:** http://localhost:8001/health

All routes are served under `/api/v1` (e.g. `POST /api/v1/projects`).

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./master_data.db` | SQLAlchemy DB URL; use `postgresql+psycopg2://…` in containers |

See [`../README.md`](../README.md) for the middleware overview.
