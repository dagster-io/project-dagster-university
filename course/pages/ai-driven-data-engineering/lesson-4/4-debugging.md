---
title: "Lesson 4: Debugging"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Debugging

The skill isn’t only for greenfield builds. You can use it to **debug** when something goes wrong. The agent may not get everything right on the first try; `dg check defs` confirms that definitions load, but runtime errors (e.g. missing files, wrong paths) can still appear when you run assets.

---

## Hitting a runtime error

Suppose you run the three raw assets and see:

```bash
_duckdb.IOException: IO Error: Cannot open file "/data/jaffle_shop.duckdb": No such file or directory
```

The code assumed a DuckDB path like `/data/jaffle_shop.duckdb`, but that path doesn’t exist on your machine (e.g. it was written for a different environment). You need to fix the path and ensure the directory exists.

---

## Debugging with the skill

Ask the agent to debug with the skill:

```bash
/dagster-expert Debug the 3 raw assets
```

The skill gives the agent a better picture of Dagster’s abstractions (resources, definitions, where config lives). The agent can:

- Launch the assets and tail logs to see the error.
- Identify that the DuckDB **resource** is configured with a bad path.
- Update the resource configuration so the database path is valid and the parent directory is created if needed.

So the agent doesn’t just “try random fixes”—it knows to look at the DuckDB resource and the file path it uses.

---

## Example fix

The agent might update the resource definition to use a path relative to the project and ensure the directory exists:

```python
from pathlib import Path

import dagster as dg
from dagster_duckdb import DuckDBResource

_DB_PATH = Path(__file__).parents[4] / "data" / "jaffle_shop.duckdb"
_DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "duckdb": DuckDBResource(database=str(_DB_PATH)),
        }
    )
```

Previously the resource might have used `database="data/jaffle_shop.duckdb"` or an absolute path like `/data/jaffle_shop.duckdb`. With the skill, the agent is more likely to fix the **right** place (the resource) and use a robust path pattern.

---

## Building and testing in isolated environments

When you work in a team or with CI, you often want to try changes in an **isolated** environment before merging. [Dagster+](https://docs.dagster.io/deployment/dagster-plus/deploying-code/branch-deployments) supports **branch deployments**: each branch can get its own deployment so you can run and debug pipelines (e.g. after the agent adds or changes assets) without affecting production. This workflow—build with the skill and `dg`, validate with `dg check defs`, run and debug in a branch deployment—fits well with AI-driven iteration.
