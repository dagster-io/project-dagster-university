FROM mcr.microsoft.com/devcontainers/python:3.11
ENV PYTHONUNBUFFERED 1

COPY --from=ghcr.io/astral-sh/uv:0.4.7 /uv /bin/uv

COPY pyproject.toml /opt/dagster/
RUN uv pip install -r pyproject.toml --system

COPY . .