# [WIP] Dagster Testing

> [!NOTE]  
> This module is currently a work in progress and is not live as a course yet.

Code for all lessons for all the [Dagster Testing]() course.

## Getting started

Use `uv` to install the necessary Python dependencies.

```bash
uv sync
```

Most of this module is based around running pytest

Then, start the Dagster UI web server:

```bash
dagster dev -m dagster_testing.lesson_{LESSON NUMBER}.definitions
```

Open http://localhost:3000 with your browser to see the project.

## Development

### Tests
To run tests, use `pytest`. To run all the tests for all lesson run:

```bash
pytest dagster_testing_tests
```

This will include (lesson 4 integration tests) which requires Docker. To not run the integration tests:

```bash
pytest -m "not integration"
```

The Github Action will execute all tests for this module using all supported Python versions and OS.

### Linting
To run linting, use `ruff`.

```bash
ruff check . --select I --fix
```

The Github Action will check for errors with ruff.