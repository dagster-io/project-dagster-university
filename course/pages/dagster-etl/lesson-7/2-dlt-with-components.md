---
title: "Lesson 7: dlt with Components"
module: 'dagster_etl'
lesson: '7'
---

# dlt with Components

To navigate including Components with Dagster, we will be using the Dagster `dg` command line. `dg` is a useful to initializing and navigating Dagster projects. Because we have been working the virtual envionment and project structure of this course we have not needed `dg` as much.

We used `dg` before to lanuch the UI to view and execute our assets but now we will use it to scaffold our Component.

To start run:

```bash
dg list plugins
```

This will list all the plugins available in our Dagster project. At the bottom of that output you should see a plugin for for `dagster_dlt.DltLoadCollectionComponent`.
```

```
│ dagster_dlt   │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓ │
│               │ ┃ Symbol                                 ┃ Summary            ┃ Features            ┃ │
│               │ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩ │
│               │ │ dagster_dlt.DltLoadCollectionComponent │ Expose one or more │ [component,         │ │
│               │ │                                        │ dlt loads to       │ scaffold-target]    │ │
│               │ │                                        │ Dagster as assets. │                     │ │
│               │ └────────────────────────────────────────┴────────────────────┴─────────────────────┘ │
```

The dlt component is available to use because our Python environment has the `dagster-dlt` package installed (and that we used in the previous lesson). If we were starting our project from scratch we could add the plugin by adding it to our Python envrionment.

```bash
uv pip install dagster-dlt
```

But we have everything we need so we can start using the Component.

## Create dlt Component

To initialize our dlt Component, we just need 

```bash
dg scaffold dagster_dlt.DltLoadCollectionComponent ingestion --source sql_database --destination duckdb
```

# TODO: After dg dlt works with sql_database