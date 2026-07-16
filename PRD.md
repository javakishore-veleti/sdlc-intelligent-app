# Product Requirements Document — SDLC Intelligent App

| Field | Value |
|---|---|
| **Product name** | SDLC Intelligent App |
| **Document type** | Product Requirements Document (PRD) |
| **Version** | 0.1 (Draft) |
| **Status** | Draft — for review |
| **Last updated** | 2026-07-15 |
| **Owners** | Product / Architecture |

> **Note on scope of this document.** This PRD specifies *what* the product must do
> and *how it is structured* at an architectural level. It intentionally does **not**
> contain implementation code. All sample data, domain examples, customers, prices,
> and business rules referenced in this document are **synthetic and illustrative**.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals and Non-Goals](#3-goals-and-non-goals)
4. [Personas and Users](#4-personas-and-users)
5. [Key Concepts and Glossary](#5-key-concepts-and-glossary)
6. [Reference Sample Domain](#6-reference-sample-domain-digital-sales-services)
7. [Product Scope](#7-product-scope)
8. [Functional Requirements](#8-functional-requirements)
9. [System Architecture](#9-system-architecture)
10. [Repository Structure](#10-repository-structure)
11. [Data Model](#11-data-model)
12. [API Surface](#12-api-surface)
13. [RAG and Ingestion Design](#13-rag-and-ingestion-design)
14. [Non-Functional Requirements](#14-non-functional-requirements)
15. [Assumptions and Constraints](#15-assumptions-and-constraints)
16. [Phased Delivery Roadmap](#16-phased-delivery-roadmap)
17. [Success Metrics and Acceptance Criteria](#17-success-metrics-and-acceptance-criteria)
18. [Risks and Mitigations](#18-risks-and-mitigations)
19. [Open Decisions Log](#19-open-decisions-log)
20. [Future Enhancements](#20-future-enhancements)
21. [Appendix A: Sample Questions](#appendix-a-sample-questions-the-assistant-should-answer)

---

## 1. Executive Summary

**SDLC Intelligent App** is an internal knowledge platform that turns a software
development team's evolving sprint documentation into an instantly queryable,
citation-backed knowledge base.

Software teams produce a continuous stream of requirement and feature documents —
sprint after sprint, across many microservice applications. That knowledge is
scattered across PDFs, wikis, and inboxes, and becomes progressively harder to
search, trace, and reason about as the number of sprints grows. New team members
cannot answer "when did we add X?" or "what is the current rule for Y?" without
manually digging through a stack of historical documents.

SDLC Intelligent App solves this with two coordinated capabilities:

1. **Structured SDLC master data management** — administrators register the
   business applications (microservices) under development and define the sprints
   (with agendas) for each, giving every uploaded document a precise home in the
   organization's SDLC hierarchy.
2. **Retrieval-Augmented Generation (RAG) assistant** — customers (developers,
   product owners, product managers, project managers) upload their sprint feature
   documents and then ask natural-language questions across the entire accumulated
   history, receiving answers with **explicit citations** back to the source
   document, application, sprint, and page.

The platform is delivered as two Angular portals over a set of FastAPI middleware
services, with Apache Airflow orchestrating document ingestion into a ChromaDB
vector store, and a LangChain-based question-answering pipeline over a Large
Language Model (LLM).

---

## 2. Problem Statement

As software organizations scale their delivery across many microservices and
biweekly sprints, the documentation describing *what was built, why, and under
which rules* accumulates faster than any individual can track. Concretely:

- **Knowledge is siloed and temporal.** A feature specified in an early sprint is
  frequently amended in a later one. Readers cannot easily tell which version is
  current, or how a rule evolved.
- **Retrieval is manual and slow.** Answering a factual question ("which sprint
  introduced prepaid variants?", "what is the current discount-stacking rule?")
  requires opening and skimming many documents.
- **Onboarding is expensive.** New developers, product owners, and managers spend
  significant time reconstructing context that already exists in documents.
- **Trust requires traceability.** Any automated answer that cannot cite its source
  is not trustworthy enough for engineering or product decisions.

The platform must make this body of knowledge **searchable, current-aware, and
traceable**, while fitting the natural SDLC structure of *application → sprint →
feature*.

---

## 3. Goals and Non-Goals

### 3.1 Goals

- **G1** — Provide a single place to register business applications (microservices)
  and define their sprints with agendas.
- **G2** — Allow customers to upload sprint feature documents (PDF) and have them
  ingested, chunked, embedded, and indexed automatically.
- **G3** — Provide a natural-language assistant that answers questions across all
  ingested sprint documentation.
- **G4** — Return **citation-backed** answers (source document, application, sprint,
  page) so answers are verifiable.
- **G5** — Support **metadata-scoped** retrieval (filter by application and/or sprint
  range) and **temporal awareness** (surface how a feature evolved across sprints).
- **G6** — Keep the ingestion source **pluggable**, so a future automated source
  (e.g., an issue tracker) can replace manual entry without changing the RAG core.

### 3.2 Non-Goals (for the initial release)

- **NG1** — This is **not** a general document-management system; it is scoped to
  SDLC sprint/feature knowledge.
- **NG2** — No automated integration with external issue trackers in the initial
  release (designed for, but deferred — see [§20](#20-future-enhancements)).
- **NG3** — No enterprise identity/SSO, fine-grained RBAC, or multi-tenant isolation
  in the initial release (single trusted organization assumed).
- **NG4** — The assistant does **not** execute transactional business logic (e.g.,
  compute a real customer's final price). It answers questions *about* documented
  features and rules. (A tool-augmented "agentic" extension is a future enhancement.)

---

## 4. Personas and Users

The platform serves two portals and two broad persona groups.

### 4.1 Administrator (sdlc-admin portal)

Responsible for **master data**: registering business applications (microservices)
and defining their sprints and agendas. Administrators set up the SDLC scaffolding
that all uploaded documents attach to.

### 4.2 Customer (sdlc-nexus portal)

> **Definition — "Customer".** In this product, a **Customer** is any internal
> platform user in one of the following roles:
> **Developer, Product Owner, Product Manager, Project Manager.**
> These users consume the platform: they upload sprint feature documents and query
> the assistant. This is distinct from the *"Customer Profile"* entity that appears
> inside the **sample Digital Sales domain data** (see [§6](#6-reference-sample-domain-digital-sales-services)),
> which represents an end-buyer in that illustrative dataset. The two meanings are
> unrelated; where ambiguity is possible this document uses **"platform Customer"**
> vs. **"domain Customer Profile."**

| Customer role | Primary interest |
|---|---|
| Developer | Implementation-level details, business rules, acceptance criteria, cross-service dependencies |
| Product Owner | Feature intent, scope of a sprint, backlog rationale |
| Product Manager | Roadmap and evolution of capabilities across sprints |
| Project Manager | What was delivered in which sprint, agenda vs. outcome |

All Customer roles share the same core capabilities in the initial release (upload,
browse, ask). Role-specific views and permissions are a future enhancement.

---

## 5. Key Concepts and Glossary

| Term | Definition |
|---|---|
| **Business Application** | A microservice application under development (e.g., Product Catalog, Pricing). Also referred to as a **Project** in the admin context. |
| **Project** | The administrative record representing one Business Application in the master data. One project per microservice. |
| **Sprint** | A time-boxed delivery iteration (assumed biweekly) belonging to a Business Application, with a defined **agenda**. |
| **Agenda** | The stated goals/theme of a sprint (what the sprint intends to deliver). |
| **Feature / Requirement Document** | A PDF describing one or more features/requirements delivered (or planned) in a sprint. The primary ingestion input. |
| **Ingestion** | The pipeline that parses a document, splits it into chunks, embeds them, and indexes them (with metadata) into the vector store. |
| **Chunk** | A bounded segment of document text (target ~2000 tokens) that is embedded and retrieved as a unit. |
| **Embedding** | A vector representation of a chunk used for semantic similarity search. |
| **Vector Store** | ChromaDB collection holding chunk embeddings and their metadata. |
| **RAG** | Retrieval-Augmented Generation — retrieve relevant chunks, then have the LLM answer grounded in them. |
| **Citation** | The provenance attached to an answer: source document, application, sprint, and page. |
| **Sprint Source** | The abstraction describing where sprint/feature data originates. The initial release implements the **Manual** source (portal entry + upload); future sources plug into the same interface. |

---

## 6. Reference Sample Domain: Digital Sales Services

To demonstrate the platform end-to-end, the initial release ships a **synthetic
reference corpus** modeled on a **Digital Sales Services** subscription-commerce
domain — i.e., selling digital products as subscriptions. This domain is used only
to produce realistic sample sprint documents; the platform itself is
**domain-agnostic** and works with any team's SDLC documentation.

> All entities, values, prices, customers, and rules in the sample corpus are
> **fictional and illustrative**. No real, proprietary, or confidential material is
> included.

### 6.1 Sample microservices (Business Applications)

| Microservice | Responsibility (sample) |
|---|---|
| **Product Catalog** | Master list of digital products available for sale |
| **Customer & Vehicle Onboarding** | Onboarding of profiles and assets; assigns trial offers |
| **Offer Management** | Offers (each mapped to a product) and their variants |
| **Pricing** | Country-specific price per offer variant |
| **Discounts** | Loyalty, affinity, and active-promotion discounts (stackable) |
| **Tax** | Country-specific tax applied to a priced offer |
| **Offer Qualification / Eligibility** | Determines which offers a profile/asset can purchase |

### 6.2 Sample entity backbone

```
Product ──< Offer ──< Offer Variant ──< Pricing (per country)
                                   └──< Discounts (loyalty | affinity | promotion; stackable)
                                   └──< Tax (per country)

Customer Profile (id = first name + last name + email; type ∈ {Personal, Business, Fleet, Other})
        └──< Asset/Vehicle (1..N; some owned by a Business/Fleet)

Onboarding ── assigns ──> Trial Offer
Eligibility ── determines ──> Purchasable Offers
```

This backbone is deliberately rich enough that sample sprint documents can describe
features that **evolve across sprints** (e.g., a discount-stacking rule that changes
between an early and a later sprint), exercising the platform's temporal-awareness
and citation features.

---

## 7. Product Scope

### 7.1 In scope (initial release)

- Admin portal: Business Application (Project) management and Sprint management (with agenda).
- Customer portal: sprint document (PDF) upload, browse defined applications/sprints, and the chatbot assistant.
- Manual Sprint Source (portal-driven creation and upload).
- Airflow-orchestrated ingestion into ChromaDB with metadata tagging.
- LangChain-based RAG Q&A over ChromaDB with citations and metadata-scoped filtering.
- Synthetic Digital Sales Services reference corpus for demonstration.

### 7.2 Out of scope (initial release)

- Automated issue-tracker ingestion source.
- SSO / enterprise auth / fine-grained RBAC / multi-tenancy.
- Tool-augmented "agentic" actions (e.g., live price computation).
- Real-time collaborative editing of documents.

---

## 8. Functional Requirements

Requirements are grouped by capability. Each has an ID and acceptance criteria (AC).

### 8.1 Business Application (Project) Management — Admin

- **FR-1** The system shall let an administrator create, view, update, and archive a
  Business Application (Project), capturing at minimum: name, description, and owning
  team.
  - *AC:* A created application appears in the customer portal's browsable list.
- **FR-2** The system shall enforce unique application names within the organization.

### 8.2 Sprint Management — Admin

- **FR-3** The system shall let an administrator define a Sprint under a Business
  Application, capturing: sprint number/name, start date, end date, and **agenda**.
  - *AC:* Sprint dates are validated (end ≥ start); sprint number is unique within its application.
- **FR-4** The system shall let an administrator edit or archive a Sprint.
- **FR-5** Sprints shall be listable and filterable by application and by date range.

### 8.3 Document Upload — Customer

- **FR-6** The system shall let a Customer upload one or more **PDF** feature/requirement
  documents and associate each upload with an existing Business Application and Sprint.
- **FR-7** On upload, the system shall capture document metadata: application, sprint,
  upload date, uploader role, and original filename.
  - *AC:* Metadata is persisted and later surfaced in citations.
- **FR-8** The system shall accept a metadata-assist flow in which suggested
  application/sprint values may be pre-filled and confirmed by the uploader before
  ingestion. *(See Open Decision OD-1.)*
- **FR-9** The system shall reject non-PDF files and files exceeding a configured size
  limit, with a clear error.

### 8.4 Ingestion — System (Airflow)

- **FR-10** Upon a confirmed upload, the Ingest service shall trigger an Airflow
  ingestion run for the document.
- **FR-11** The ingestion pipeline shall: parse the PDF per page, split text into
  chunks (target ~2000 tokens), generate embeddings, and index chunks into ChromaDB
  with full metadata (application, sprint, sprint dates, page number, document id).
  - *AC:* Every indexed chunk is traceable to application + sprint + page + document.
- **FR-12** The ingestion pipeline shall be **idempotent** for re-uploads of the same
  document version (no duplicate chunks).
- **FR-13** Ingestion status (queued, running, succeeded, failed) shall be observable
  and surfaced back to the Customer.

### 8.5 Assistant / Q&A — Customer

- **FR-14** The system shall provide a chat interface where a Customer can ask a
  natural-language question and receive a grounded answer.
- **FR-15** Every answer shall include **citations** listing the source document(s),
  application, sprint, and page(s) used.
  - *AC:* Removing all retrieved context yields an explicit "not found in the
    documentation" style answer rather than a fabricated one.
- **FR-16** The system shall support **metadata-scoped** questions — the Customer may
  restrict a question to a specific application and/or a sprint range.
- **FR-17** The system shall be **temporally aware**: when retrieved context contains
  conflicting versions of a rule/feature across sprints, the answer shall present the
  evolution (earlier vs. later) and identify the most recent version. *(See OD-2.)*
- **FR-18** The system shall maintain conversational memory within a session to support
  multi-turn follow-up questions.

### 8.6 Browse — Customer

- **FR-19** The system shall let a Customer browse the catalog of Business Applications
  and the sprints (with agendas) defined for each.
- **FR-20** The system shall let a Customer see which documents are ingested for a given
  application/sprint and their ingestion status.

---

## 9. System Architecture

### 9.1 Component overview

```
┌───────────────────────────── PORTALS (Angular) ─────────────────────────────┐
│                                                                              │
│   sdlc-admin portal                     sdlc-nexus portal                     │
│   • Business Application mgmt            • Upload sprint PDFs                  │
│   • Sprint mgmt (agenda)                • Chatbot assistant (Q&A + citations) │
│                                          • Browse applications / sprints      │
└───────────────┬──────────────────────────────────┬──────────────────────────┘
                │ REST/JSON                          │ REST/JSON
        ┌───────▼──────────────────── MIDDLEWARE (FastAPI) ───────────▼────────┐
        │                                                                      │
        │  Master-Data-    Workspace-      Ingest-Extract-   Knowledge-        │
        │  Service         Service         Service           Service           │
        │  (admin writes)  (customer reads) (upload →         (LangChain        │
        │  apps, sprints,  fetch apps &     extract →         retrieval +       │
        │  agendas         sprints          Airflow)          LLM)              │
        └───────┬───────────────────┬──────────────────┬───────────────┬───────┘
                │                   │                  │               │
          ┌─────▼─────┐       ┌─────▼─────┐      ┌─────▼───────┐  ┌────▼───────┐
          │ Postgres  │◄──────┤ Postgres  │      │  Apache     │  │  ChromaDB  │
          │ (master   │       │ (read)    │      │  Airflow    │──►│ (vectors + │
          │  data)    │       │           │      │  (ingest    │  │  metadata) │
          └───────────┘       └───────────┘      │  DAG)       │  └────▲───────┘
                                                 └─────────────┘       │
                                                        ┌──────────────┴─────────┐
                                                        │  LLM (Ollama local /    │
                                                        │  hosted API — config)   │
                                                        └─────────────────────────┘
```

### 9.2 Runtime flows

**Admin — define master data**
```
sdlc-admin portal → Master-Data-Service → Postgres
  (create Business Application; define Sprint + agenda)
```

**Customer — upload & ingest**
```
sdlc-nexus portal → Ingest-Extract-Service → trigger Airflow DAG
  → parse PDF → chunk (~2000 tokens) → embed → ChromaDB (+ metadata)
  → update ingestion status (Postgres)
```

**Customer — ask (Q&A)**
```
sdlc-nexus portal → Knowledge-Service → LangChain retriever
  → ChromaDB (metadata-filtered similarity search) → LLM
  → grounded answer + citations → portal
```

**Customer — browse**
```
sdlc-nexus portal → Workspace-Service → Postgres (read)
  (list applications, sprints, agendas, ingested documents & status)
```

### 9.3 Architectural principles

- **Separation of write and read planes.** `Master-Data-Service` is the administrative
  command/write plane; `Workspace-Service` is the customer query/read plane. This keeps
  admin operations and customer consumption independently evolvable.
- **Layered services.** Each `*-Service` follows a consistent layout —
  `api → facades (+ tasks) → services → dao` — with all cross-layer contracts declared
  as interfaces under `common/` (`service`, `facade`, `dao`), plus `common/constants`
  and `utils`.
- **Pluggable Sprint Source.** Ingestion depends on a `SprintSource` interface. The
  initial release ships a `ManualSource`; alternative sources implement the same
  interface without touching ingestion or RAG logic.
- **Orchestrated ingestion.** Airflow provides observable, retriable, idempotent
  ingestion runs — appropriate for a growing biweekly document stream.
- **Provenance-first RAG.** Metadata (application, sprint, page, document) travels
  with every chunk so that every answer can cite its sources.

### 9.4 Technology stack

| Layer | Technology |
|---|---|
| Front-end portals | Angular (2 SPAs) |
| API / middleware | Python, FastAPI |
| Orchestration / ingestion | Apache Airflow |
| Vector store | ChromaDB |
| Master data store | PostgreSQL |
| RAG framework | LangChain |
| Embeddings | Sentence-transformer embeddings (configurable) |
| LLM | Configurable: local (Ollama) or hosted API |
| Packaging / runtime | Docker / container engine, orchestrated via Compose |

---

## 10. Repository Structure

```
sdlc-intelligent-app/
├── PRD.md                              # this document
├── README.md                           # project overview
├── Portals/                            # Angular front-ends
│   ├── sdlc-admin/                     #   admin portal (apps, sprints, agendas)
│   └── sdlc-nexus/                     #   customer hub (upload, browse, chatbot)
├── Middleware/                         # FastAPI microservices (layered — see below)
│   ├── Master-Data-Service/            #   admin writes (apps, sprints, agendas)
│   ├── Workspace-Service/              #   customer reads (apps, sprints, documents)
│   ├── Ingest-Extract-Service/         #   receive PDF, extract, trigger Airflow
│   ├── Knowledge-Service/              #   LangChain retrieval + LLM over ChromaDB
│   └── SDLC-Workflows/                 #   Airflow DAGs (ingestion into ChromaDB)
├── cicd/
│   └── Local/                          # docker-all-up / -down / -status scripts
├── corpus/                             # synthetic Digital Sales sample sprint documents
├── infra/                              # docker-compose stack (Postgres, Chroma, Airflow, …)
└── docs/                               # architecture, design, and presentation material
```

**Standard layout inside every `*-Service`:**

```
<Service>/
├── api/                  # FastAPI routers / endpoints
├── facades/              # facade impls; each facade = subpackage with a tasks/ module
├── services/             # service-layer implementations
├── dao/                  # DAO implementations
├── common/
│   ├── service/interfaces/   # service-layer contracts
│   ├── facade/interfaces/    # facade-layer contracts
│   ├── dao/interfaces/       # DAO-layer contracts
│   └── constants/            # shared constants
└── utils/                # cross-cutting utilities
```

> The `Middleware/`, `Portals/`, and service names
> (`Master-Data-Service`, `Workspace-Service`, `Ingest-Extract-Service`,
> `Knowledge-Service`) and portal names (`sdlc-admin`, `sdlc-nexus`) are normative and
> reflected in [§9](#9-system-architecture).

---

## 11. Data Model

### 11.1 Master data (PostgreSQL — logical)

**BusinessApplication (Project)**

| Field | Type | Notes |
|---|---|---|
| id | UUID | PK |
| name | string | unique |
| description | text | |
| owning_team | string | |
| status | enum | active / archived |
| created_at, updated_at | timestamp | |

**Sprint**

| Field | Type | Notes |
|---|---|---|
| id | UUID | PK |
| application_id | UUID | FK → BusinessApplication |
| sprint_number | string | unique within application |
| agenda | text | sprint goals/theme |
| start_date, end_date | date | end ≥ start |
| status | enum | planned / active / closed / archived |
| created_at, updated_at | timestamp | |

**Document**

| Field | Type | Notes |
|---|---|---|
| id | UUID | PK |
| application_id | UUID | FK → BusinessApplication |
| sprint_id | UUID | FK → Sprint |
| original_filename | string | |
| uploaded_by_role | enum | Developer / ProductOwner / ProductManager / ProjectManager |
| upload_date | timestamp | |
| ingestion_status | enum | queued / running / succeeded / failed |
| version | string/int | supports re-uploads / idempotency |

### 11.2 Vector store (ChromaDB — per chunk)

| Field | Notes |
|---|---|
| embedding | vector for the chunk |
| text | chunk text |
| document_id | FK → Document |
| application_id / application_name | for metadata filtering & citation |
| sprint_id / sprint_number | for metadata filtering & citation |
| sprint_start_date / sprint_end_date | supports temporal ordering |
| page_number | for citation |
| chunk_index | ordering within document |

### 11.3 Sample domain data (synthetic; for the reference corpus only)

The Digital Sales entities in [§6](#6-reference-sample-domain-digital-sales-services)
(Product, Offer, Offer Variant, Pricing, Discounts, Tax, Customer Profile, Asset/Vehicle,
Onboarding, Eligibility) exist **only as content inside the synthetic sprint documents**.
They are not first-class tables in the platform; the platform indexes the *documents that
describe them*.

---

## 12. API Surface

High-level, representative endpoints (final contracts defined during design of each service).

### 12.1 Master-Data-Service (admin writes)

| Method | Path | Purpose |
|---|---|---|
| POST | `/applications` | Create a Business Application |
| GET | `/applications` | List applications |
| PUT | `/applications/{id}` | Update / archive an application |
| POST | `/applications/{id}/sprints` | Define a sprint (with agenda) |
| PUT | `/sprints/{id}` | Update / archive a sprint |

### 12.2 Workspace-Service (customer reads)

| Method | Path | Purpose |
|---|---|---|
| GET | `/applications` | List applications available to customers |
| GET | `/applications/{id}/sprints` | List sprints + agendas for an application |
| GET | `/sprints/{id}/documents` | List documents + ingestion status for a sprint |

### 12.3 Ingest-Extract-Service

| Method | Path | Purpose |
|---|---|---|
| POST | `/uploads` | Upload a PDF (multipart) with application_id + sprint_id |
| POST | `/uploads/{id}/confirm` | Confirm suggested metadata and start ingestion |
| GET | `/uploads/{id}/status` | Poll ingestion status |

### 12.4 Knowledge-Service

| Method | Path | Purpose |
|---|---|---|
| POST | `/ask` | Ask a question; body may include filters (application_id, sprint range) and session id |
| GET | `/sessions/{id}` | Retrieve conversation history for a session |

---

## 13. RAG and Ingestion Design

### 13.1 Ingestion pipeline (Airflow DAG)

1. **Extract** — parse the PDF, preserving page boundaries.
2. **Chunk** — split into ~2000-token chunks with overlap to preserve context.
3. **Embed** — generate embeddings for each chunk.
4. **Index** — upsert chunks into ChromaDB with full metadata (§11.2).
5. **Finalize** — update `Document.ingestion_status`; emit metrics.

Idempotency: re-ingesting the same document version replaces its existing chunks
rather than appending duplicates (keyed by `document_id` + `version`).

### 13.2 Retrieval and answering (Knowledge-Service)

1. **Filter** — apply metadata filters from the request (application, sprint range).
2. **Retrieve** — semantic similarity search over ChromaDB for top-k relevant chunks.
3. **Assemble** — construct a grounded prompt containing retrieved chunks and their
   provenance.
4. **Generate** — the LLM answers strictly from provided context; if context is
   insufficient, it says so rather than fabricating (FR-15).
5. **Cite** — attach citations (document, application, sprint, page) to the answer.
6. **Remember** — persist the turn to session memory for multi-turn dialogue.

### 13.3 Temporal awareness

When retrieved chunks describing the same rule/feature come from different sprints
with conflicting content, the pipeline orders them by sprint date and instructs the
LLM to present the evolution and highlight the most recent version (FR-17). The exact
default behavior is tracked as **OD-2**.

### 13.4 Citation format (illustrative)

> "Discounts may stack as of **Pricing / Sprint 9** (2026-04). This changed an earlier
> rule from **Pricing / Sprint 3** (2026-01) that disallowed stacking."
> **Sources:** Pricing — Sprint 9, p.2; Pricing — Sprint 3, p.4.

---

## 14. Non-Functional Requirements

- **NFR-1 Security & privacy.** Only synthetic sample data is included in the repository.
  Uploaded documents are treated as internal; the design must not transmit document
  content to third parties beyond the explicitly configured LLM provider. A fully-local
  LLM (Ollama) configuration must be supported for a no-external-egress deployment.
- **NFR-2 Traceability.** 100% of assistant answers that make factual claims must carry
  citations.
- **NFR-3 Observability.** Ingestion runs and their status must be observable (Airflow
  UI + status surfaced to customers).
- **NFR-4 Idempotency & reliability.** Ingestion must be safely retriable without
  producing duplicate chunks.
- **NFR-5 Configurability.** LLM provider, embedding model, chunk size, and top-k are
  configuration, not code changes.
- **NFR-6 Portability.** The full stack runs locally via containers with a single
  bring-up command.
- **NFR-7 Performance (target).** Typical Q&A round-trip returns within a few seconds on
  the reference hardware profile (subject to LLM choice).
- **NFR-8 Maintainability.** Clear separation between portals, middleware services,
  ingestion, and stores; the Sprint Source abstraction isolates ingestion origin.

---

## 15. Assumptions and Constraints

- **A1** Sprints are assumed biweekly, but the model does not hard-code cadence.
- **A2** The initial release assumes a single trusted organization (no multi-tenant
  isolation).
- **A3** Documents are provided as PDF in the initial release.
- **A4** A single administrator group manages master data; all customer roles share
  capabilities initially.
- **A5** The reference domain corpus is entirely synthetic and illustrative.

---

## 16. Phased Delivery Roadmap

The architecture is specified in full above; delivery is incremental. Each phase is
independently demonstrable.

| Phase | Theme | Delivers |
|---|---|---|
| **Phase 0** | Foundations | Repo scaffolding, container bring-up (Postgres, ChromaDB, Airflow, LLM), health checks |
| **Phase 1** | Vertical slice | One Business Application + one Sprint (admin) → upload one PDF (customer) → Airflow ingest → ask one question with citation, end-to-end |
| **Phase 2** | Breadth | Full Business Application & Sprint management; browse; multiple documents; metadata-scoped retrieval |
| **Phase 3** | Intelligence | Temporal awareness, multi-turn memory, ingestion status UX, synthetic corpus with evolving rules |
| **Phase 4** | Polish | Observability, error handling, packaging, demo script, presentation |

> **Recommendation.** Build and demo **Phase 1 (thin vertical slice)** before widening.
> It proves every layer of the architecture cooperates and de-risks the rest.

---

## 17. Success Metrics and Acceptance Criteria

- **M1** A customer can go from uploading a sprint PDF to receiving a cited answer
  about its contents without manual back-end steps.
- **M2** ≥ 90% of factual test questions over the reference corpus are answered
  correctly with valid citations.
- **M3** Questions with no supporting document produce an explicit "not documented"
  answer (no fabrication) in 100% of tested cases.
- **M4** A question scoped to an application/sprint returns only in-scope sources.
- **M5** For a rule that changes across sprints, the assistant identifies the current
  version and references the prior one.

---

## 18. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Hallucinated answers | Loss of trust | Strict grounded-prompting; "not documented" fallback; mandatory citations (FR-15) |
| Version confusion across sprints | Wrong answers | Temporal ordering by sprint date; evolution-aware answering (FR-17) |
| Poor PDF parsing (scans, tables) | Missing content | Per-page parsing; note parsing limits; future OCR |
| Scope creep | Never ships | Phased roadmap; vertical slice first (§16) |
| Airflow operational weight | Setup friction | Containerized; Airflow used for orchestration/observability value; simple synchronous fallback documented |
| LLM cost/egress (hosted) | Privacy / cost | Local (Ollama) configuration supported (NFR-1, NFR-5) |

---

## 19. Open Decisions Log

| ID | Decision | Options | Recommendation | Status |
|---|---|---|---|---|
| **OD-1** | Sprint metadata capture on upload | (a) manual form; (b) auto-extract from PDF; (c) auto-extract + confirm | **(c)** hybrid | Open |
| **OD-2** | Default temporal behavior | (a) latest-only; (b) show evolution; (c) neutral | **(b)** show evolution | Open |
| **OD-3** | Default LLM provider | (a) local Ollama; (b) hosted API | Config switch; default **local** for privacy | Open |
| **OD-4** | Embedding model | sentence-transformer variants | Pick during Phase 0 benchmarking | Open |
| **OD-5** | Front-end scope of first slice | full Angular vs. minimal first | Minimal admin+ask UI in Phase 1, full Angular thereafter | Open |

---

## 20. Future Enhancements

- **Automated Sprint Source** — an issue-tracker/backlog adapter implementing the
  `SprintSource` interface to replace manual entry (design already accommodates this).
- **Agentic assistant** — tool-augmented capabilities (e.g., compute an illustrative
  price, check eligibility) that go beyond documentation Q&A.
- **Identity & RBAC** — SSO and role-specific permissions/views per customer role.
- **Multi-tenancy** — isolation across teams or organizations.
- **Additional input formats** — Word, Markdown, wiki, OCR for scanned PDFs.
- **Analytics** — most-asked topics, documentation gaps, coverage per application.

---

## Appendix A: Sample Questions the Assistant Should Answer

Over the synthetic Digital Sales reference corpus, the assistant should handle:

- "Which sprint introduced prepaid offer variants, and for which product?"
- "What is the current rule for stacking loyalty and promotional discounts?"
- "How did the discount-stacking rule change across sprints?"
- "What trial offers are assigned during onboarding for a Fleet profile?"
- "Which microservice owns country-specific tax calculation?"
- "List the offer variants available for the WiFi/hotspot product as of the latest sprint."
- "What eligibility rules determine which offers a Business profile can purchase?"
- (Scoped) "Within the Pricing application, what changed between Sprint 3 and Sprint 9?"

---

*End of document.*
