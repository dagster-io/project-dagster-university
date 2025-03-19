# [WIP] ETL with Dagster

> [!NOTE]  
> This module is currently a work in progress and is not live as a course yet.

Code for all lessons for all the [Dagster for ETL]() course.

## Getting started

Use `uv` to install the necessary Python dependencies.

```bash
uv sync
```

Most of this module is based around running pytest

Then, start the Dagster UI web server:

```bash
dagster dev -m dagster_and_etl.completed.lesson_{LESSON NUMBER}.definitions
```

Open http://localhost:3000 with your browser to see the project.

## Development

### Tests
To run tests, use `pytest`. To run all the tests for all lesson run:

```bash
pytest dagster_and_etl_tests
```

### Linting
To run linting, use `ruff`.

```bash
ruff check . --select I --fix
```

The Github Action will check for errors with ruff.