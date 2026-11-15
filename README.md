# VentureLens AI

**Better Questions. Stronger Ideas.**

VentureLens AI is a local-demo startup idea validation workspace. It helps
aspiring entrepreneurs capture an idea, record competitors and source notes,
review a transparent structured report, and plan practical validation
experiments.

The product must distinguish external evidence, user-provided information,
assumptions, and AI-generated recommendations. It must not invent market
statistics or promise that an idea will succeed.

## Technology and architecture

- Python and Streamlit
- Streamlit UI, Pydantic input validation, SQLAlchemy persistence, and a
  deterministic rule-based analysis module
- SQLite by default; PostgreSQL URLs are supported through `DATABASE_URL`
- pytest for automated tests

No AI or live research provider is configured or required. Authentication and
multi-user access controls are not implemented. See
[PROJECT_STATUS.md](PROJECT_STATUS.md) for what is and is not included.

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

The app defaults to the local SQLite database `venturelens.db`. To use the same
defaults through a local environment file, optionally copy the example:

```bat
copy .env.example .env
```

Edit `DATABASE_URL` in `.env` only if you have independently configured a
database. Never commit `.env` or put credentials in `.env.example`.

Initialize the database (the app also initializes it at startup):

```bat
python -m database.init_db
```

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

## Current implementation status

The app supports persistent idea projects with problem, solution, customer,
industry, geography, and optional business-model details. Competitor records
include a description, website/reference, target audience, pricing, and
differentiation notes. Manual research notes capture a title, publisher, URL,
and notes.

Generate and save a structured rule-based report with 0-3 information-coverage
scores, risk counts, competitor comparison, assumptions, and validation
experiments. Score rubrics are included in each report; scores measure only
how much information was entered, never commercial viability. The report can
be downloaded as JSON and reopened with the project.

All competitor and research details are user-provided and unverified. No URLs
are fetched; no AI or external research is used. Reports clearly label their
provenance and assumptions.

The demo is single-user and local: there is no login, authorization, tenant
isolation, live research, or AI-generated analysis. There is no Alembic
migration framework; startup applies the current additive schema upgrades to
existing local databases.
Source notes and competitor records are manually entered and are not
independently verified. The completeness indicator measures only whether
fields are filled; it is not a market or success score.

See [PROJECT_STATUS.md](PROJECT_STATUS.md), [DECISIONS.md](DECISIONS.md), and
the product requirements in `docs/02-requirements/PRODUCT_REQUIREMENTS.md`.
