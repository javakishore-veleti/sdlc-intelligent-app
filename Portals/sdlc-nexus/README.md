# sdlc-nexus

Angular portal for **customers** — the central hub of the platform.

> **Nexus** — a central connection or focal point where multiple things join together.
> `sdlc-nexus` is where Developers, Product Owners, Product Managers, and Project
> Managers converge to work with the team's sprint knowledge.

Capabilities:

- **Upload** sprint feature/requirement documents (PDF) against an application and sprint.
- **Browse** the defined business applications, sprints, and agendas.
- **Ask** the RAG assistant natural-language questions across all sprints, with
  citation-backed answers.

Backed by `Middleware/DevLifeCycleAPI` (browse), `Middleware/Ingest-API` (upload),
and `Middleware/QnA-API` (assistant). See [`../../PRD.md`](../../PRD.md).
