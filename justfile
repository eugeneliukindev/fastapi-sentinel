set dotenv-load := true
set fallback := true

[doc("All command information")]
_default:
    @just --list --unsorted --list-heading $'Available commands…\n'

[doc("Start dev server with hot reload")]
[group("infra")]
run:
    uv run fastapi dev src/main.py

[doc("Run docker compose")]
[group("infra")]
dc *args:
    docker compose {{args}}

[doc("Connect to the database via psql")]
[group("infra")]
psql:
    just dc exec -it db psql -U {{env("MY_APP__DB__USERNAME")}} -d {{env("MY_APP__DB__NAME")}}

[doc("Run alembic commands")]
[group("infra")]
alembic *args:
    uv run alembic {{args}}

[doc("Ruff check and format check")]
[group("linter")]
lint:
    uv run ruff check .
    uv run ruff format --check .

[doc("Ruff autofix and format")]
[group("linter")]
fmt:
    uv run ruff check --fix .
    uv run ruff format .

[doc("Mypy strict check")]
[group("static analysis")]
typecheck:
    uv run mypy .

[doc("Run all checks (CI equivalent)")]
[group("ci")]
[parallel]
check: lint typecheck

[doc("Regenerate docs/er_diagram.png")]
[group("docs")]
er:
    scripts/generate_er
