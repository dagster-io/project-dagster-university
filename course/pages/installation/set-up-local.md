---
title: "Lesson 2: Set up local"
lesson: '2'
---

# Set up local

This will set up Dagster for you local machine. If you would prefer to do this course in Github Codespaces, please follow [that guide](/dagster-essentials/lesson-2/2-set-up-codespace).

- **To install git.** Refer to the [Git documentation](https://github.com/git-guides/install-git) if you don’t have this installed.
- **To have Python installed.**  Dagster supports Python 3.9 - 3.12 (3.12 recommended).
- **To install a package manager**. To manage the python packages, we recommend [`uv`]((https://docs.astral.sh/uv/)) which Dagster uses internally.

---

## Clone the Dagster University project

[Clone the Github repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). The command will depend on if you choose to clone with [ssh or https](https://graphite.dev/guides/git-clone-ssh-vs-https):

| Option | Command |
| --- | --- |
| ssh | ```git clone git@github.com:dagster-io/project-dagster-university.git``` |
| https | ```git clone https://github.com/dagster-io/project-dagster-university.git``` |

After cloning the Dagster University project, navigate to the specific course directory within the repository. All courses are located inside the `dagster_university` folder.

For example, if you are completing "Dagster Essentials", change into that directory:

```bash
cd dagster_university/dagster_essentials
```

## Install uv and dg

Now we want to install `dg`. This is the command line interface that makes it easy to interact with Dagster. Throughout the course we will use `dg` to scaffold our project and streamline the development process.

In order to best use `dg` we will need the Python package manager [`uv`](https://docs.astral.sh/uv/). `uv` will allow us to install `dg` globally and more easily build our virtual environments.

If you do not have `uv` instead already, you can do so with:

```bash
brew install uv
```

## Install the dependencies

To install the python dependencies with [uv](https://docs.astral.sh/uv/). While in the course specific directory run the following:

```bash
uv sync
```

This will create a virtual environment and install the required dependencies. To enter the newly created virtual environment:

| OS | Command |
| --- | --- |
| MacOS | ```source .venv/bin/activate``` |
| Windows | ```.venv\Scripts\activate``` |

---

**pip**

To install the python dependencies with [pip](https://pypi.org/project/pip/).  While in the course specific directory run the following:

```bash
python3 -m venv .venv
```

This will create a virtual environment. To enter the newly created virtual environment:

| OS | Command |
| --- | --- |
| MacOS | ```source .venv/bin/activate``` |
| Windows | ```.venv\Scripts\activate``` |

To install the required dependencies:

```bash
pip install -e ".[dev]"
```