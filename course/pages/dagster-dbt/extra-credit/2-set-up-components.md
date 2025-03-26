---
title: 'Extra credit: What are components?'
module: 'dbt_dagster'
lesson: 'extra-credit'
---

# What are components?

You might be wondering what components are and how they can help with this project. Components provide a structured, opinionated project layout that supports scaffolding in Dagster. They simplify the process by transforming configuration files (like YAML) into Dagster definitions, eliminating unnecessary code. This is especially useful for integrations that follow common patterns—dbt being a great example.

In our dbt project, most of the logic was contained within our SQL models, and the mapping of Dagster onto our project followed a standard approach.

With components, much of the boilerplate code we previously had to write is removed, allowing us to get up and running much faster.

## Setting up components

Components exist in a separate Python package `dagster-dg`. While the core `dagster` package can be specific to a particular code location, `dg` is meant to be installed globally.

### Install dg

If you were using `uv` to manage your virtual environment (`uv` is used if you are running this course with Github Codepsaces) you can include `dagster-dg` with the following command.

```bash
uv tool install dagster-dg
```

You now have everything necessary to run components and we can get started with replacing our existing code with the dbt components.