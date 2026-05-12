## Project Overview

This repository is a modular FastAPI backend template.

The project is intended to be a reusable foundation for backend services built with:

- FastAPI
- PostgreSQL
- SQLAlchemy async
- Alembic migrations
- Pydantic settings
- Modular application structure
- Docker support

This is not a single-purpose application. Treat it as a foundation for future modules.

---

## Project Structure

```text
fastapi_template/
├── main.py
├── alembic/
├── alembic.ini
├── Dockerfile
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
└── app/
    ├── api/
    │   └── router.py
    ├── core/
    │   ├── config.py
    │   ├── database.py
    │   └── security.py
    └── modules/
        └── system/
            ├── handlers.py
            ├── models/
            ├── schemas/
            ├── services/
            └── utils/
```

## Architecture Rules

- Use a modular architecture.
- Global infrastructure lives in `app/core/`.
- Application-wide API routing lives in `app/api/router.py`.
- Business modules live in `app/modules/`.

Each module should follow this structure:

```text
module_name/
├── handlers.py
├── models/
├── schemas/
├── services/
├── utils/
└── README.md
```

## Naming Rules

Use clear and boring names.

Preferred names:

- `handlers.py` for FastAPI routers and endpoints
- `services/` for business logic
- `schemas/` for Pydantic schemas
- `models/` for SQLAlchemy models
- `utils/` for small helper functions

Avoid:

- Putting business logic inside handlers
- Putting database queries directly inside endpoints
- Creating large mixed-purpose files
- Using unclear abbreviations

## FastAPI Rules

- Every module may expose its own router from `handlers.py`.
- The central router in `app/api/router.py` should include module routers.

Example module router:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/health")
async def health_check():
    return {"status": "ok"}
```

Example central router:

```python
from fastapi import APIRouter

from app.modules.system.handlers import router as system_router

api_router = APIRouter()
api_router.include_router(system_router)
```

## Configuration Rules

- Application settings are stored in `app/core/config.py`.
- Settings must be loaded from the `.env` file in the project root.
- Use `pydantic-settings`.
- If you add a new environment variable or runtime setting, update `app/core/config.py` explicitly by adding the corresponding `MainSettings` field and, if needed, its default value.
- Do not hardcode secrets, database credentials, tokens, or passwords in source code.

Use this pattern:

```python
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class MainSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = "FastAPI Template"
    debug: bool = True
    database_url: str


settings = MainSettings()
```

## Database Rules

- Use async SQLAlchemy.
- Database connection logic belongs in `app/core/database.py`.
- Use `settings.database_url`.
- Do not create database engines inside modules.
- Do not create sessions manually inside endpoint functions. Use dependencies.

## Alembic Rules

- Alembic is used for database migrations.
- Migration files live in `alembic/versions/`.
- Models should be imported into Alembic metadata carefully so autogeneration can detect them.
- Never manually edit existing migrations unless explicitly asked.
- Create new migrations for schema changes.
- When working with database models, create migrations exclusively with `uv run alembic revision --autogenerate -m "..."`.

## Code Style

Use Python 3.12+ style where possible.

Prefer:

- Type hints
- Async endpoints
- Explicit imports
- Small functions
- Clear names
- Simple architecture

Avoid:

- Hidden magic
- Global mutable state
- Circular imports
- Business logic in routers
- Unnecessary abstractions

## Package Manager

This project uses `uv`.

Use:

- `uv add package-name`
- `uv run command`

Do not use `pip install` unless explicitly requested.

## Common Commands

Install dependencies:

```bash
uv sync
```

Run app locally:

```bash
uv run uvicorn main:app --reload
```

Run Alembic migration:

```bash
uv run alembic upgrade head
```

Create Alembic revision:

```bash
uv run alembic revision --autogenerate -m "message"
```

## Safety Rules

Before making changes:

- Inspect the relevant files
- Explain the intended change briefly
- Prefer minimal edits
- Do not rewrite large parts of the project without need
- Do not delete files unless explicitly instructed
- Do not modify `.env`
- If a change introduces new configuration, update `app/core/config.py` together with the related docs and `.env.example`.
- Do not commit secrets

When uncertain, choose the simplest maintainable solution.
