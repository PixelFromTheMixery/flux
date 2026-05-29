# --- Stage 1: Build ---
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev \
    && if [ -d "/.venv" ]; then mv /.venv /app/.venv || true; fi

# --- Stage 2: Runtime ---
FROM python:3.14-slim

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV IP_ADDR=0.0.0.0
ENV IP_PORT=8000

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY --chown=1000:1000 app/ ./app/
COPY --chown=1000:1000 settings.yaml ./

RUN useradd --system --create-home --home-dir /home/appuser --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:create_app --factory --host $IP_ADDR --port $IP_PORT"]