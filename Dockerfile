FROM ghcr.io/astral-sh/uv:0.13.4 AS uv-bin

FROM python:3.14-slim-bookworm AS dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=uv-bin /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project --no-cache

FROM python:3.14-slim-bookworm
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --user-group --no-create-home daridict

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=daridict.settings.docker
WORKDIR /app
COPY --from=dependencies /app/.venv /app/.venv
COPY manage.py ./
COPY daridict ./daridict
COPY dict ./dict
COPY home ./home
COPY --chmod=755 container/daridict.sh /usr/local/bin/daridict

USER daridict
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/daridict"]
CMD ["serve"]
