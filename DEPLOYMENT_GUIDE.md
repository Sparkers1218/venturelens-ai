# Public Evaluator Demo Deployment

The synthetic read-only demo is deployed at
[https://venturelens-ai-spark2scale.streamlit.app/](https://venturelens-ai-spark2scale.streamlit.app/).
The deployed branch is `feature/project-ui`, with `app.py` as the entry point.
The Streamlit Secrets loading fix was pushed in commit
[`c256b4d`](https://github.com/Sparkers1218/venturelens-ai/commit/c256b4d8c2fd6f33f3c5991040ccb27c4c005fe2).
The hosted dashboard, fictional sample, navigation, theme switching in both
directions, and disabled project-creation state were verified after UI
recovery commit `8e9c665f41461f2e054bd48a3c527eaf60233abd`.

## What this deployment is

The recommended hosting target is **Streamlit Community Cloud**. The app runs
in a public, read-only evaluator mode with one clearly labeled, fictional
sample project. That mode uses in-memory SQLite, ignores `DATABASE_URL`, and
blocks database writes. It does not accept or persist evaluator project data.

This is not authentication or a multi-user service. It is intentionally a
public synthetic-data presentation. Do not add real project, customer, or
personal information. AI-provider, research-provider, OAuth, and database
credentials are not required.

## Existing deployment

Evaluators can open the public URL above without an account. The application
visibly identifies itself as a public evaluator demo and contains only
fictional sample data. Do not enter real project, customer, or personal data.

The original startup failure occurred because Pydantic settings did not read
Streamlit Community Cloud's separate `st.secrets` store. The app now reads
root-level Streamlit Secrets directly while preserving process-environment
and `.env` precedence. Production still fails closed when `DEMO_MODE` is
absent or false.

## Recreate or inspect the Cloud app

1. Sign in to Streamlit Community Cloud using a GitHub account authorized to
   access `Sparkers1218/venturelens-ai`. Approve the Community Cloud OAuth
   access request if prompted, including access to this repository.
2. Do not add `.env`, `.streamlit/secrets.toml`, API keys, or database
   credentials to Git. `.streamlit/secrets.toml` is ignored by `.gitignore`.

## Configure a new or existing app

1. If the evaluator app already exists, open its settings; otherwise select
   **Create app** (or **Deploy an app**).
2. Select:
   - Repository: `Sparkers1218/venturelens-ai`
   - Branch: `feature/project-ui`
   - Main file path: `app.py`
3. Open **Advanced settings** before deploying and select **Python 3.11**.
4. In the **Secrets** field, enter this TOML exactly:

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
5. Select **Deploy** and wait for the app to finish starting. The first
   dependency installation can take several minutes. The verified deployment
   used Python 3.11.18.

## Verify before sharing

Open the deployed HTTPS URL in a private/incognito browser window and confirm:

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

Verified on the current deployment: the dashboard and fictional sample
loaded; My Projects and Create Project navigation worked; project creation
displayed the read-only message; and the light/dark controls switched
successfully in both directions. A local browser sweep also covered every
navigation page in both themes at requested widths 320, 375, 390, 430, 768,
1024, and 1440 CSS pixels without observed overflow or clipped content. The
browser rounded 375 to 376 and 430 to 431 CSS pixels. That responsive sweep
was not performed against the public deployment. During the latest UI
verification, Cloud application logs were not directly inspected. The browser
console showed resource 404s, aborted status-page embed requests, Vega chart
warnings, and one transient WebSocket close (1006); the verified page remained
responsive. A separate private/incognito walkthrough and every settings/profile
page were not part of this verification.

If startup fails, check the Community Cloud app logs and confirm that the two
Secrets entries above were saved. Never paste secrets into a public issue or
commit them to the repository.

## Evaluator access and operating limits

Share the public HTTPS URL above with evaluators. The app is intentionally
public and requires no evaluator account. All visitors see the same fictional
sample. Its database exists only in the running app process and is recreated
when the process restarts; it is not a persistent evaluator workspace.

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
