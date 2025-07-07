---
title: 'Lesson 6: Projects'
module: 'dagster_testing'
lesson: '6'
---

# Projects

We have covered how to test everything within a definition. Now we will zoom out and discuss how to test the multiple definitions that make up a platform.

Each definition has will be tied to a unique project and will have its own Python dependencies. It is important that your tests are tailored to that project. Part of a mature Dagster deployment is configuring your CI (continuous integration) process to run your tests. How to properly configure that will depend on how the code is organized and if you are using a single repository for all of your projects (monorepo) or a repository for each project (multi repo).

## Monorepo

![Mono Repo](/images/dagster-testing/lesson-6/monorepo.png)

In a monorepo, the different projects exist within different directories of the main project. Each of these directories will contain environment configurations specific to the project and must be run separately.

Your CI build system will need build the Python environments separately and execute the tests specific to that directory in the given environment.

If you use a build system like Github Action to execute your tests, the step by step process might look like this.

```yaml
name: dagster-example-action

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        code-locations-dir:
          - code_location_1
          - code_location_2
          - code_location_3

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install uv and set the python version
        uses: astral-sh/setup-uv@v5

      - name: Sync dependencies
        working-directory: ${{ matrix.code-locations-dir }}
        run: uv sync

      - name: Pytest
        working-directory: ${{ matrix.code-locations-dir }}
        run: uv run pytest -v
```

The code above:

1. Sets a list of all the projects within the monorepo.
2. Checks out the code for the entire repo.
3. Sets `uv` for use within the Github Action.
4. For each project, install the necessary Python dependencies using `uv`.
5. For each project, execute the tests for that project.

## Multi Repo

![Multi Repo](/images/dagster-testing/lesson-6/multi-repo.png)

In a multi repository, there will be a single environment as the entire repository is dedicated to a single project. This usually means there is only one place where Python dependencies are set and only one testing suite.

In Github Actions, the set up will look very similar to a monorepo though we only need to run everything for the single project.

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

1. Checks out the code for the entire repo.
2. Set `uv` for use within the Github Action.
3. Install the necessary Python dependencies using `uv`.
4. Executes the tests for the project.
