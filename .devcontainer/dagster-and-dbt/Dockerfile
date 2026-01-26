FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm
ENV PYTHONUNBUFFERED 1

COPY --from=ghcr.io/astral-sh/uv:0.6.10 /uv /bin/uv

COPY dagster_university/dagster_and_dbt /workspace
WORKDIR /workspace

RUN uv pip install -r pyproject.toml --system