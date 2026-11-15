# VentureLens AI — Project Charter

## 1. Document information and version

| Field | Value |
|---|---|
| Document | Project Charter |
| Project | VentureLens AI |
| Version | 1.0 |
| Status | Initial charter |
| Last updated | 2026-11-04 |
| Problem statement | PS49 — AI Startup Idea Validator |
| Track | Business, FinTech & Emerging Tech |

This charter records the product direction and proposed scope. It does not
assert that planned features, providers, or infrastructure have been
implemented or selected.

## 2. Project overview

VentureLens AI is intended to help entrepreneurs examine startup ideas through
structured problem analysis, competitor research, evidence-linked insights,
assumptions, risks, missing information, and practical validation experiments.

**Tagline:** Better Questions. Stronger Ideas.

### Historical implementation snapshot

At the charter's initial drafting on 2026-11-04, the inspected project
contained a Streamlit landing page, environment settings, and basic settings
tests. That description records the starting point; it is not the current
implementation status.

### Current local MVP status (2026-11-15)

- SQLAlchemy persistence with SQLite is implemented for projects, competitors,
  manual research sources, and saved reports. Project creation, editing,
  deletion, and retrieval are available.
- Competitor and research records can be manually added, listed, and removed.
  Research is not automatically retrieved or verified.
- Analysis is deterministic and rule-based. There is no AI provider or live
  research provider integration. Reports are saved, downloadable as JSON, and
  include charts based on application data.
- Authentication and per-user ownership enforcement are not implemented.
  The application is suitable only for a controlled local, single-user
  demonstration.
- Existing test baseline: 9 passed, 0 failed. It was not rerun for this
  documentation-only update.

## 3. Problem statement

Aspiring founders may have difficulty turning an initial idea into a structured
investigation. They need a way to examine the problem and its users, consider
competitors and alternatives, distinguish evidence from assumptions, identify
gaps and risks, and choose practical ways to learn more.

VentureLens AI aims to support that investigation. It does not determine
whether a startup will succeed or guarantee business outcomes.

## 4. Project vision

Provide entrepreneurs with a clear, evidence-aware workspace for asking better
questions about an idea and planning useful next steps, while making
uncertainty and the origin of each insight visible.

## 5. Project objectives

- Guide users through a structured description of an idea, its problem, and
  intended customers.
- Support investigation of competitors, alternatives, and relevant external
  research.
- Keep sourced evidence, user-provided information, assumptions, AI
  interpretations, and recommendations distinguishable.
- Surface risks, missing information, and questions for further validation.
- Help users plan practical validation experiments.
- Keep AI and research integrations replaceable through separate provider
  adapters.
- Preserve a modular Python application structure and a path to persistent,
  user-owned project data.

These objectives describe intended outcomes, not current capabilities.

## 6. Target users and stakeholders

| Group | Interest |
|---|---|
| Aspiring entrepreneurs | Explore and investigate an initial startup idea. |
| Student founders | Structure early research and plan validation activities. |
| Early-stage startup teams | Organize evidence, assumptions, risks, and next steps. |
| Project team and maintainers | Build, test, operate, and maintain the product. |
| External providers, if selected | Supply authentication, research, AI, or hosting capabilities under verified terms. |

The provider group is conditional: no authentication, AI, research, or hosting
provider has been finalized.

## 7. Proposed product workflow

1. User describes an idea, the problem it addresses, and intended customers.
2. The product organizes the description and identifies questions or missing
   information.
3. If configured, a research adapter retrieves external material and retains
   source attribution.
4. If configured, an AI adapter helps synthesize the available inputs into
   structured insights.
5. The product presents evidence, user input, assumptions, AI interpretations,
   risks, and recommendations as distinct categories.
6. User reviews the analysis and plans practical validation experiments.
7. The local MVP allows users to return to saved projects and reports; user
   authentication and ownership enforcement remain future work.

Provider-dependent steps must not be presented as available until their
providers and access are configured. The local project and report workflow is
implemented in the current MVP; live research, AI synthesis, and authenticated
user ownership are not.

