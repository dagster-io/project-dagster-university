---
title: "Lesson 2: Set up local"
module: 'dagster_testing'
lesson: '2'
---

# Set up local

- **To install git.** Refer to the [Git documentation](https://github.com/git-guides/install-git) if you don’t have this installed.
- **To have Python installed.**  Dagster supports Python 3.9 - 3.12.
- **To install a package manager**. To manage the python packages, we recommend [`uv`]((https://docs.astral.sh/uv/)) which Dagster uses internally.

---

## Clone the Dagster University project

Run the following to clone the project.

```bash
git clone git@github.com:dagster-io/project-dagster-university.git
```

After cloning the Dagster University project, you’ll want to navigate to specific course within the repository.

```
cd dagster_university/dagster_testing
```

## Install the dependencies

**uv**

To install the python dependencies with [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

This will create a virtual environment that you can now use.

```bash
source .venv/bin/activate
```
