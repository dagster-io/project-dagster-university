---
title: "Lesson 4: Debugging"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Debugging

Skills aren't only useful for greenfield builds. They are also your first line of defense when something breaks. And things will break as you are developing.

When that happens, the skill's understanding of Dagster's abstractions means the agent looks in the right place rather than trying random fixes.

## Hitting a runtime error

Suppose you run the three raw assets and see:

```bash
_duckdb.IOException: IO Error: Cannot open file "/data/jaffle_shop.duckdb": No such file or directory
```

The code assumed a DuckDB database path that doesn't exist on your machine. The agent may have written an absolute path that worked in its context but not in yours (a common failure mode for AI-generated path handling). You need to fix the path and ensure the parent directory gets created.

## Debugging with the skill

Ask the agent to debug with the skill active:

```bash {% obfuscated="true" %}
> /dagster-expert The raw assets are failing with this error:
_duckdb.IOException: IO Error: Cannot open file "/data/jaffle_shop.duckdb": No such file or directory
Debug and fix the issue.
```

The skill gives the agent a better picture of Dagster's abstractions—in particular, that connection configuration lives in `resources`, not inline in asset functions. Rather than searching every file for a path string, the agent goes directly to the DuckDB resource, identifies the misconfigured database path, and fixes it in the right place.

It can also launch the assets and tail logs to confirm the error before fixing it, so it's working from evidence rather than guessing.

## Example fix

The agent updates the resource definition to use a path relative to the project and ensures the parent directory exists at startup:

```python
from pathlib import Path

import dagster as dg
from dagster_duckdb import DuckDBResource

_DB_PATH = Path(__file__).parents[4] / "data" / "jaffle_shop.duckdb" # Debug fix
_DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "duckdb": DuckDBResource(database=str(_DB_PATH)),
        }
    )
```

Previously the resource might have used `database="data/jaffle_shop.duckdb"` (relative to wherever the process runs) or an absolute path like `/data/jaffle_shop.duckdb`. The fix uses `Path(__file__).parents[4]` to anchor the path to the project directory regardless of where the process is invoked. With the skill, the agent is more likely to fix the right place (the resource) and use a robust path pattern rather than patching the asset function directly.

## Building and testing in isolated environments

When you work in a team or with CI, you often want to try changes in an isolated environment before merging. Dagster+ supports [branch deployments](https://docs.dagster.io/deployment/dagster-plus/deploying-code/branch-deployments) where each branch gets its own deployment so you can run and debug pipelines after the agent makes changes without affecting production. The workflow—build with the skill and `dg`, validate with `dg check defs`, run and debug in a branch deployment—fits naturally with AI-driven iteration where you're making frequent, incremental changes.
