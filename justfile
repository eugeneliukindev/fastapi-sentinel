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

psql:
    just dc exec -it db psql -U {{env("MY_APP__DB__USERNAME")}} -d {{env("MY_APP__DB__NAME")}}

alembic *args:
    uv run alembic {{args}}

er:
    uv run --group docs python scripts/generate_er.py
