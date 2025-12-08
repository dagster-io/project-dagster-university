FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye
ENV PYTHONUNBUFFERED 1

COPY --from=ghcr.io/astral-sh/uv:0.6.10 /uv /bin/uv

COPY dagster_university/dagster_testing /workspace
WORKDIR /workspace

RUN uv pip install -r pyproject.toml --system
