---
title: 'Lesson 5: Code locations'
module: 'dagster_testing'
lesson: '5'
---

We have covered how to test everything within a definition. But your Dagster project may have multiple definitions deployed across multiple code locations. Each of these code locations will have their own Python dependencies and may be running different versions of Python and Dagster.

Your tests should be tailored to your specific code location but your CI will depend in how you organization your code. There is no correct answer if your Dagster code should exist as a single repository or be broken up across multiple repositories but your CI might look like the following. 

## Multi Repo

![Multi Repo](/images/dagster-testing/lesson-5/multi-repo.png)

If you have a dedicated repository for each code location. You will likely have a single place where Python dependencies are defined and a single suite of tests to run.

If you use a build system like Github Action to execute your tests, the action might look like this in a multi repo:

```yaml
name: dagster-example-action

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install uv and set the python version
        uses: astral-sh/setup-uv@v5

      - name: Sync dependencies
        run: uv sync

      - name: Pytest
        run: uv run pytest -v
```

The code above:

1. Checks out the code
2. Set `uv` for use within the Github Action
3. Install the necessary Python dependencies using `uv`
4. Executes the tests for the code location


## Monorepo

![Mono Repo](/images/dagster-testing/lesson-5/monorepo.png)

In a monorepo, the various code locations likely exist within different directories in the main project. Each of these directories will contain environment configurations specific to the code location and must be run separately.

The Github Action for a monorepo would be very similar though the python dependencies would be installed at the directory level for each code location and the tests would be executed within each directory:

```yaml
name: dagster-example-action

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install uv and set the python version
        uses: astral-sh/setup-uv@v5

      - name: Sync dependencies
        working-directory: "CODE LOCATION DIRECTORY"
        run: uv sync

      - name: Pytest
        working-directory: "CODE LOCATION DIRECTORY"
        run: uv run pytest -v
```