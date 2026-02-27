---
title: "Lesson 5: Skill chaining"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Skill chaining

If you look back at everything you've built in this lesson, you'll notice something: you didn't use just one skill. You used `/dagster-integrations` to set up dbt and Sling, and somewhere in the process you probably switched to `/dagster-expert` to handle definitions, dependencies, and debugging. That back-and-forth is intentional, and it has a name: skill chaining.

Skill chaining is the practice of switching between skills as the nature of your task shifts. It's one of the most important habits you can develop for AI-driven Dagster work, because the two main skills have genuinely different knowledge domains that complement each other.

## How to think about it

The distinction isn't always obvious at first, but a simple rule covers most cases:

Use `/dagster-expert` when you're working with Dagster itself—its core abstractions, project structure, and CLI:

- Creating or scaffolding assets, schedules, sensors, jobs
- Understanding project structure and definitions
- Running or materializing assets (`dg launch`, `dg list`)
- Debugging failed runs
- Automation: conditions, partitions, backfills
- Any general Dagster concept, including asset checks

Use `/dagster-integrations` when you're connecting Dagster to something external:

- Working with a specific `dagster-*` library (e.g. `dagster-dbt`, `dagster-sling`, `dagster-fivetran`)
- Configuring or troubleshooting a Component
- Setting up a new integration for the first time
- Questions about how a specific external tool maps into Dagster

Rule of thumb: if the question mentions a specific external technology (dbt, S3, Fivetran, Snowflake, Sling), reach for `/dagster-integrations`. If it's about Dagster itself—structure, definitions, checks, automation—use `/dagster-expert`.

## The chaining pattern in this lesson

Look at what happened as we built this lesson's project:

1. `/dagster-integrations` handled setting up the dbt Component—installing dependencies, scaffolding the Component layout with `dg`, building the dbt models, and validating with `dbt parse`. This is integration territory: the skill knows how `DbtProjectComponent` works, what YAML config it expects, and how dbt projects map to Dagster assets.

2. `/dagster-expert` handled wiring assets together, setting group names, and the `dg` workflow around it. Once the dbt Component existed as a Dagster entity, questions like "which group should these assets be in?" or "how do I connect the raw assets to the dbt models?" are core Dagster questions, not dbt questions.

3. `/dagster-integrations` came back for the Sling component—same pattern as dbt: scaffold the Component, configure the replication, wire the dependency.

4. `/dagster-expert` again for the asset check in the worked example below. Adding an asset check is a core Dagster concept even though the check touches S3.

5. `/dagster-integrations` one more time to refine the asset check to use the S3 resource rather than raw boto3—because now the question is specifically about the `dagster-aws` integration pattern.

That's five skill switches over a single lesson. Each one happens at a natural seam: when the task shifts from "configure this external tool" to "wire this into Dagster" and back again.

## A worked example: adding an asset check

The asset check is a good illustration because it sits right on the boundary between the two skills.

You want to verify that the Parquet file the Sling export produces actually exists in S3. The check touches an external service (S3), which might suggest `/dagster-integrations`. But the task is fundamentally about adding an asset check, a core Dagster concept—so start with `/dagster-expert`:

```bash {% obfuscated="true" %}
> /dagster-expert Include an asset check for the parquet asset to ensure that file exists in the S3 bucket.
```

The agent creates a working asset check. The code makes sense, but if you look closely you'll spot a small anti-pattern: the check builds its own S3 connection using `boto3` instead of using a Dagster resource. That works, but it means credentials and endpoint config are embedded in the check rather than living in one shared place.

```python {% obfuscated="true" %}
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

This is where you chain to `/dagster-integrations`. The next task is specifically about the S3 integration—using the Dagster S3 resource instead of boto3 directly:

```bash {% obfuscated="true" %}
> /dagster-integrations Rewrite the fct_orders_parquet_exists to use the Dagster S3 resource instead of boto3 directly.
```

The integrations skill knows the `dagster-aws` S3 resource pattern and makes two changes.

First, it adds an S3 resource to your definitions:

```python {% obfuscated="true" %}
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

Second, it updates the asset check to receive the S3 client via dependency injection instead of building its own:

```python {% obfuscated="true" %}
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

The behavior is identical, but credentials and endpoint config now live in the resource, and the check itself is simpler and consistent with how Dagster expects resource-backed checks to look.

---

## Why this matters

Skill chaining isn't overhead—it's how you get the most out of both skills. Each one has deep context about its domain, and neither one has deep context about the other's. When you're working on dbt models, the integrations skill knows far more about `DbtProjectComponent` than the expert skill does. When you're debugging a failed run, the expert skill knows far more about Dagster's execution model.

The seam between the two skills usually corresponds to a natural seam in the work itself: configuring an external tool versus wiring it into Dagster. Recognizing that seam is the skill.
