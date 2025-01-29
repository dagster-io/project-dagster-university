# Example Module

Use this template when creating a new Dagster University module.

## Steps

### 1. Configure the code example

Modules are named `dagster_{module name}` and contain a directory of the code for each lesson of the module:

```bash
dagster_essentials
├── __init__.py
├── lesson_1
│   ├── __init__.py
│   ├── assets
│   │   └── trips.py
│   └── definitions.py
```

A Dagster University module will contain code for module as it evolves over each lesson. The `pyproject.toml` should be configured so `dagster dev` launches the  the finished project once it is completed.

Each lesson should include tests to ensure that all parts of the project work as expected.

### 2. Add an necessary dependencies

Within the new module directory. Set any necessary dependencies in the `pyproject.toml`. The dev dependencies required for the templated GHA (see below) are already included.

### 3. Add GHA

To ensure that the code is properly tested and linted, add a GHA yaml to the `.github/workflows`. There is a template GHA that will perform all the necessary validation, you will only need to set the working directory of the new module.
