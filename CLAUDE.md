# Dagster University

An educational platform with two independent parts: Dagster course projects (Python) and a course-content web app (Next.js).

## Repository structure

```
course/                          # Next.js/Markdoc web app (courses.dagster.io)
    pages/
        dagster_essentials/      # Course: Dagster fundamentals
        dagster_and_dbt/         # Course: Dagster + dbt
        dagster_and_etl/         # Course: ETL pipelines
        ...
dagster_university/
    dagster_essentials/          # Course: Dagster fundamentals
    dagster_and_dbt/             # Course: Dagster + dbt
    dagster_and_etl/             # Course: ETL pipelines
    ...
```

## Working on a Dagster course

Each course is an **independent Python project** — there is no root-level Python environment. Always `cd` into the course directory first.

**Package manager:** `uv` (never `pip` or `poetry`)

```bash
cd dagster_university/<course_name>

uv sync                                   # install dependencies
uv run dg dev                             # launch Dagster UI
uv run pytest tests -p no:warnings        # run tests
uv run ruff check                         # lint
```

### Course project layout

```
src/<course_name>/
    definitions.py        # root Definitions object
    defs/
        assets/           # asset definitions
    completed/            # reference implementations per lesson — do not modify
        lesson_4/         # matches lesson 4 of the content in course/pages/course_name
                          # completed lessons only correspond to pages/ that have code 
            defs/
        lesson_5/
            defs/
        ...
tests/
```

The `completed/` directory contains the finished code for each lesson. It exists for student reference, treat it as read-only. The root defs/ directory is the student's working area for the course.

## Working on the web app

Course content is written in Markdoc (`.md` files under `course/pages/`).

**Package manager:** `yarn` (v4.5.0)

```bash
cd course

yarn dev          # local dev server
yarn build        # production build
yarn lint         # ESLint
yarn linkcheck    # validate internal and external links
yarn prettier     # format all files
```

## Running all course tests

```bash
make test_all     # from repo root — runs pytest for all courses
```

## CI

Each course has GitHub Actions workflows that run `uv sync` → `ruff check` → `pytest` on Ubuntu and Windows across Python 3.10–3.13.
