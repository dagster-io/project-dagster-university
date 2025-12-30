---
title: 'Lesson 3: Creating a Dagster resource to run dbt'
module: 'dagster_dbt'
lesson: '3'
---

# Creating a Dagster resource to run dbt

Our next step is to define a Dagster resource as the entry point used to run dbt commands and configure its execution.

The `DbtCliResource` is the main resource that you’ll be working with. In later sections, we’ll walk through some of the resource’s methods and how to customize what Dagster does when dbt runs.

> 💡 **Resource refresher:** Resources are Dagster’s recommended way of connecting to other services and tools, such as dbt, your data warehouse, or a BI tool.

Navigate to `defs/resources.py`, which is where other resources are defined. You'll be adding to this existing file, not replacing it.

> ⚠️ **Important:** The `resources.py` file already contains code for `database_resource`, `smart_open_config`, and other imports. Do not delete this existing code! You'll be adding the dbt-related imports and resource definition to the file.

1. First, add the following imports to the **top of the file**, alongside the existing imports:

   ```python
   from dagster_dbt import DbtCliResource

   from dagster_and_dbt.defs.project import dbt_project
   ```

2. Next, add the `dbt_resource` definition somewhere below the existing `smart_open_config` code:

   ```python
   dbt_resource = DbtCliResource(
       project_dir=dbt_project,
   )
   ```

3. Finally, update the `@dg.definitions` function to include the new `dbt` resource:

   ```python
   @dg.definitions
   def resources():
       return dg.Definitions(
           resources={
               "database": database_resource,
               "dbt": dbt_resource,
           },
       )
   ```

After making these changes, your complete `resources.py` file should look like this:

```python
# src/dagster_and_dbt/defs/resources.py
import os

import boto3
import dagster as dg
from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource

from dagster_and_dbt.defs.project import dbt_project

database_resource = DuckDBResource(
    database=dg.EnvVar("DUCKDB_DATABASE"),
)

if os.getenv("DAGSTER_ENVIRONMENT") == "prod":
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    smart_open_config = {"client": session.client("s3")}
else:
    smart_open_config = {}


dbt_resource = DbtCliResource(
    project_dir=dbt_project,
)


@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "database": database_resource,
            "dbt": dbt_resource,
        },
    )
```

The new code:

1. Imports the `DbtCliResource` from the `dagster_dbt` package that we installed earlier
2. Imports the `dbt_project` representation we just defined
3. Instantiates a new `DbtCliResource` under the variable name `dbt_resource`
4. Tells the resource that the dbt project to execute is the `dbt_project`
5. Adds the dbt resource to the definitions so it can be automatically loaded
