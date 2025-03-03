---
title: "Lesson 2: Set up the Dagster project"
module: 'dagster_testing'
lesson: '2'
---

# Set up the Dagster project

After downloading the Dagster University project, you’ll want to navigate to that project to install the necessary python packages.

{% callout %}
💡 **Heads up!** We strongly recommend installing the project dependencies inside a Python virtual environment. If you need a primer on virtual environments, including creating and activating one, check out this [blog post](https://dagster.io/blog/python-packages-primer-2).
{% /callout %}

Then, run the following in the command line to rename the `.env.example`  file and install the dependencies:

```bash
cd dagster-and-dbt
cp .env.example .env
pip install -e ".[dev]"
```

The `e` flag installs the project in editable mode so you can modify existing Dagster assets without having to reload the code location. This allows you to shorten the time it takes to test a change. However, you’ll need to reload the code location in the Dagster UI when adding new assets or installing additional dependencies.
