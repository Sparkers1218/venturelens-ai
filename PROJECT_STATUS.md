# Project Status

## Milestones

| Milestone | Scope | Status |
|---|---|---|
| 1. Project Foundation | Entry point, dependencies, configuration, documentation, and basic tests | Complete |
| Project Charter | Initial project charter documentation | Complete |
| 2. Core domain | Idea briefs, evidence, assumptions, risks, and experiment concepts | MVP implemented |
| 3. Persistence | SQLAlchemy models, SQLite/PostgreSQL URL support, and repositories | MVP implemented; additive upgrades included, Alembic and ownership pending |
| 4. Authentication | OIDC integration and authenticated user context | Not implemented |
| 5. Research integration | Research provider, retrieval, and evidence attribution | Not implemented |
| 6. AI provider integration and evaluation | Provider evaluation and structured analysis | Deterministic rule-based engine implemented; no AI provider |
| 7. User workflows | Streamlit pages for idea intake, analysis, and saved reports | Local MVP implemented |
| 8. Hardening and release | Deployment configuration and release verification | Read-only synthetic evaluator mode and Streamlit Community Cloud configuration prepared; hosted deployment not yet performed |

## Current implementation

- The normal local workflow supports project creation, editing, search,
  reopening, and deletion, with persistent SQLite by default. PostgreSQL URL
  configuration exists but has not been integration-tested against a server.
- Navigation includes dashboard, My Projects, project creation, competitor
  insights, research, report review, derived notifications/activity, profile,
  settings, and project workspace. The light/dark theme control is preserved.
- Competitor and source records are manual entry only; they are not retrieved
  or independently verified.
- Versioned deterministic reports cover problem/solution, customer definition,
  competitor comparison, business-model considerations, brief strengths and
  gaps, risks, assumptions, research references, experiments, and next steps.
  JSON download is available. Scores describe information coverage/detail, not
  viability or success.
- The public evaluator mode is separate from the local workflow. It overrides
  any configured database URL with in-memory SQLite, seeds only clearly
  labeled fictional sample data, disables write controls, enables SQLite's
  query-only mode, and allows report JSON download.
- Production startup fails closed unless `DEMO_MODE=true`. The prepared public
  configuration requires `APP_ENV="production"` and `DEMO_MODE=true`.
- The public sample is temporary and is recreated after process restart. It
  accepts no evaluator project data and makes no authentication or ownership
  claims.
- Authentication, per-user ownership, tenant isolation, live research, and
  AI-provider integration are not implemented. Do not use the app as a public
  multi-user project service.
- The sample alternatives and report are fictional demonstration content,
  not real competitor findings, market research, or customer evidence.

## Deployment status

- `.streamlit/config.toml` and [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
  prepare the app for Streamlit Community Cloud.
- The deployment source is pushed to `feature/project-ui` at commit
  `a28ca4fbdd05b9c42595721b908a286ee1fbf6cb`. Hosting still requires an
  authorized Community Cloud sign-in and deployment. No public URL has been
  created or tested.
- Community Cloud Secrets for the prepared demo are:

  ```toml
  APP_ENV = "production"
  DEMO_MODE = true
  ```

- No database, OAuth, AI, or research-provider credentials are needed for the
  synthetic demo. Never commit secrets.
- Public multi-user project storage remains out of scope until authentication,
  ownership enforcement, persistent storage, migrations, and cross-user tests
  exist.

## Verification

- `.venv\Scripts\python.exe -m pytest -q`: **15 passed in 3.65s**.
- Python compilation, Streamlit config/Secrets TOML parsing, and
  `git diff --check` passed.
- AppTest verified production evaluator startup, synthetic sample display,
  disabled mutation controls, report download-button availability, database
  URL isolation, SQLite write blocking, and production fail-closed behavior.
- A local Streamlit process returned HTTP 200 from `/healthz`; the configured
  external database file was not created.
- No hosted deployment or public URL has been created. Full details and
  remaining manual checks are in [FINAL_RELEASE_AUDIT.md](FINAL_RELEASE_AUDIT.md).

## Known limitations and remaining work

- No AI provider is configured; analysis is deterministic Python logic, not an
  AI model. NVIDIA NIM remains only a candidate in [DECISIONS.md](DECISIONS.md).
- No live competitor or research retrieval, source verification, or external
  attribution is implemented.
- No authentication or user/project ownership isolation exists.
- There is no Alembic migration history. Existing local schema support is
  limited to the explicit additive upgrades in `database/connection.py`.
- PostgreSQL connectivity and Streamlit Community Cloud deployment have not
  been verified against live services.
- Public demo data is in memory only and is not persistent across process
  restarts.
- A deployed browser session, public URL access, and evaluator sharing still
  require manual verification after deployment.
