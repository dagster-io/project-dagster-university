FROM mcr.microsoft.com/devcontainers/python:3.11
ENV PYTHONUNBUFFERED 1

COPY --from=ghcr.io/astral-sh/uv:0.4.7 /uv /bin/uv

RUN uv pip install -r dagster_university/dagster_testing/pyproject.toml --system
