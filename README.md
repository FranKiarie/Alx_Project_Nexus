# Project Nexus – Online Poll System (This is my work)

Backend API for creating polls, casting votes once per poll, and viewing results in real time. Built with Django, Django REST Framework, PostgreSQL, and documented via Swagger at `/api/docs`.

## Overview
- RESTful endpoints for polls, voting, and results.
- Duplicate vote prevention enforced at the database level.
- UUID primary keys for public-facing safety.
- Production-ready configuration for Render (PostgreSQL, `DEBUG=False`, `ALLOWED_HOSTS`).
- Live API docs via drf-spectacular at `/api/docs`.

## ERD (must match models)
```
Poll (id PK UUID) 1 ──< Option (id PK UUID)
Poll (id PK UUID) 1 ──< Vote (id PK UUID) >──1 Option (id PK UUID)
Unique: Vote(poll_id, voter_identifier)
```

## Tech Stack
- Django 5, Django REST Framework
- drf-spectacular (Swagger)
- PostgreSQL
- gunicorn (Render)

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # fill in secrets
python manage.py migrate
python manage.py runserver
```

## Environment Variables
- `SECRET_KEY` – Django secret (required)
- `DEBUG` – `False` for production
- `ALLOWED_HOSTS` – comma-separated hosts for production
- `DATABASE_URL` – Postgres URL (`postgres://user:pass@host:5432/db`)
- `CSRF_TRUSTED_ORIGINS` – comma-separated (e.g., `https://your-app.onrender.com`)
- `REQUIRE_AUTH` – set `True` to require auth for write actions (configure auth backend)

## API
- Base URL (Render): `https://<your-render-app>.onrender.com`
- Swagger UI: `/api/docs`
- Schema: `/api/schema`
- Health: `/health/`

### Polls
- `GET /api/polls/` – list (paginated)
  - filters: `?active=true|false`
  - ordering: `?ordering=created_at` (prefix with `-` for desc; allowed: `created_at`, `expires_at`, `question`)
- `POST /api/polls/` – create poll + options
  - body: `{ "question": "...", "expires_at": "...", "options": ["A","B"] }`
- `GET /api/polls/{id}/` – retrieve poll with options
- `POST /api/polls/{id}/vote/` – cast vote
  - body: `{ "option_id": "<uuid>", "voter_identifier": "user-or-ip" }`
- `GET /api/polls/{id}/results/` – aggregated results

### Error Shape (examples)
- 400: `{ "detail": "You have already voted on this poll." }`
- 401: `{ "detail": "Authentication credentials were not provided." }`
- 403: `{ "detail": "You do not have permission to perform this action." }`
- 404: `{ "detail": "Not found." }`

## Tests
```bash
python manage.py test
```

## Deployment (Render)
1) Create Render Web Service (Docker not required) and a Render PostgreSQL instance.  
2) Set env vars: `DATABASE_URL`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=<render-host>`.  
   Also set `CSRF_TRUSTED_ORIGINS=https://<render-host>` and toggle `REQUIRE_AUTH=True` if you want protected writes.  
3) Build command: `pip install -r requirements.txt`  
4) Start command: `gunicorn core.wsgi:application --log-file -`  
5) Run `python manage.py migrate` via Render shell after deploy.  
6) Verify `/health/` then `/api/docs`.

## GitHub (make public)
```bash
git init
git add .
git commit -m "feat: initial poll API backend"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

## Definition of Done Checklist
- ERD matches models.
- CRUD + vote + results endpoints working.
- Duplicate vote prevention via DB unique constraint.
- Swagger live at `/api/docs`.
- Render deployment with PostgreSQL and `/health/` check.
- Clean, conventional commits and readable repo.

