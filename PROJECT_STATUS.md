# Project Status

## Milestones

| Milestone | Scope | Status |
|---|---|---|
| 1. Project Foundation | Entry point, dependencies, configuration, documentation, and basic tests | Complete |
| 2. Core domain | Define and validate the idea, evidence, assumptions, risks, and experiment concepts | Not started |
| 3. Persistence | PostgreSQL data model, migrations, repositories, and per-user ownership enforcement | Not started |
| 4. Authentication | OIDC integration and authenticated user context | Not started |
| 5. Research integration | Research provider selection, retrieval, and evidence attribution | Not started |
| 6. AI analysis | NVIDIA NIM integration, structured analysis, and clearly labelled fallbacks | Not started |
| 7. User workflows | Streamlit pages for idea intake, analysis, and saved reports | Not started |
| 8. Hardening and release | End-to-end tests, deployment configuration, operations, and release readiness | Not started |

## Current implementation

- The existing modular directory layout is retained.
- The Streamlit entry point and environment-based settings are in place.
- A root `.venv` exists and is used for local Python development.
- All ten direct requirements are installed in `.venv`; `pip check` reports no
  broken requirements.
- The configuration test suite passes when run with `.venv` (2 tests).
- No authentication, database access, AI provider, or research provider is wired
  into the application.
- Provider access, credentials, endpoints, and model availability remain
  unconfigured.

## Repository and environment status

- Virtual environment: created at the project root; preserved during this
  setup.
- Dependency installation: verified in `.venv`; tests and `pip check` passed.
- Git: not started; not initialized.
- GitHub: not started; no repository or connection is configured or verified.

## Remaining foundation review tasks

- Review dependency update and compatibility policy before deployment.
- After review, initialize Git and configure the intended GitHub repository
  when authorized.
- Confirm setup and test instructions in a clean checkout.
- Plan deployment and install production dependencies in the deployment
  environment separately from local development.

## Product and architecture work still outstanding

- Choose an OIDC provider and define its setup and callback configuration.
- Select the research/search provider and confirm its supported API and terms.
- Confirm NVIDIA NIM access, model availability, and integration details.
- Design domain models and PostgreSQL schema, with ownership enforced on every
  project data operation.
- Add clearly labelled fallback behavior and tests for unavailable providers.
- Plan deployment, operations, data retention, and privacy requirements.
