# Dagster Essentials

Code for all lessons for all the [Dagster Essentials](https://courses.dagster.io/courses/dagster-essentials) course.

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
> `dagster dev -m dagster_essentials.lesson_{LESSON NUMBER}.definitions`
>
> Lessons 3 and 4 do not use a `definition` in the content.

## Development

### Tests
To run tests, use `pytest`.

```bash
pytest dagster_essentials_tests
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
