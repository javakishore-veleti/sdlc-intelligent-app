# Workspace-Service

FastAPI service — **agile delivery workspace**. Project-scoped CRUD for the work
hierarchy, consumed by the `sdlc-nexus` portal.

## Entities

```
Project (referenced by id from Master-Data-Service)
  └─ Epic ─ Feature ─ Story
Sprint, Release          time-boxes a Story can be assigned to (sprint_id / release_id)
WorkspaceMembership      which projects a user belongs to (drives access scoping)
```

Every work entity carries `project_id`. Enums: `WorkItemStatus` (epics/features/stories),
`SprintStatus`, `ReleaseStatus`.

## Access scoping (per-user / admin)

Identity comes from the **`X-User-Email`** header (a stub for real JWT auth; replacing
`auth/current_user.py` is the only change needed later).

- **Admins** (emails in `ADMIN_EMAILS`, default `admin@example.com`) — see and act on **all** projects.
- **Everyone else** — limited to projects in their `workspace_memberships`; other projects
  return `403` on read/write and are excluded from lists.
- **Memberships** are admin-only master data.

## API

| Method | Path | Scoped |
|---|---|---|
| CRUD | `/api/v1/epics`, `/features`, `/sprints`, `/releases`, `/stories` | per-user/admin |
| CRUD | `/api/v1/memberships` | admin only |

Send `X-User-Email: <email>` on requests. Swagger at `/docs`.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8002    # http://localhost:8002/docs
```

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./workspace.db` | store (Postgres in containers) |
| `ADMIN_EMAILS` | `admin@example.com` | comma-separated admin emails |

Schema is versioned with Alembic and auto-applied on startup.
