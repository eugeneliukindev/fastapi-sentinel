set dotenv-load := true

run:
    uv run fastapi dev src/main.py

lint:
    uv run ruff check .
    uv run ruff format --check .

fmt:
    uv run ruff check --fix .
    uv run ruff format .

typecheck:
    uv run mypy .

test:
    uv run pytest

check: lint typecheck test

dc *args:
    docker compose {{args}}

migrate message:
    uv run alembic revision --autogenerate -m "{{message}}"

upgrade revision="head":
    uv run alembic upgrade {{revision}}

downgrade revision="-1":
    uv run alembic downgrade {{revision}}
