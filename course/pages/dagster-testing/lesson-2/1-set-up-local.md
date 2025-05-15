---
title: "Lesson 2: Set up local"
module: 'dagster_testing'
lesson: '2'
---

# Set up local

This will set up Dagster for you local machine. If you would prefer to do this course in Github Codespaces, please follow [that guide](/dagster-testing/lesson-2/2-set-up-codespace).

- **To install git.** Refer to the [Git documentation](https://github.com/git-guides/install-git) if you don’t have this installed.
- **To have Python installed.**  Dagster supports Python 3.9 - 3.12.
- **To install a package manager**. To manage the python packages, we recommend [`uv`]((https://docs.astral.sh/uv/)) which Dagster uses internally.

---

## Clone the Dagster University project

[Clone the Github repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). The command will depend on if you choose to clone with [ssh or https](https://graphite.dev/guides/git-clone-ssh-vs-https).

**ssh**

```bash
git clone git@github.com:dagster-io/project-dagster-university.git
```

**https**

```bash
git clone https://github.com/dagster-io/project-dagster-university.git
```

After cloning the Dagster University project, you’ll want to navigate to specific course within the repository.

```bash
cd dagster_university/dagster_testing
```

## Install uv and dg

Now we want to install `dg`. This is the command line interface that makes it easy to interact with Dagster. Throughout the course we will use `dg` to scaffold our project and streamline the development process.

In order to best use `dg` we will need the Python package manager [`uv`](https://docs.astral.sh/uv/). `uv` will allow us to install `dg` globally and more easily build our virtual environments.

If you do not have `uv` instead already, you can do so with:
```bash
brew install uv
```

Now you can use `uv` to install `dg` globally:
```bash
uv tool install dagster-dg
```

## Install the dependencies

With `uv` and `dg` set, we can create the virtual environment specific to this course. All of the dependencies are maintained in the `pyproject.toml` (you will not need to edit anything in that project for this course). To create the virtual environment, run:
```bash
uv sync
```

This will create a virtual environment and install all the necessary dependencies. To activate this virtual environment:

```bash
source .venv/bin/activate
```

To ensure everything is working you can launch the Dagster UI.

```bash
dg dev
```