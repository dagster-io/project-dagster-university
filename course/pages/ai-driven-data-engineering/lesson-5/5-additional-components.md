---
title: "Lesson 5: Additional components"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Additional components

The transformation layer is in place, but dbt likely not the only integration you use in your data platform. Suppose you also need to get data out of DuckDB and into the systems downstream consumers actually use. In this case, you want to export the data from `fct_orders` to S3 as a Parquet file.

You could write a one-off asset that runs a DuckDB query and uploads the result to S3. It would work. But you'd rather use a proper replication path that handles the mechanics cleanly and gives you a Component layout that's consistent with the rest of the project. The `dagster-expert` skill can help you figure out what that looks like.

## Asking the agent for options

When you're not sure which integration to use, just ask:

```text
/dagster-expert I would like to export the data from the fct_orders model to S3. What are some good open-source tools that can handle this with Dagster?
```

Rather than the agent returning code, it will share thoughts on possible solutions:

```text
For exporting from DuckDB to S3, there are two strong open-source options with first-class
  Dagster support:

  ---
  Sling (dagster-sling) — Recommended for this use case

  Sling is purpose-built for data replication between databases and file systems, including
  DuckDB → S3. It's the most direct fit here.

  - Reads directly from DuckDB and writes to S3 as CSV, Parquet, JSON, etc.
  - Component-based Dagster integration with a simple YAML config
  - Low complexity, high performance
  - Open-source CLI tool

  # replication config example
  source: DUCKDB
  target: S3

  streams:
    main.fct_orders:
      object: s3://my-bucket/exports/fct_orders.parquet
      mode: full-refresh

  ---
  dlt (dagster-dlt) — Best if you need schema evolution or incremental loads

  dlt is a Python-native EL library that handles schema inference, incremental state, and
  normalization. It supports DuckDB as a source and S3 as a destination.

  - More code-centric than Sling (Python-based pipeline definitions)
  - Strong incremental loading with built-in state management
  - Good fit if the export logic needs transformation or filtering in Python
  - Open-source

  ---
  Quick comparison for your case

  ┌─────────────────────┬─────────────────┬─────────────────┐
  │                     │      Sling      │       dlt       │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ DuckDB → S3         │ ✅ Native       │ ✅ Supported    │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ Config style        │ YAML            │ Python          │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ Incremental         │ ✅              │ ✅ Strong       │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ Complexity          │ Low             │ Medium          │
  ├─────────────────────┼─────────────────┼─────────────────┤
  │ Dagster integration │ Component-based │ Component-based │
  └─────────────────────┴─────────────────┴─────────────────┘

  Recommendation: Start with Sling — it's the least overhead for a straightforward DuckDB → S3
   export and integrates cleanly as a Dagster component alongside your existing dbt setup.
  Would you like to implement one of these?
```

This is the expert skill doing what it's designed for: you described the goal, and it narrowed the decision space to two well-supported options with a concrete recommendation. You didn't have to know that [Sling](https://slingdata.io/) or [dlt](https://dlthub.com/context/) existed.

## Setting up the Sling component

Based on the agent's recommendation, we can try Sling. Ask your agent to include Sling and export the fct_orders table to S3:

```text {% obfuscated="true" %}
/dagster-expert Setup a Sling component that exports the DuckDB data from fct_orders to S3 (assume the bucket is called test-bucket).
```

This workflow should be familiar now. The agent manages the dependency, scaffolds the Component, and configures the replication before confirming that everything is successful:

```bash
uv add dagster-sling
```

```bash
dg scaffold defs dagster_sling.SlingReplicationCollectionComponent fct_orders_s3_export
```

```bash
dg check defs
```

The Sling Component is similar to the dbt Component but both have their own specific configurations. One difference is that the Sling component requires an additional configuration file for defining the `source` and `target` information. However the agent handles all of this for us and injects the information in the correct places from our prompt.

```yaml
# /src/university/defs/fct_orders_s3_export/replication.yaml
source: DUCKDB
target: S3

streams:
  "main.fct_orders":
    object: "s3://test-bucket/fct_orders.parquet"
    mode: full-refresh
```

## Wiring the dependency

One thing we were not explicit about with our prompt was the dependency for our asset. If you look at the asset catalog you may see the the sling asset is disconnected from the other assets. This is easy enough to fix:

```text {% obfuscated="true" %}
/dagster-expert The parquet asset should have a dependency on the fct_orders asset.
```

The agent wires the dependency. Now the full graph is correct: raw assets → dbt staging → `fct_orders` → S3 Parquet export. You can run the entire pipeline with one command and everything materializes in the right order.

![Asset graph with dbt and Sling export to S3](/images/ai-driven-data-engineering/lesson-5/project-dbt-sling.png)

Open the asset catalog and look at what you've built. This is the complete ELT pipeline from the project preview, built from prompts, without writing a project scaffold or reading the Sling documentation.
