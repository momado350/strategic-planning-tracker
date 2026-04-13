# Library Strategic Priorities Tracker

A Flask app for managing strategic priorities, KPIs, quarterly updates, monthly service entries, scorecards, and reference workbook downloads.

## Render deployment

This version is prepared to run on Render the same way as a simple Flask production app:

- you create a Render Postgres database
- you create a Render web service from this repo
- you add `DATABASE_URL` in Render
- the app automatically creates tables on first boot
- the app automatically seeds the starter data if the database is empty

### Environment variables for Render

Add these in the Render web service:

- `DATABASE_URL` = the Internal Database URL or External Database URL from your Render Postgres service
- `SECRET_KEY` = any long random string
- `AUTO_CREATE_TABLES=true`
- `AUTO_SEED_DATA=true`

### Start command

```bash
gunicorn app:app
```

### Build command

```bash
pip install -r requirements.txt
```

### Demo login after first deploy

If the database is empty and auto-seeding is on, these users are created:

- Admin: `admin@example.com` / `password123`
- Editor: `editor@example.com` / `password123`
- Viewer: `viewer@example.com` / `password123`

Change these passwords after deployment.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

If `DATABASE_URL` is not set locally, the app falls back to a local SQLite file named `app.db`.

## Manual commands

```bash
python app.py init-db
python app.py reset-db
python app.py seed-demo
```

## Included files

- `render.yaml`
- `requirements.txt`
- `.env.example`
- application code under `app/`
- reference workbooks under `reference_workbooks/`

## Notes

- Render sometimes provides PostgreSQL URLs beginning with `postgres://`. This app converts them automatically.
- The reference workbook downloads are served from the `reference_workbooks` folder bundled with the app.
