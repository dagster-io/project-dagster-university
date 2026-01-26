FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm
ENV PYTHONUNBUFFERED 1

# Remove Yarn repository to avoid expired GPG key issues
# This repository is pre-configured in the base image but has an expired key
# Remove both the sources list and any GPG keys
RUN rm -f /etc/apt/sources.list.d/yarn.list* 2>/dev/null || true && \
    rm -f /etc/apt/trusted.gpg.d/yarn* 2>/dev/null || true && \
    rm -f /usr/share/keyrings/yarn* 2>/dev/null || true

COPY --from=ghcr.io/astral-sh/uv:0.6.10 /uv /bin/uv

COPY dagster_university/dagster_testing /workspace
WORKDIR /workspace

RUN uv pip install -r pyproject.toml --system
