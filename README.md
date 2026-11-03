# VentureLens AI

**Better Questions. Stronger Ideas.**

VentureLens AI is an AI-powered startup idea validation platform in its
foundation stage. It is intended to help aspiring entrepreneurs describe an
idea and its customers, investigate competitors and alternatives, review
external research, identify assumptions and risks, and plan practical,
low-cost validation experiments.

The product must distinguish external evidence, user-provided information,
assumptions, and AI-generated recommendations. It must not invent market
statistics or promise that an idea will succeed.

## Technology and architecture

- Python and Streamlit
- Modular monolith, with UI, business logic, persistence, and integrations kept
  separate as the application grows
- OpenID Connect (OIDC) for planned authentication
- PostgreSQL with SQLAlchemy and Alembic for planned persistence and migrations
- NVIDIA NIM and a separate research/search API for planned integrations
- Pydantic for validation, HTTPX for HTTP clients, and pytest for tests

External providers and credentials have not been configured. No provider
endpoints or model availability are assumed.

## Getting started (Windows)

Prerequisites: Python with `venv` and `pip`, plus Windows Command Prompt or
PowerShell. The project currently has a `.venv` virtual environment in its root.
This environment is local to your checkout and must not be committed to Git.
If you are setting up a fresh checkout and `.venv` does not exist, create it
from the project root:

```powershell
python -m venv .venv
```

Activate the environment in **Command Prompt**:

```bat
.venv\Scripts\activate.bat
```

Activate it in **PowerShell**:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project's dependencies after activation:

```bat
python -m pip install -r requirements.txt
```

Create a local environment file only if you need to supply configuration for
services you have independently set up:

```bat
copy .env.example .env
```

Edit `.env` locally. Never commit it or put real credentials in
`.env.example`.

Run the Streamlit application:

```bat
python -m streamlit run app.py
```

Run the tests:

```bat
python -m pytest -v
```

When finished, deactivate the virtual environment:

```bat
deactivate
```

Git and GitHub setup have not started. Wait for review before proceeding with
version control setup.

## Current implementation status

Milestone 1 provides the initial project configuration, a Streamlit landing
page, and basic configuration tests. Authentication, database connections and
migrations, AI analysis, and external research are not implemented. See
[PROJECT_STATUS.md](PROJECT_STATUS.md) and [DECISIONS.md](DECISIONS.md).
