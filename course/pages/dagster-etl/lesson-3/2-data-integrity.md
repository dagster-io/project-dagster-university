---
title: "Lesson 3: Data integrity"
module: 'dagster_etl'
lesson: '3'
---

# Data integrity

Our ETL pipeline can execute successfully: we provide a file, and it gets loaded into DuckDB. While it’s reassuring to see data load without errors, there's actually something worse than a pipeline that fails to run, a pipeline that loads bad data.

Poor-quality data entering an ETL workflow can cause far more damage than a job that simply fails. Once bad data is ingested, it can have cascading effects, affecting all downstream consumers and applications. When fixing a bug around bad data, we not only have to fix the original issue, we’re also tasked with cleaning up every process that depends on it.

In many cases, the data we ingest comes from systems outside our control. We often treat these sources as the source of truth and assume they enforce their own validation rules. But when we know there are specific characteristics of the data that could disrupt our pipelines or outputs, it becomes critical to add validation checks before ingestion.

## Asset checks

In Dagster, one way to handle data validation is through asset checks. Asset checks let you define custom logic to ensure that an asset meets defined quality standards. For example, we can attach an asset check to `import_file` to verify that the file structure and contents meet our expectations.

Let’s start by writing an asset check to ensure the "share_price" column in the file contains only valid, non-zero values:

```python {% obfuscated="true" %}
with open("my_file.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    data = (row for row in reader)

    for row in data:
        if float(row["share_price"]) <= 0:
            break
```

Here’s what the logic might look like:

```python {% obfuscated="true" %}
@dg.asset_check(
    asset=import_file,
    blocking=True,
    description="Ensure file contains no zero value shares",
)
def not_empty(
    context: dg.AssetCheckExecutionContext,
    import_file,
) -> dg.AssetCheckResult:
    with open(import_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = (row for row in reader)

        for row in data:
            if float(row["share_price"]) <= 0:
                return dg.AssetCheckResult(
                    passed=False,
                    metadata={"'share' is below 0": row},
                )

    return dg.AssetCheckResult(
        passed=True,
    )
```

The code above does the following:

1. Uses the `@dg.asset_chec`k decorator to define an asset check. It references the `import_file` asset and sets `blocking=True`, which prevents downstream assets from executing if the check fails.
2. Reads the file path returned by the import_file asset and parses it as a CSV.
3. Iterates through each row to check whether the "share_price" value is less than or equal to zero (or missing/invalid).
4. Fails the check if any bad values are found; otherwise, it passes.

When you launch dg dev, you won’t see an additional node in the asset graph the asset check is visually tied to the import_file asset.

Now, when you re-execute the pipeline, a green dot will appear on the `import_file` node if the asset check passes, indicating both successful materialization and validation. If the check fails, the dot will appear red, helping you catch data issues early in the process.
