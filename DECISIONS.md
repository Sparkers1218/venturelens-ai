# Architecture Decisions

## Agreed

| Area | Decision |
|---|---|
| Language and UI | Python and Streamlit |
| Application shape | Modular monolith |
| Authentication | OpenID Connect (OIDC) |
| Production database | PostgreSQL |
| ORM and migrations | SQLAlchemy and Alembic |
| AI integration | NVIDIA NIM |
| External research | A separate research/search API |
| Validation and HTTP | Pydantic and HTTPX |
| Tests | pytest |
| Version control | Git and GitHub |

Keep UI, business logic, database operations, and external integrations in
separate modules. Enforce user ownership in every project database operation.
When an external provider is unavailable, the product should remain usable and
label fallback behavior clearly.

## Local and deployment environments

Use a project-root `.venv` for isolated local Python development. The existing
virtual environment is preserved; do not commit it. Dependencies for production
will be installed separately in the deployment environment using that
environment's deployment process, rather than relying on or copying the local
`.venv`.

## Not yet decided or configured

- OIDC provider, client registration, and deployment-specific callback settings
- Research provider, API contract, and source attribution details
- NVIDIA NIM access, model choice, and verified availability
- Domain schema, report retention, and data deletion policy
- Deployment target, observability, and operational requirements

Do not treat these unresolved items as configured. Do not add credentials,
assumed endpoints, or claims about provider availability until verified.
