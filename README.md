# fastapi-sentinel

Production-ready FastAPI template with async SQLAlchemy, JWT authentication (RS256), role-based access control, and a clean layered architecture. Use it as a starting point for any API that needs auth and permissions out of the box.

## Stack

| Layer | Library |
|---|---|
| Web | FastAPI |
| ORM | SQLAlchemy 2 (async) |
| Database | PostgreSQL 18 via asyncpg |
| Migrations | Alembic |
| IoC / DI | Dishka |
| Auth | PyJWT (RS256), pwdlib (Argon2) |
| Validation | Pydantic v2 |
| Config | pydantic-settings |

## Features

- **JWT auth** — asymmetric RS256 keys; access token (15 min) + refresh token (30 days) with per-token blacklist
- **RBAC** — static roles and permissions defined as `StrEnum`s, seeded via Alembic data migration; `require_role` / `require_any_role` / `require_permission` / `require_any_permission` FastAPI dependencies
- **Unit of Work** — single `UnitOfWork` wraps all repositories behind one `async with` session
- **Generic repository** — `BaseRepository[Model, InsertDTO, UpdateDTO]` with `get_by_id`, `get_all`, `insert`, `update`, `delete`
- **ER diagram** — auto-generated `docs/er_diagram.png` via eralchemy; pre-commit hook regenerates it on model changes

## RBAC model

| Role | Permissions |
|---|---|
| `user` | `users:read` |
| `admin` | `users:read` · `users:create` · `users:update` · `users:delete` |

New roles and permissions are added by extending `RoleEnum` / `PermissionEnum` and writing a data migration. `src/utils/mappings.py` documents the role → permission matrix.

## Project structure

```
src/
├── api/v1/          # routers: auth, users, rbac
├── services/        # business logic
├── repo/            # repository layer
├── models/          # SQLAlchemy ORM models
├── schemas/         # Pydantic request/response schemas
├── dto/             # internal data transfer objects
├── enums/           # RoleEnum, PermissionEnum, TokenType
├── exceptions/      # domain exceptions
├── ioc/             # Dishka providers (container wiring)
├── core/            # UnitOfWork
└── config.py        # pydantic-settings
```

## Getting started

### 1. Generate RS256 key pair

```bash
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

### 2. Create `.env`

```dotenv
MY_APP__DB__USERNAME=postgres
MY_APP__DB__PASSWORD=postgres
MY_APP__DB__NAME=sentinel
MY_APP__DB__HOST=localhost
MY_APP__DB__PORT=5432

MY_APP__APP__JWT__PRIVATE_KEY="$(cat private.pem)"
MY_APP__APP__JWT__PUBLIC_KEY="$(cat public.pem)"
```

### 3. Run with Docker Compose

```bash
just dc up -d --build
```

This starts three services in order: `db` → `migrate` (runs Alembic `upgrade head`) → `app`.

### 4. Local development (without Docker)

```bash
uv sync
just dc up -d db          # only the database
just alembic upgrade head
just run
```

API is available at `http://localhost:8000`. Interactive docs at `/docs`.

## API

### Auth

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/v1/auth/login` | — | Returns access + refresh tokens |
| `POST` | `/v1/auth/refresh` | Bearer (refresh) | Rotates both tokens |
| `POST` | `/v1/auth/logout` | Bearer (refresh) | Blacklists the refresh token |

### Users

| Method | Path | Required | Description |
|---|---|---|---|
| `GET` | `/v1/users/me` | any token | Current user |
| `POST` | `/v1/users` | — | Register |
| `GET` | `/v1/users` | role `admin` | List all users |
| `GET` | `/v1/users/{id}` | perm `users:read` | Get user |
| `PATCH` | `/v1/users/{id}` | perm `users:update` | Update user |
| `DELETE` | `/v1/users/{id}` | perm `users:delete` | Delete user |
| `POST` | `/v1/users/{id}/roles/{role_id}` | role `admin` | Assign role |
| `DELETE` | `/v1/users/{id}/roles/{role_id}` | role `admin` | Revoke role |

### RBAC (read-only)

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/v1/rbac/roles` | any token | List roles |
| `GET` | `/v1/rbac/permissions` | any token | List permissions |

## Auth flow

```
POST /login  →  { access_token, refresh_token }
                        │
              access_token (Bearer) used on every request
                        │
              when expired → POST /refresh  →  new token pair
                        │
              POST /logout  →  refresh_token blacklisted
```

Refresh token rotation: each `/refresh` call blacklists the old token and issues a new pair, preventing reuse.

## Configuration reference

All settings use the `MY_APP__` prefix with `__` as the nested delimiter.

| Variable | Default | Description |
|---|---|---|
| `MY_APP__DB__USERNAME` | — | Postgres user |
| `MY_APP__DB__PASSWORD` | — | Postgres password |
| `MY_APP__DB__NAME` | — | Database name |
| `MY_APP__DB__HOST` | `localhost` | Postgres host |
| `MY_APP__DB__PORT` | `5432` | Postgres port |
| `MY_APP__APP__JWT__PRIVATE_KEY` | — | RS256 private key (PEM) |
| `MY_APP__APP__JWT__PUBLIC_KEY` | — | RS256 public key (PEM) |
| `MY_APP__APP__JWT__ACCESS_TTL` | `PT15M` | Access token lifetime |
| `MY_APP__APP__JWT__REFRESH_TTL` | `P30D` | Refresh token lifetime |

## Development

```bash
just run          # start dev server with hot reload
just lint         # ruff check + format check
just fmt          # ruff autofix + format
just typecheck    # mypy strict
just test         # pytest
just er           # regenerate docs/er_diagram.png
just alembic revision --autogenerate -m "description"
just alembic upgrade head
```

Pre-commit hooks run ruff and regenerate the ER diagram automatically when `src/models/__init__.py` changes. Install once with:

```bash
uv run pre-commit install
```

## ER diagram

![ER diagram](docs/er_diagram.png)
