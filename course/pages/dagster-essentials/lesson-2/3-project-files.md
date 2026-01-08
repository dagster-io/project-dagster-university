---
title: 'Lesson 2: Project files'
module: 'dagster_essentials'
lesson: '3'
---

# Project files

Let’s talk a bit about the files in the Dagster Essentials course. The `dagster_university/dagster_essentials` directory should look something like this:

```bash
dagster_university/dagster_essentials
.
├── .env
├── dagster_cloud.yaml
├── data
├── Makefile
├── pyproject.toml
├── pytest.ini
├── README.md
├── src
│   └── dagster_essentials
│       ├── __init__.py
│       ├── completed
│       ├── definitions.py
│       └── defs
│           ├── __init__.py
│           └── assets
│               ├── __init__.py
│               └── constants.py
├── tests
└── uv.lock
```

**We’re only going to touch on a handful of files for now**, but later lessons will go over additional files in more detail.

The columns in the following table are as follows:

- **File/Directory -** The name of the file/directory
- **Context** - The reason the file/directory is in the project. Indicates that the file/directory is:
  - **Dagster -** Found in every Dagster project
  - **Dagster U** - Specifically for the project you will build during Dagster University
  - **Python** - Highly recommended as software engineering and Python best practices, but not technically required by Dagster
- **Description** - A description of what the file/directory contains or what it’s used for

{% table %}

- File/Directory {% width="20%" %}
- Context {% width="10%" %}
- Description

---

- `README.md`
- Python
- A description and starter guide for the Dagster project.

---

- `dagster_essentials/`
- Dagster U
- Contains the files we will be working with during the course.

---

- `src/dagster_essentials/completed/`
- Dagster U
- Finished code for each lesson of the course.

---

- `src/tests/`
- Dagster U
- A Python module that contains unit tests for the completed code.

---

- `data/`
- Dagster U
- This directory (and directories within it) is where you’ll store the data assets you’ll make during this course. In production settings, this could be Amazon S3 or a data warehouse.

---

- `.env`
- Python
- A text file containing pre-configured environment variables. We’ll talk more about this file in Lesson 6, when we cover connecting to external services.

---

- `pyproject.toml`
- Python
- A file that specifies package core metadata in a static, tool-agnostic way. This file includes a `tool.dagster` section which references the Python module with your Dagster definitions defined and discoverable at the top level. This allows you to use the `dagster dev` command to load your Dagster code without any parameters.

---

- `pytest.ini`
- Python
- The pytest.ini file is a configuration file for pytest that allows you to define test settings, such as command-line options, markers, and plugin configurations.

---

- `uv.lock`
- Python
- In Python, `uv.lock` is a file used by the package manager uv to lock dependencies, similar to `poetry.lock` or `requirements.txt`, ensuring reproducible installations.

{% /table %}

For more info about the other files in your Dagster project, check out the [Project file reference in the Dagster Docs](https://docs.dagster.io/guides/understanding-dagster-project-files).