## 8. MVP scope — included features

The following are proposed MVP capabilities, subject to technical and provider
decisions:

- Streamlit interface for idea intake and structured results.
- Python modular monolith with distinct UI, domain/business logic, persistence,
  and integration boundaries.
- Structured problem and customer analysis, including questions and missing
  information.
- Competitor and alternative research through a replaceable research adapter,
  with source attribution.
- AI-assisted synthesis through a replaceable AI provider adapter.
- Clear labeling of evidence, user-provided information, assumptions, AI
  interpretations, risks, and recommendations.
- Practical validation experiment planning.
- PostgreSQL persistence using SQLAlchemy and Alembic, with user ownership
  enforced for project data operations.
- Automated tests using pytest for domain behavior and relevant integration
  boundaries.
- OIDC authentication, subject to selection of a provider and confirmation of
  its terms and configuration requirements.

These bullets describe the intended product scope. The current implementation
covers only the local MVP described in Section 2; authentication, ownership
enforcement, AI, and live research remain unimplemented.

## 9. Out-of-scope features

The MVP is not intended to:

- Predict, certify, or guarantee startup success, investment returns, or other
  business outcomes.
- Replace professional legal, financial, or investment advice.
- Treat AI-generated interpretations as verified facts.
- Present unsupported market statistics or research claims as evidence.
- Include a marketplace, fundraising, investor matching, or full business
  operations suite unless separately approved.
- Depend on a single AI or research provider in application business logic.

## 10. Technical constraints and principles

- **UI:** Streamlit is implemented for the local MVP's dashboard, project
  workflows, and saved reports. The landing-page-only description above is a
  historical snapshot.
- **Application structure:** Python modular monolith, keeping UI, domain logic,
  persistence, and provider integrations separate.
- **Authentication:** OIDC is the planned direction; provider and configuration
  are open decisions.
- **Persistence:** SQLAlchemy models and repositories with SQLite by default
  are implemented for the local MVP. PostgreSQL URLs are configurable but
  PostgreSQL integration is not verified; Alembic migrations are not
  implemented.
- **AI and research:** Use separate provider adapters so providers can be
  replaced. Provider choices and integrations are not finalized.
- **Validation and HTTP:** Pydantic is used for domain input validation.
  HTTPX is present in the dependency manifest but is not used for a provider
  integration.
- **Testing:** pytest covers settings, validation, persistence, rule-based
  reports, and the Streamlit workflow. The existing recorded baseline is 9
  passed and 0 failed; it was not rerun for this documentation update.
- **Data boundaries:** Keep evidence, user input, assumptions, AI
  interpretations, and recommendations distinguishable. Enforce ownership for
  every project data operation in authenticated/shared releases; the current
  local MVP has persistence but no ownership enforcement.
- **Configuration:** Use environment-based configuration; keep credentials out
  of source control and example files.
- **Resilience:** Provider failures should be communicated clearly. Any
  fallback must be labeled and must not imply that unavailable research or AI
  work occurred.

## 11. Cost and tooling policy

- No mandatory paid software, subscription, API, or service may be required to
  use or develop the MVP.
- Prefer free and open-source technologies where they satisfy the requirements.
- Before selecting a hosted provider or service, verify current free-tier
  limits, licensing and usage terms, payment-method requirements, and possible
  overage charges. Record the date and source of verification in the relevant
  implementation decision.
- Do not assume a free tier exists or remains available.
- Evaluate self-hosting only with its licensing, hardware, hosting, and
  operational costs included; open-source software does not make infrastructure
  free.
- Keep provider integrations replaceable and avoid coupling the core product
  to paid-only capabilities.
- Current Python dependencies are listed in `requirements.txt`; listing a
  dependency does not mean its related feature is implemented or that future
  provider costs have been resolved.

## 12. Risks, assumptions and dependencies

