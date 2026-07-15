# Workspace-Service

FastAPI service — **customer read / workspace plane**.

Lets customers (Developers, Product Owners, Product Managers, Project Managers) browse
the defined **business applications**, **sprints**, **agendas**, and the **documents**
(with ingestion status) available in their workspace. Consumed by the `sdlc-nexus` portal.

Follows the standard layered layout (`api` → `facades`/`tasks` → service → `dao`,
with interfaces in `common/`). See [`../README.md`](../README.md).
