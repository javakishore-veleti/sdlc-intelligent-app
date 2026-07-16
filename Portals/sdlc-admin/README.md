# sdlc-admin

Angular portal for **administrators** — the admin UI of the SDLC Intelligent App.

## Top-level areas

| Menu | Contents |
|---|---|
| **Dashboard** | No. of Projects + Top-10 Tech Stacks by project count (from the cached Master-Data-Service stats endpoint) |
| **Entitlements** | Left nav → **Users** (paged list of employees) |
| **Projects** | Left nav → **Projects**, **Project Dependencies**, **Project Tech Stack** |

## Pagination model

List screens use `BatchPaginator` (`src/app/core/utils/batch-paginator.ts`): it fetches
**100 rows at a time** from the server and paginates the loaded rows **client-side**
(10 per page). Advancing past the loaded rows automatically fetches the next batch of 100.

## Run

```bash
npm install
npm start            # ng serve -> http://localhost:4200
```

The app calls **Master-Data-Service** at the URL in `src/environments/environment.ts`
(default `http://localhost:8001/api/v1`). Start that service first:

```bash
cd ../../Middleware/Master-Data-Service
uvicorn main:app --reload --port 8001
```

Master-Data-Service enables CORS for `http://localhost:4200` by default
(override via its `CORS_ALLOW_ORIGINS` env var).

## Structure

```
src/app/
├── app.component.ts            top menu shell + router-outlet
├── app.routes.ts              Dashboard / Entitlements / Projects (+ children)
├── core/
│   ├── models/                API DTO interfaces
│   ├── services/              MasterDataService (HTTP)
│   └── utils/                 BatchPaginator
└── features/
    ├── dashboard/
    ├── entitlements/  (layout + users)
    └── projects/      (layout + list, dependencies, tech-stack)
```

## Build

```bash
npm run build        # ng build -> dist/sdlc-admin
```
