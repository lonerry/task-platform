FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml ./

RUN /root/.local/bin/uv sync --no-dev --no-managed-python

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]
