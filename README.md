# VentureLens AI

**Better Questions. Stronger Ideas.**

VentureLens AI is a startup idea validation demo. It helps
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
- SQLite by default; PostgreSQL URLs are configurable through `DATABASE_URL`
- pytest for automated tests

No AI or live research provider is configured or required. Authentication and multi-user access controls are not implemented. See
[PROJECT_STATUS.md](PROJECT_STATUS.md) for what is and is not included.
See [FINAL_RELEASE_AUDIT.md](FINAL_RELEASE_AUDIT.md) for the latest verification
results and release limitations, and [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
for the public synthetic evaluator demo setup.

Choose **☀️ Light** or **🌙 Dark** from the appearance control in the application
header. The theme is applied throughout the UI and remains selected across
Streamlit reruns in the current session; it resets when a new session starts.

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
be downloaded as JSON and reopened with the project. Earlier report versions
remain selectable across navigation; the report view warns when project inputs
have changed since the latest saved analysis.

All competitor and research details are user-provided and unverified. No URLs
are fetched; no AI or external research is used. Reports clearly label their
provenance and assumptions.

The normal local workflow uses persistent storage and is single-user: there is
no login, authorization, or tenant isolation. The separate public evaluator
mode uses only a clearly labeled fictional sample in temporary in-memory
storage; write controls are disabled and database writes are blocked. It does
not accept or persist evaluator project data. This mode is not authentication
or a public multi-user service. There is no Alembic migration framework;
startup applies the current additive schema upgrades to existing local
databases.
Source notes and competitor records are manually entered and are not
independently verified. The completeness indicator measures only whether
fields are filled; it is not a market or success score.

### Public evaluator demo

The public, synthetic read-only evaluator demo is available at
[venturelens-ai-spark2scale.streamlit.app](https://venturelens-ai-spark2scale.streamlit.app/).
It displays the **PUBLIC EVALUATOR DEMO** notice and fictional sample data.
Evaluators do not need an account. The demo does not accept or persist their
project data; it uses temporary in-memory SQLite and disables writes. Do not
enter real project, customer, or personal information.

The Streamlit Community Cloud startup issue caused by settings not reading
`st.secrets` has been fixed. Hosted dashboard, sample data, navigation, theme
switching in both directions, and disabled project creation were verified
after UI recovery commit `8e9c665f41461f2e054bd48a3c527eaf60233abd`. A local
browser sweep covered all application pages in both themes at requested widths
320, 375, 390, 430, 768, 1024, and 1440 CSS pixels without observed horizontal
overflow or clipped content. The browser rounded 375 to 376 and 430 to 431 CSS
pixels. These responsive checks were local, not a viewport-by-viewport test of
the hosted deployment. See
[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment configuration and
limitations. This public demo is not authenticated multi-user hosting.

The public evaluator deployment uses `APP_ENV="production"` and
`DEMO_MODE=true` in the host's Secrets settings; it does not require a
database URL, OAuth credentials, AI key, or research key.
Public multi-user project storage would require authentication, ownership
enforcement, persistent database hosting, migrations, and cross-user security
tests.

See [PROJECT_STATUS.md](PROJECT_STATUS.md), [DECISIONS.md](DECISIONS.md), and
the product requirements in `docs/02-requirements/PRODUCT_REQUIREMENTS.md`.
