---
title: "Lesson 5: When to use each skill"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# When to use the Dagster Expert vs Dagster Integrations skill

Sometimes the right skill isn’t obvious. For example, say you want to add an **asset check** for the Sling Parquet asset to ensure the file exists in S3. The check touches an external service (S3), which might suggest `dagster-integrations`, but the task is really about **adding an asset check**—a core Dagster concept—so **`dagster-expert`** is the better choice.

Here’s how to think about when to use each skill, then we’ll add that asset check and refine it with both skills.

---

## When to use each skill

**`/dagster-expert`** — Use for core Dagster questions:

- Creating or scaffolding assets, schedules, sensors, jobs
- Understanding project structure and definitions
- Running or materializing assets (`dg launch`, `dg list`, etc.)
- Debugging failed runs
- Automation: conditions, partitions, backfills
- Any general Dagster concept (including asset checks)

**`/dagster-integrations`** — Use when connecting Dagster to an external tool:

- Working with a specific `dagster-*` library (e.g. `dagster-dbt`, `dagster-sling`, `dagster-fivetran`)
- Questions about how an integration or component is configured
- Setting up a new integration for the first time

In practice the two skills often **chain together**. In this course:

1. **`/dagster-integrations`** guided setting up the dagster-sling and dagster-dbt components (external tools).
2. **`/dagster-expert`** handled scaffolding, the `dg` CLI, asset dependencies, and group names (core Dagster).

**Rule of thumb:** If the question mentions a specific external technology (dbt, S3, Fivetran, Snowflake, etc.), reach for **`/dagster-integrations`**. If it’s about Dagster itself—structure, definitions, checks, automation—use **`/dagster-expert`**.

---

## Adding the asset check with dagster-expert

Ask the expert skill to add the check:

```bash
/dagster-expert Include an asset check for the parquet asset to ensure that file exists in the S3 bucket
```

The agent creates an asset check that verifies the Parquet file exists in S3. The check runs and passes. The code makes sense, but if you know Dagster you may spot a small anti-pattern: the check builds its own S3 connection (e.g. with `boto3`) instead of using a Dagster **resource**. That works, but it’s cleaner to use the S3 resource so credentials and config live in one place and the check stays focused on the assertion.

Example of what the agent might generate (connection inside the check):

```python
import os

import boto3
import dagster as dg
from botocore.exceptions import ClientError

BUCKET = "test-bucket"
KEY = "fct_orders.parquet"

@dg.asset_check(asset=dg.AssetKey(["target", "s3_test_bucket_fct_orders", "parquet"]))
def fct_orders_parquet_exists(context: dg.AssetCheckExecutionContext) -> dg.AssetCheckResult:
    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ["AWS_ENDPOINT_URL_S3"],
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    try:
        response = s3.head_object(Bucket=BUCKET, Key=KEY)
        size_bytes = response["ContentLength"]
        return dg.AssetCheckResult(
            passed=True,
            metadata={"size_bytes": dg.MetadataValue.int(size_bytes)},
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return dg.AssetCheckResult(passed=False, metadata={"reason": f"s3://{BUCKET}/{KEY} not found"})
        raise
```

---

## Refining with dagster-integrations: use the S3 resource

Switch to the integrations skill and ask it to use the Dagster S3 resource instead of boto3 directly:

```bash
/dagster-integrations Rewrite the fct_orders_parquet_exists to use the Dagster S3 resource instead of boto3 directly
```

The agent makes two changes.

**1. Add an S3 resource to your definitions** (e.g. in `resources()`):

```python
@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "duckdb": DuckDBResource(database=str(_DB_PATH)),
            "s3": S3Resource(
                endpoint_url=dg.EnvVar("AWS_ENDPOINT_URL_S3"),
                aws_access_key_id=dg.EnvVar("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=dg.EnvVar("AWS_SECRET_ACCESS_KEY"),
                region_name="us-east-1",
                use_ssl=False,
            ),
        }
    )
```

**2. Update the asset check to use the resource** so it receives the S3 client via dependency injection:

```python
@dg.asset_check(asset=dg.AssetKey(["target", "s3_test_bucket_fct_orders", "parquet"]))
def fct_orders_parquet_exists(context: dg.AssetCheckExecutionContext, s3: S3Resource) -> dg.AssetCheckResult:
    client = s3.get_client()

    try:
        response = client.head_object(Bucket=BUCKET, Key=KEY)
        size_bytes = response["ContentLength"]
        return dg.AssetCheckResult(
            passed=True,
            metadata={"size_bytes": dg.MetadataValue.int(size_bytes)},
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return dg.AssetCheckResult(passed=False, metadata={"reason": f"s3://{BUCKET}/{KEY} not found"})
        raise
```

The behavior is the same, but credentials and endpoint config live in the resource, and the check is simpler and more consistent with Dagster’s resource pattern. Using **`/dagster-expert`** for the asset check and **`/dagster-integrations`** for the S3 resource is a good example of chaining the two skills for the right outcome.
