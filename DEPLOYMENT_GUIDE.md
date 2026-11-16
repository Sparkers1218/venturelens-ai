# Public Evaluator Demo Deployment

The deployment-ready source is pushed to
[`feature/project-ui`](https://github.com/Sparkers1218/venturelens-ai/tree/feature/project-ui)
at commit
[`a28ca4f`](https://github.com/Sparkers1218/venturelens-ai/commit/a28ca4fbdd05b9c42595721b908a286ee1fbf6cb).
No Community Cloud app has been created yet; the current browser session is
signed out and must be authorized before deployment.

## What this deployment is

The recommended hosting target is **Streamlit Community Cloud**. The app runs
in a public, read-only evaluator mode with one clearly labeled, fictional
sample project. That mode uses in-memory SQLite, ignores `DATABASE_URL`, and
blocks database writes. It does not accept or persist evaluator project data.

This is not authentication or a multi-user service. It is intentionally a
public synthetic-data presentation. Do not add real project, customer, or
personal information. AI-provider, research-provider, OAuth, and database
credentials are not required.

## Before opening the Cloud console

1. Sign in to Streamlit Community Cloud using a GitHub account authorized to
   access `Sparkers1218/venturelens-ai`. Approve the Community Cloud OAuth
   access request if prompted, including access to this repository.
2. Do not add `.env`, `.streamlit/secrets.toml`, API keys, or database
   credentials to Git. `.streamlit/secrets.toml` is ignored by `.gitignore`.

## Create the app

1. Select **Create app** (or **Deploy an app**) and choose:
   - Repository: `Sparkers1218/venturelens-ai`
   - Branch: `feature/project-ui`
   - Main file path: `app.py`
2. Open **Advanced settings** before deploying and select **Python 3.12**.
3. In the **Secrets** field, enter this TOML exactly:

   ```toml
   APP_ENV = "production"
   DEMO_MODE = true
   ```

   These two settings are required. No other secret or `DATABASE_URL` is
   required. In production, the app refuses to start unless demo mode is
   enabled; demo mode always selects its own in-memory database. VentureLens
   reads these root-level values directly from Streamlit's `st.secrets`; it
   does not rely on the host exporting them as process environment variables.
   Process environment variables still take precedence over `.env`, which
   takes precedence over Streamlit Secrets.
4. Select **Deploy** and wait for the app to finish starting. The first
   dependency installation can take several minutes.

## Verify before sharing

Open the generated HTTPS URL in a private/incognito browser window and confirm:

- The page loads without an error and displays the **PUBLIC EVALUATOR DEMO**
  notice.
- The fictional **Synthetic sample: Harbor Harvest Planner** project and its
  rule-based report are visible.
- Project creation, editing, research entry, competitor entry, report
  generation, and deletion are unavailable; the sample report JSON download
  remains available.
- The profile/settings pages state that accounts and authentication are not
  enabled.
- No real project data or credentials are present.

If startup fails, check the Community Cloud app logs and confirm that the two
Secrets entries above were saved. Never paste secrets into a public issue or
commit them to the repository.

## Evaluator access and operating limits

Once the checks pass, copy the app's public HTTPS URL and share it with the
evaluators. The app is intentionally public and requires no evaluator account.
All visitors see the same fictional sample. Its database exists only in the
running app process and is recreated when the process restarts; it is not a
persistent evaluator workspace.

There is no app-level authentication, authorization, project ownership, or
tenant isolation. Do not enable write workflows or use a real shared database
for this public app. Public multi-user project storage requires a separate
implementation of authentication and per-user authorization, a persistent
database, migrations, and cross-user security tests.

## Local workflow remains unchanged

For the normal local, persistent demo, leave `DEMO_MODE` unset or set it to
`false`. Continue to configure `DATABASE_URL` locally if needed. The public
mode can also be run locally by setting `APP_ENV=production` and
`DEMO_MODE=true`; it will still use only in-memory synthetic data.
