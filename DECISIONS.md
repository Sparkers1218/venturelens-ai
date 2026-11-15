# VentureLens AI — Decisions and Direction

This document distinguishes current implementation from agreed principles,
proposed technical directions, and unresolved choices. A dependency in
`requirements.txt` or a directory in the project tree is not evidence that its
related feature is implemented or selected.

The status labels used below are **Accepted**, **Proposed**, **Open**, and
**Superseded**.

## Confirmed implementation

These are observations about the current project, not decisions about the
eventual product architecture.

| Area | Verified implementation |
|---|---|
| Language and UI | Python and Streamlit app in `app.py`; supports project management, manual competitor/source records, saved reports, and JSON downloads. |
| Configuration and persistence | `config/settings.py` uses Pydantic Settings; SQLite is the local default, with PostgreSQL URLs configurable. SQLAlchemy models and repositories persist projects, competitors, source notes, and reports. |
| Analysis | Deterministic rule-based reports are labeled as non-AI and avoid claiming external research or validation. |
| Tests | pytest covers settings, validation, persistence, scoped child-record deletion, cascading deletion, and a Streamlit AppTest workflow. |
| Dependencies | `requirements.txt` declares Streamlit, Pydantic, HTTPX, database, migration, authentication, and test packages. Declaring a package does not mean the corresponding feature is wired in. |
| Authentication and external integrations | No authentication provider, live research provider, or AI provider is wired into the application. |

## Accepted principles

The following are accepted product and engineering principles. They do not
mean that the corresponding architecture or behavior is fully implemented.

| Area | Accepted principle | Implementation status |
|---|---|---|
| Evidence and analysis | Keep external evidence, user-provided information, assumptions, AI interpretations, and recommendations distinguishable. Do not present AI output as verified fact or a guarantee of business success. | User-input, assumption, source-note, and rule-based recommendation labels are implemented; no AI or external evidence provider is configured. |
| Provider boundaries | Keep AI and external research behind separate provider adapters so either provider can be changed. | Adapters not implemented. |
| User data ownership | Enforce user ownership in every project data operation for authenticated/shared use. | SQLAlchemy persistence is implemented for the local demo; authentication and per-user ownership enforcement are not implemented. |
| Provider failures | Communicate provider unavailability clearly; any fallback must be labeled and must not imply that unavailable research or AI work occurred. | Provider handling and fallbacks not implemented. |
| Cost | No mandatory paid software, APIs, subscriptions, or services. Prefer free and open-source tools. | Policy; provider and infrastructure choices remain open. |
| Cost verification | Before adopting a provider or service, verify its free-tier restrictions, licensing and terms, payment-method requirements, potential overage charges, and deployment terms. Record evidence of verification; do not assume a free tier exists. | No provider verification is claimed by this document. |

## Proposed technical directions

These directions preserve the intended architecture recorded in the Project
Charter. They are not claims of completed implementation or provider selection.

| Area | Status | Direction | Current implementation |
|---|---|---|---|
| Language and UI | **Proposed** | Python and Streamlit. | Implemented as a local MVP with dashboard, project forms, workspaces, reports, and charts. |
| Application shape | **Proposed** | Modular monolith, separating UI, domain/business logic, persistence, and integrations. | UI, core validation/analysis, SQLAlchemy persistence, and settings modules are implemented; provider adapters and migrations are not. |
| Authentication | **Proposed** | OIDC authentication. | Not implemented; provider and configuration are open. |
| Production database | **Proposed** | PostgreSQL. | SQLAlchemy supports PostgreSQL URLs; local default and verified tests use SQLite. |
| ORM and migrations | **Proposed** | SQLAlchemy ORM and Alembic migrations. | SQLAlchemy models/repositories are implemented; Alembic migrations are not. |
| Validation and HTTP | **Proposed** | Pydantic for validation and HTTPX for HTTP clients. | Pydantic validates domain inputs; no HTTP integration is implemented. |
| Tests | **Accepted** | pytest for automated tests. | pytest covers settings, domain validation, persistence, report integrity, and the Streamlit demo workflow. |
| Version control | **Accepted** | Git and GitHub as project version-control tools. | Git is in use and `origin` is configured; no project changes from this MVP task were committed or pushed. |

## Proposed provider option

### NVIDIA NIM — **Proposed, not selected**

NVIDIA NIM may be evaluated as an AI provider option. It is not a finalized or
accepted provider, and no integration, model, endpoint, or access has been
confirmed. Before any adoption, verify current free access and its usage limits,
payment-method requirements, licensing and usage terms, and deployment terms,
including any infrastructure or overage costs. Do not assume that development
access makes production deployment free.

## Open decisions

| Area | Open decision |
|---|---|
| Authentication | Select an OIDC provider; confirm account, client-registration, and callback requirements and verify cost and terms. |
| AI | Select an AI provider and model, if any. NVIDIA NIM remains only a proposed option. Verify access, limits, payment requirements, licensing, and deployment costs before selection. |
| External research | Select a research/search provider and confirm its API, source attribution requirements, terms, limits, payment requirements, and possible overage charges. |
| Hosting | Select a hosting/deployment provider, if needed, after verifying free-tier restrictions, payment requirements, overages, and deployment terms. |
| PostgreSQL environment | Decide how PostgreSQL will be provided for development and production, including associated costs. |
| Domain and data lifecycle | Define the domain schema, report retention, data deletion, and privacy requirements. |
| Fallback behavior | Define user-visible behavior when an AI or research provider is unavailable. |
| Operations | Decide observability and operational requirements. |

Do not treat any provider, endpoint, credential, model availability, or free
tier as configured or verified until the relevant decision is recorded with
current supporting information.

## Local and deployment environments

**Accepted practice:** Use a project-root `.venv` for isolated local Python
development and do not commit it. The existing project documentation describes
installing production dependencies separately in the deployment environment
rather than copying the local `.venv`. The deployment process and hosting
provider remain **Open**.

## Superseded decision record

| Previous wording or implication | Status | Current interpretation |
|---|---|---|
| NVIDIA NIM listed as an agreed/finalized AI integration. | **Superseded** | NVIDIA NIM is a proposed option only; the AI provider is **Open** pending verification and selection. |
| The previous “Agreed” table could be read as saying every listed technology was both finalized and implemented. | **Superseded** | Technical directions are classified above; implementation status is stated separately. |

The Project Charter's milestone label “NVIDIA NIM integration” should be read
as a candidate integration to evaluate, not as provider selection. Its open
decisions and provider-selection requirements remain applicable.
