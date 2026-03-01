FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock ./
RUN /root/.local/bin/uv sync --no-dev --frozen --no-managed-python

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]