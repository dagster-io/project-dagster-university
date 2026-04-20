---
title: 'Lesson 7: Using dbt Cloud'
module: 'dbt_dagster'
lesson: '7'
---

# Using dbt Cloud

The course so far has used the dbt CLI (`DbtCliResource`) to run dbt commands locally and in CI/CD. If your team uses dbt Cloud, the setup is different: Dagster connects to dbt Cloud via its API and runs commands through it, rather than invoking a local dbt installation.

This page explains what changes and what stays the same.

---

## How dbt Cloud integration differs

| | dbt CLI (this course) | dbt Cloud |
|---|---|---|
| Decorator | `@dbt_assets` | `@dbt_cloud_assets` |
| Resource | `DbtCliResource` | `DbtCloudWorkspace` |
| Manifest source | Generated locally via `dbt parse` | Fetched from the dbt Cloud API |
| Project object | `DbtProject` | Not used |
| `prepare_if_dev()` | Used in local dev | Not applicable |
| Function body | `yield from dbt.cli([...]).stream()` | `yield from dbt_cloud.cli(args=[...]).wait()` |

`.stream()` processes events in real time as a local dbt process runs. `.wait()` polls the dbt Cloud API until the remote job completes, then returns the results — there's no local process to stream from.

The `DagsterDbtTranslator` works the same way in both cases.

---

## Setting up dbt Cloud integration

### 1. Configure credentials and workspace

```python
import os
import dagster as dg
from dagster_dbt import DbtCloudCredentials, DbtCloudWorkspace

workspace = DbtCloudWorkspace(
    credentials=DbtCloudCredentials(
        account_id=int(os.environ["DBT_CLOUD_ACCOUNT_ID"]),
        token=os.environ["DBT_CLOUD_API_TOKEN"],
        access_url="https://cloud.getdbt.com",  # your dbt Cloud URL
    ),
    project_id=int(os.environ["DBT_CLOUD_PROJECT_ID"]),
    environment_id=int(os.environ["DBT_CLOUD_ENVIRONMENT_ID"]),
)
```

The `account_id` and `project_id` appear in your dbt Cloud URLs. The `environment_id` is the deployment environment you want Dagster to use.

### 2. Define assets with `@dbt_cloud_assets`

```python
from dagster_dbt import dbt_cloud_assets

@dbt_cloud_assets(workspace=workspace)
def my_dbt_cloud_assets(
    context: dg.AssetExecutionContext,
    dbt_cloud: DbtCloudWorkspace,
):
    yield from dbt_cloud.cli(args=["build"], context=context).wait()
```

The function body uses `dbt_cloud.cli(...).wait()` instead of `dbt.cli(...).stream()`. The `args` keyword argument takes the same dbt commands you'd pass from the terminal.

### 3. Add to Definitions

```python
defs = dg.Definitions(
    assets=[my_dbt_cloud_assets],
    resources={"dbt_cloud": workspace},
)
```

---

## Partitioned dbt Cloud assets

Passing partition variables to dbt Cloud works the same way as with the CLI — use `--vars` with a JSON-encoded dict:

```python
import json

@dbt_cloud_assets(
    workspace=workspace,
    partitions_def=dg.DailyPartitionsDefinition(start_date="2024-01-01"),
)
def my_partitioned_dbt_cloud_assets(
    context: dg.AssetExecutionContext,
    dbt_cloud: DbtCloudWorkspace,
):
    time_window = context.partition_time_window
    dbt_vars = {
        "min_date": time_window.start.isoformat(),
        "max_date": time_window.end.isoformat(),
    }
    yield from dbt_cloud.cli(
        args=["build", "--vars", json.dumps(dbt_vars)],
        context=context,
    ).wait()
```

---

## Custom translator with dbt Cloud

`DagsterDbtTranslator` works exactly the same way. Pass it to the decorator:

```python
@dbt_cloud_assets(
    workspace=workspace,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
)
def my_dbt_cloud_assets(
    context: dg.AssetExecutionContext,
    dbt_cloud: DbtCloudWorkspace,
):
    yield from dbt_cloud.cli(args=["build"], context=context).wait()
```

---

## When to use dbt Cloud vs dbt CLI

Use the **CLI integration** when:
- You run dbt Core yourself (self-hosted or in CI/CD)
- You want Dagster to own dbt execution end-to-end
- You need fine-grained control over commands, selectors, and variables at runtime

Use the **dbt Cloud integration** when:
- dbt Cloud manages your project and environments
- You want Dagster to orchestrate dbt Cloud alongside other pipeline steps
- Your team controls dbt configuration through the dbt Cloud UI
