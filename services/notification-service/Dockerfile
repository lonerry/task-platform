FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml ./
RUN /root/.local/bin/uv sync --no-dev --no-managed-python

COPY src ./src

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["/root/.local/bin/uv", "run", "python", "src/main.py"]