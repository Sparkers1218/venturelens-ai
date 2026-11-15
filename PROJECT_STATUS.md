# Project Status

## Milestones

| Milestone | Scope | Status |
|---|---|---|
| 1. Project Foundation | Entry point, dependencies, configuration, documentation, and basic tests | Complete |
| Project Charter | Initial project charter documentation | Complete |
| 2. Core domain | Define and validate the idea, evidence, assumptions, risks, and experiment concepts | MVP implemented |
| 3. Persistence | SQLAlchemy models, SQLite/PostgreSQL URL support, and repositories | MVP implemented; additive upgrades included, Alembic and ownership pending |
| 4. Authentication | OIDC integration and authenticated user context | Not started |
| 5. Research integration | Research provider selection, retrieval, and evidence attribution | Not started |
| 6. AI provider integration and evaluation | Provider evaluation, structured analysis, and clearly labelled fallbacks | Deterministic rule-based analysis engine implemented; no AI provider integration |
| 7. User workflows | Streamlit pages for idea intake, analysis, and saved reports | Local MVP implemented |
| 8. Hardening and release | End-to-end tests, deployment configuration, operations, and release readiness | Not started |

No AI provider has been selected. NVIDIA NIM remains a candidate pending
verification of free access, usage limits, payment requirements, licensing,
and deployment terms before adoption.

## Current implementation

- The Streamlit app supports project creation, editing, search, reopening, and
  deletion. Project fields include optional business model; competitor records
  include audience, pricing, differentiation notes, and reference URL.
- Navigation includes dashboard, My Projects, project creation, competitor
  insights, research, report review, derived notifications/activity, profile,
  settings, and project workspace. Profile and settings explicitly reflect the
  unauthenticated local-demo limitations.
- SQLite persistence is initialized automatically; PostgreSQL can be selected
  through `DATABASE_URL`.
- Versioned rule-based reports cover problem/solution, customer definition,
  competitor comparison, business-model considerations, strengths/weaknesses
  of the brief, risks, assumptions, research references, experiments, and next
  steps. JSON downloads and score/risk/priority charts are implemented.
- 0-3 report scores measure input coverage/detail under explicit rubrics only;
  they do not estimate viability or success.
- Pydantic validates field lengths and manual source URLs.
- Authentication, user ownership, live research, and AI-provider integration
  are not implemented. The app explicitly labels itself a single-user local
  demo.
- The app is for a controlled local, single-user demonstration only. Do not
  expose it as a public or shared multi-user service.
- A root `.venv` exists and is used for local Python development.
- All ten direct requirements are installed in `.venv`; `pip check` reports no
  broken requirements.
- The current automated suite passes; see the verification section below.
- Provider access, credentials, endpoints, and model availability remain
  unconfigured.

## Repository and environment status

- Git repository initialized.
- Intentional local branches: `main` and `feature/project-ui`.
- GitHub remote `origin` is configured.
- The initial project foundation is pushed to GitHub; `origin/main` points to
  the initial project foundation commit.
- The teammate invitation has been accepted, as previously confirmed. No claim
  is made here about a teammate pushing a feature branch.
- A project-root `.venv` is used for local Python development.

## Remaining foundation review tasks

- Review dependency update and compatibility policy before deployment.
- Confirm setup and test instructions in a clean checkout.
- Plan deployment and install production dependencies in the deployment
  environment separately from local development.

## Product and architecture work still outstanding

- Choose an OIDC provider and define its setup and callback configuration.
- Select the research/search provider and confirm its supported API and terms.
- Evaluate AI provider options, including NVIDIA NIM, and verify access,
  licensing, costs, and deployment terms before selection.
- Plan the production PostgreSQL schema and migrations, and implement ownership
  enforcement for every project data operation before any authenticated/shared
  deployment.
- Add clearly labelled fallback behavior and tests for unavailable providers.
- Plan deployment, operations, data retention, and privacy requirements.

## MVP limitations

- Database schema creation uses `create_all` with additive upgrades for current
  project fields; there are no Alembic migrations.
- The demo has no authentication or tenant isolation and is not suitable for
  multi-user, public, or network-shared deployment. Use only in a controlled
  local single-user demonstration.
- Research is manual entry only; references are not fetched or verified.
- Analysis is deterministic and rule-based, not an AI model or market
  validation.
- PostgreSQL support is configuration-level and has not been integration
  tested against a PostgreSQL server.

## Verification

- `.venv\Scripts\python.exe -m pytest -q`: 9 passed.
- This is the existing recorded test baseline; tests were not rerun as part of
  the documentation correction.
- The Streamlit AppTest exercises project creation, competitor and source entry,
  report generation, JSON download availability, project/report reopening, and
  a fresh app run against the same SQLite file.
- A legacy-schema test verifies additive upgrades preserve existing records.
- SQLite persistence is tested after disposing and recreating the database engine.
- A local browser smoke test verified the dashboard, empty-state metrics, project
  form, project creation, and workspace rendering. Full responsive, theme-switch,
  and accessibility review was not performed.
- PostgreSQL integration and multi-user access have not been tested.
