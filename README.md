# FastAPI Template

`fastapi_template` is a modular backend template for services built with:

- FastAPI
- PostgreSQL
- async SQLAlchemy
- Alembic migrations
- Pydantic settings
- `uv` for dependency management

The repository is intentionally small. It gives you a clean foundation for new modules, shared infrastructure, and database-backed APIs without locking you into a specific product domain.

## What Is Included

- Application entrypoint in [main.py](/home/misha/code/module_service/fastapi_template/main.py:1)
- Central API router in [app/api/router.py](/home/misha/code/module_service/fastapi_template/app/api/router.py:1)
- Settings loader in [app/core/config.py](/home/misha/code/module_service/fastapi_template/app/core/config.py:1)
- Async database engine and session dependency in [app/core/database.py](/home/misha/code/module_service/fastapi_template/app/core/database.py:1)
- Base infrastructure module in [app/modules/system/README.md](/home/misha/code/module_service/fastapi_template/app/modules/system/README.md:1)
- Alembic configuration for schema migrations in [alembic/env.py](/home/misha/code/module_service/fastapi_template/alembic/env.py:1)

## Current Scope

The template already covers:

- modular project layout;
- settings from `.env`;
- async DB access with pooled connections;
- shared ORM base classes;
- reusable CRUD helpers;
- health-check endpoints.

The following parts are present as placeholders or are intentionally not implemented yet:

- [app/core/security.py](/home/misha/code/module_service/fastapi_template/app/core/security.py:1) is empty;
- [Dockerfile](/home/misha/code/module_service/fastapi_template/Dockerfile:1) is empty;
- there is no dedicated test setup yet.

If you need auth, containerization, or CI-ready tests, treat them as the next layer to add on top of this template.

## Project Structure

```text
fastapi_template/
├── alembic/
├── app/
│   ├── api/
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   └── modules/
│       ├── system/
│       └── <your_module>/
├── main.py
├── pyproject.toml
└── README.md
```

Recommended structure for a business module:

```text
module_name/
├── handlers.py
├── models/
├── schemas/
├── services/
├── utils/
└── README.md
```

## Requirements

- Python 3.11+
- PostgreSQL
- `uv`

Project metadata and runtime dependencies are defined in [pyproject.toml](/home/misha/code/module_service/fastapi_template/pyproject.toml:1).

## Configuration

Settings are loaded by `pydantic-settings` from `.env` in the project root. The loader is configured in [app/core/config.py](/home/misha/code/module_service/fastapi_template/app/core/config.py:9).

Example environment file:

```env
debug=true
database_url=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_template
database_pool_size=5
database_max_overflow=10
database_pool_timeout=30
database_pool_recycle=1800
```

Available settings:

- `project_name`: application title shown by FastAPI; optional, defaults to `"Fast API Template"`.
- `debug`: enables verbose error details in some infrastructure handlers.
- `database_url`: async SQLAlchemy URL, required.
- `database_pool_size`: base connection pool size.
- `database_max_overflow`: extra temporary connections above the base pool.
- `database_pool_timeout`: seconds to wait for a free DB connection.
- `database_pool_recycle`: seconds before recycling pooled connections.

Use [.env.example](/home/misha/code/module_service/fastapi_template/.env.example:1) as the baseline.

## Install And Run

Install dependencies:

```bash
uv sync
```

Run the application locally:

```bash
uv run uvicorn main:app --reload
```

The FastAPI app is created in [main.py](/home/misha/code/module_service/fastapi_template/main.py:17). On shutdown it disposes the shared SQLAlchemy engine through the `lifespan` hook.

## API Layout

The central API router uses the `/api` prefix in [app/api/router.py](/home/misha/code/module_service/fastapi_template/app/api/router.py:6).

Infrastructure endpoints currently available:

- `GET /api/system/health`
- `GET /api/system/health/db`

The system router is implemented in [app/modules/system/handlers.py](/home/misha/code/module_service/fastapi_template/app/modules/system/handlers.py:11).

## Database And Sessions

The shared database object is created in [app/core/database.py](/home/misha/code/module_service/fastapi_template/app/core/database.py:46).

Important behavior:

- one async engine is created for the app process;
- request handlers should consume `AsyncSession` through `Depends(database.get_session)`;
- if an exception escapes the dependency scope, the session is rolled back automatically;
- low-level SQLAlchemy errors are normalized by the infrastructure error handler used in the `system` module CRUD layer.

## Migrations

Alembic is configured for async SQLAlchemy in [alembic/env.py](/home/misha/code/module_service/fastapi_template/alembic/env.py:1).

Apply all migrations:

```bash
uv run alembic upgrade head
```

Create a new migration after schema changes:

```bash
uv run alembic revision --autogenerate -m "describe change"
```

### Important: How Autogenerate Sees Models

Alembic does not scan the filesystem automatically. It uses `Base.metadata`, which is imported in [alembic/env.py](/home/misha/code/module_service/fastapi_template/alembic/env.py:23) through:

- [app/__init__.py](/home/misha/code/module_service/fastapi_template/app/__init__.py:1)
- [app/modules/__init__.py](/home/misha/code/module_service/fastapi_template/app/modules/__init__.py:1)

When you add a new module with ORM models, make sure its models are imported into that chain. Otherwise Alembic autogenerate will not detect the tables.

## Adding A New Module

When creating a new non-system module, use this checklist:

1. Create the module directory under `app/modules/<module_name>/`.
2. Add `handlers.py`, `models/`, `schemas/`, `services/`, and `README.md`.
3. Define ORM models using `Base` or `Base` + `TimestampMixin` from `app.modules.system`.
4. Export the module models through [app/modules/__init__.py](/home/misha/code/module_service/fastapi_template/app/modules/__init__.py:1) so Alembic can see them.
5. Import and include the module router in [app/api/router.py](/home/misha/code/module_service/fastapi_template/app/api/router.py:3).
6. Generate a migration with Alembic.

Minimal router example:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["example"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
```

Minimal model example:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.system import Base, TimestampMixin


class ExampleEntity(Base, TimestampMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
```

## Working Rules

- Keep business logic in `services/`, not in route handlers.
- Reuse shared infrastructure from `app/core/` and `app/modules/system/`.
- Do not create ad hoc SQLAlchemy engines inside modules.
- Do not hardcode credentials or secrets in source code.
- Prefer explicit imports and small focused files.

## Related Docs

- [app/modules/system/README.md](/home/misha/code/module_service/fastapi_template/app/modules/system/README.md:1)
- [AGENTS.md](/home/misha/code/module_service/fastapi_template/AGENTS.md:1)