| Type | Item |
|---|---|
| Risk | Provider access, limits, terms, or pricing may change or may not satisfy the no-mandatory-cost constraint. |
| Risk | Research may be incomplete, stale, or poorly matched to a user's idea; source attribution and uncertainty need to remain visible. |
| Risk | AI output may be incorrect or overconfident; it must not be represented as verified evidence or a success prediction. |
| Risk | User-entered startup ideas and saved data may be sensitive; privacy, retention, deletion, and access controls need decisions before production use. |
| Assumption | The initial product is intended for aspiring entrepreneurs, student founders, and early-stage startup teams. |
| Assumption | Streamlit and a Python modular monolith remain suitable for the initial product. |
| Dependency | Authentication, AI, research, and hosting provider choices require documented terms and cost verification before use. |
| Dependency | Persistence depends on a domain model, PostgreSQL environment, migration strategy, and ownership design. |
| Dependency | Delivery depends on project-team decisions for unresolved product, privacy, and operations requirements. |

## 13. Success criteria

The MVP will be considered ready for review when:

- A user can submit an idea and receive an organized analysis of the problem,
  intended customers, open questions, risks, and missing information.
- When research is available, findings include traceable sources; unavailable
  research is not represented as completed.
- Evidence, user-provided input, assumptions, AI interpretations, and
  recommendations are visibly distinguishable.
- AI output is framed as assistance and does not claim to validate success or
  guarantee an outcome.
- A user can produce practical validation experiments from the identified
  questions and risks.
- If saved projects are in scope for the delivered MVP, access to persisted
  project data is authenticated and ownership-enforced.
- Automated tests cover the implemented domain behavior and provider failure
  boundaries.
- Required tools and services do not impose a mandatory paid subscription or
  unverified usage charge.

These criteria are qualitative acceptance conditions, not numeric performance
targets. No quantitative targets have been supplied.

## 14. Project milestones

The sequence reflects the existing project status document; it does not set
dates or imply that unstarted work is complete.

| Milestone | Scope | Status at charter creation |
|---|---|---|
| 1. Project foundation | Entry point, dependencies, configuration, documentation, and basic tests | Complete, per `PROJECT_STATUS.md` |
| 2. Core domain | Idea, evidence, assumptions, risks, and experiment concepts | Not started |
| 3. Persistence | PostgreSQL data model, migrations, repositories, and ownership enforcement | Not started |
| 4. Authentication | OIDC integration and authenticated user context | Not started |
| 5. Research integration | Provider selection, retrieval, and evidence attribution | Not started |
| 6. AI provider integration and evaluation | Evaluate an AI provider, structured analysis, and labeled fallback behavior | Not started |
| 7. User workflows | Streamlit workflows for idea intake, analysis, and saved reports | Not started |
| 8. Hardening and release | End-to-end tests, deployment configuration, operations, and release readiness | Not started |

Milestone order may need adjustment once dependencies, providers, and MVP
acceptance are confirmed.

No AI provider has been selected. NVIDIA NIM remains a candidate pending
verification of free access, usage limits, payment requirements, licensing, and
deployment terms before adoption.

## 15. Open decisions

Each item below remains an **Open Decision**; no option is treated as selected
or verified by this charter.

| Open Decision | Needed before |
|---|---|
| OIDC provider, account model, and callback configuration | Authentication implementation |
| AI provider and model, including access, licensing, limits, payment requirements, and operating costs | AI integration |
| Research provider, source requirements, API terms, limits, and cost | Research integration |
| Hosting provider and its free-tier, payment, overage, and operational terms | Deployment planning |
| PostgreSQL hosting/environment and local development setup | Persistence implementation |
| Domain schema, project data retention, deletion, and privacy policy | Persisting user data |
| Scope and behavior of fallbacks when AI or research services are unavailable | Integration and workflow acceptance |
| MVP prioritization and acceptance ownership | Scheduling and delivery planning |
| Quantitative success measures, if needed | Product evaluation and release review |
| Supported Python versions and dependency reproducibility policy | Developer setup and release planning |

Until these decisions are recorded and verified, provider names in existing
architecture notes are directions to evaluate, not finalized integrations or
commitments.
