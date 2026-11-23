# Task Management API

A REST API for account registration and authentication, with task management scoped to the authenticated user. The project is built with FastAPI, SQLAlchemy, and MySQL, and includes background registration emails.

## Features

- Register users and hash their passwords before storing them.
- Log in and receive a signed JWT.
- Create, list, retrieve, update, and delete tasks belonging to the authenticated user.
- Schedule registration confirmation emails as background tasks.
- Check API availability and database connectivity.
- Create database tables from the SQLAlchemy models when the application starts.

## Technology

- Python 3.11+
- FastAPI and Uvicorn
- SQLAlchemy and PyMySQL (MySQL)
- Pydantic Settings and `python-dotenv`
- PyJWT for tokens
- `pwdlib` for password hashing
- FastAPI Mail for registration email
- Alembic for database migrations
- `uv` for dependency management (`uv.lock` is included)

## Project layout

```text
.
├── main.py                 # FastAPI app, lifespan, and health endpoints
├── src/
│   ├── tasks/              # Task routes, request/response schemas, and database logic
│   ├── user/               # User routes, schemas, models, and authentication logic
│   └── utils/              # Database, settings, token authentication, and email helpers
├── migration/              # Alembic environment and migration revisions
├── alembic.ini
├── pyproject.toml
└── uv.lock
```

## Getting started

### Prerequisites

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)
- A reachable MySQL server and a database for the application

### 1. Install dependencies

From the project directory, run:

```bash
uv sync
```

### 2. Configure environment variables

Create a `.env` file in the project root. Keep real credentials and signing keys out of source control.

```dotenv
DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:3306/<database>
SECRETE_KEY=<long-random-signing-key>
ALGORITHM=HS256
EXP_TIME=30

MAIL_USERNAME=<smtp-username>
MAIL_PASSWORD=<smtp-password>
MAIL_FROM=<sender-email-address>
```

`EXP_TIME` is the token lifetime in minutes. The setting is spelled `SECRETE_KEY` in the current application configuration; use that exact name. The email helper is configured for Gmail SMTP on port 587. Use an SMTP credential accepted by your mail provider, not a regular account password.

If a value in your MySQL username or password contains URL-reserved characters, URL-encode it in `DATABASE_URL`.

### 3. Start the API

```bash
uv run uvicorn main:app --reload
```

The development server is available at <http://127.0.0.1:8000>. On startup, the app checks the database connection and calls SQLAlchemy `create_all` for the registered models. The database itself must already exist.

Interactive API documentation:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI schema: <http://127.0.0.1:8000/openapi.json>

## API reference

All request and response bodies use JSON. Task routes require an authenticated user and operate only on that user's tasks. Send the token returned by login as `Authorization: Bearer <token>`.

### Health

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| `GET` | `/` | Check that the API is responding | `200 OK` |
| `GET` | `/test-db` | Check database connectivity | `200 OK` |

### Users and authentication

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| `POST` | `/user/register` | Register a user; schedules a confirmation email | `201 Created` |
| `POST` | `/user/login` | Verify credentials and return a JWT | `200 OK` |
| `GET` | `/user/is_auth` | Return the user associated with the supplied JWT | `200 OK` |

Registration request:

```json
{
  "name": "Alex Morgan",
  "username": "alex",
  "hash_password": "choose-a-password",
  "email": "alex@example.com"
}
```

Login request:

```json
{
  "username": "alex",
  "hash_password": "choose-a-password"
}
```

The login response contains a `token` field. Registration and authentication responses include the user's `id`, `name`, `username`, and `email`; the password hash is not included.

### Tasks

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| `POST` | `/tasks/create` | Create a task for the authenticated user | `201 Created` |
| `GET` | `/tasks/all_tasks` | List the authenticated user's tasks | `200 OK` |
| `GET` | `/tasks/one_task/{task_id}` | Get one of the authenticated user's tasks | `200 OK` |
| `PUT` | `/tasks/update_task/{task_id}` | Replace a task's editable fields | `201 Created` |
| `DELETE` | `/tasks/delete_task/{task_id}` | Delete one of the authenticated user's tasks | `204 No Content` |

Task creation and update body:

```json
{
  "title": "Prepare project notes",
  "description": "Review and organize the API documentation",
  "is_completed": false
}
```

`is_completed` defaults to `false` when omitted. Task responses include `id`, `title`, `description`, `is_completed`, and `user_id`. Requests for a task that does not exist or does not belong to the authenticated user are rejected.

### Example: authenticate and create a task

Register or log in first, then use the returned token in the `Authorization` header:

```bash
curl -X POST http://127.0.0.1:8000/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alex","hash_password":"choose-a-password"}'
```

```bash
curl -X POST http://127.0.0.1:8000/tasks/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"Prepare project notes","description":"Review the API docs","is_completed":false}'
```

## Database and migrations

The SQLAlchemy models are in `src/user/models.py` and `src/tasks/models.py`. On application startup, `Base.metadata.create_all()` creates missing model tables; it does not update existing tables when models change.

Alembic is configured in `alembic.ini` and `migration/`. A migration revision is included for adding the task-to-user foreign key. Review the current database schema and migration history before applying migrations to an existing database; the checked-in revision assumes the relevant tables already exist.

## Current implementation notes

- Task endpoints are protected by JWT authentication and return tasks belonging to the signed-in user.
- The task update route currently responds with `201 Created`.
- Registration schedules email sending through FastAPI background tasks; configure the mail environment variables for delivery.
- This README describes the routes and behavior currently implemented in the repository.
