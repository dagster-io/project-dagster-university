FROM mcr.microsoft.com/devcontainers/python:0-3.11-bullseye
ENV PYTHONUNBUFFERED 1

COPY --from=ghcr.io/astral-sh/uv:0.6.10 /uv /bin/uv

COPY dagster_university/dagster_and_dbt/pyproject.toml .
RUN uv pip install -r pyproject.toml --system