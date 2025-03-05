# Dagster and dbt

Code for all lessons for all the [Dagster and dbt](https://courses.dagster.io/courses/dagster-dbt) course.

## Getting started

Use `uv` to install the necessary Python dependencies.

```bash
uv sync
```

Duplicate the `.env.example` file and rename it to `.env`. Then, fill in the values for the environment variables in the file.

Then, start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

> [!NOTE]
> Running `dagster dev` will put you in the finished Dagster project (at the final lesson). To see any of the other lessons run:
> `dagster dev -m dagster_and_dbt.lesson_{LESSON NUMBER}.definitions`

## Development

### dbt Project

Each lesson contains a specific dbt project. This is because the dbt project changes slightly over the course.

### Tests
To run tests, use `pytest`.

```bash
pytest dagster_and_dbt_tests
```

The Github Action will execute all tests for this module using all supported Python versions and OS.

### Linting
To run linting, use `ruff`.

```bash
ruff check . --select I --fix
```

The Github Action will check for errors with ruff.

## Deploy on Dagster Cloud

The easiest way to deploy your Dagster project is to use Dagster Cloud.

Check out the [Dagster Cloud Documentation](https://docs.dagster.cloud) to learn more. 