---
title: "Lesson 2: Set up local"
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

After cloning the Dagster University project, you’ll want to navigate to specific course within the repository. All courses are within the `dagster_university`.

For example if you are completing "Dagster Essentials" you would change into that directory:

```bash
cd dagster_university/dagster_essentials
```

## Install the dependencies

**uv**

To install the python dependencies with [uv](https://docs.astral.sh/uv/). While in the course specific directory run the following:

```bash
uv sync
```

This will create a virtual environment and install the required dependencies. To enter the newly created virtual environment:

| OS | Command |
| --- | --- |
| MacOS | ```source .venv/bin/activate ``` |
| Windows | ```.venv\Scripts\activate ``` |

---

**pip**

To install the python dependencies with [pip](https://pypi.org/project/pip/).  While in the course specific directory run the following:

```bash
python3 -m venv .venv
```

This will create a virtual environment. To enter the newly created virtual environment:

| OS | Command |
| --- | --- |
| MacOS | ```source .venv/bin/activate ``` |
| Windows | ```.venv\Scripts\activate ``` |

To install the required dependencies:

```bash
pip install -e ".[dev]"
```

---

## Create .env file

You will want to make a copy of the example file `.env.example` which will be used later on.

```bash
cp .env.example .env
```
