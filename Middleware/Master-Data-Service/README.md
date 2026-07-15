# Master-Data-Service

FastAPI service — **admin write plane**.

Owns the SDLC master data: **business applications** (projects), **sprints**, and
their **agendas**. Consumed by the `sdlc-admin` portal.

Follows the standard layered layout (`api` → `facades`/`tasks` → service → `dao`,
with interfaces in `common/`). See [`../README.md`](../README.md).
