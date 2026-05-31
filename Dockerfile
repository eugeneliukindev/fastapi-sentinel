FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/app

WORKDIR /app

COPY pyproject.toml uv.lock ./


FROM base AS app

RUN uv export --frozen --no-default-groups --no-emit-project | uv pip install --system -r -

COPY src ./src

EXPOSE 8000
CMD ["fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]


FROM base AS migration

RUN uv export --frozen --only-group migration --no-emit-project | uv pip install --system -r -

COPY src ./src
COPY migrations ./migrations

CMD ["alembic", "--config", "pyproject.toml", "upgrade", "head"]
