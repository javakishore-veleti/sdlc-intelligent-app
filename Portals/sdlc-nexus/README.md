# sdlc-nexus

Angular portal for **customers** — the central hub where Developers, Product Owners,
Product Managers, and Project Managers work with the team's sprint knowledge.

## Areas

| Menu | Contents | Backend |
|---|---|---|
| **Workspace** | Browse Epics / Features / Sprints / Releases / Stories (scoped to your projects) | Workspace-Service (8002) |
| **Upload** | Upload a sprint PDF → datalake + ingestion; recent-ingest history | Ingest-Extract-Service (8003) |
| **Assistant** | Chat over sprint docs, with citations | Knowledge-Service (8004, *not built yet*) |

## Per-user scoping

The top bar has a **"Signed in as"** email selector — a stand-in for real login. Its value
is attached as the **`X-User-Email`** header on every request (see
`core/services/user-header.interceptor.ts`), which Workspace-Service uses to scope data:
`admin@example.com` sees all projects; other users see only projects they're a member of.

## Run

```bash
npm install
npm start            # ng serve -> http://localhost:4200
```

Start the backends first (or run the full stack via `cicd/Local/docker-all-up.sh`):
- Workspace-Service on 8002, Ingest-Extract-Service on 8003.
- The **Assistant** degrades gracefully with a friendly message until Knowledge-Service (8004) exists.

Backend URLs live in `src/environments/environment.ts`.

## Build

```bash
npm run build        # ng build -> dist/sdlc-nexus
```

## Structure

```
src/app/
├── app.component.ts            top bar (nav + user selector) + router-outlet
├── app.config.ts             providers incl. X-User-Email interceptor
├── app.routes.ts             workspace / upload / assistant
├── core/
│   ├── models/               DTO interfaces
│   ├── services/             user-context, interceptor, workspace, ingest, knowledge
│   └── utils/                BatchPaginator
└── features/
    ├── workspace/  (tabbed browse of the 5 entities)
    ├── upload/     (PDF upload + recent ingests)
    └── assistant/  (chat with citations)
```
