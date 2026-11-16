# Public Evaluator Demo Deployment

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

1. Make this completed source branch available in the GitHub repository. The
   deployment host can only deploy commits already present on GitHub.
2. Confirm you have GitHub access to `Sparkers1218/venturelens-ai` and can
   create an app in Streamlit Community Cloud.
3. Do not add `.env`, `.streamlit/secrets.toml`, API keys, or database
   credentials to Git. `.streamlit/secrets.toml` is ignored by `.gitignore`.

## Create the app

1. Sign in to Streamlit Community Cloud with the GitHub account that can access
   `Sparkers1218/venturelens-ai`.
2. Select **Create app** (or **Deploy an app**) and choose:
   - Repository: `Sparkers1218/venturelens-ai`
   - Branch: `feature/project-ui`
   - Main file path: `app.py`
3. Open **Advanced settings** before deploying and select **Python 3.12**.
4. In the **Secrets** field, enter this TOML exactly:

   ```toml
   APP_ENV = "production"
   DEMO_MODE = true
   ```

   These two settings are required. No other secret or `DATABASE_URL` is
   required. In production, the app refuses to start unless demo mode is
   enabled; demo mode always selects its own in-memory database.
5. Select **Deploy** and wait for the app to finish starting. The first
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
