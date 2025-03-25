---
title: "Lesson 2: Set up local"
module: 'dagster_dbt'
lesson: '2'
---

# Set up local

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
cd dagster_university/dagser_and_dbt
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

**pip**

Create the virtual environment.

```bash
python3 -m venv .venv
```

Enter the virtual environment.

```bash
source .venv/bin/activate
```

Install the packages.

```bash
pip install -e ".[dev]"
```

## Create .env file

You will want to copy make a copy of the example file `.env.example` which will be used later on.

```bash
cp .env.example .env
```