---
title: "Lesson 3: Data integrity"
module: 'dagster_etl'
lesson: '3'
---

## Data integrity

Our simple ETL pipeline is now ready to execute: we provide a file, and it gets loaded into DuckDB. While it's great that we can load data without errors, there's actually something worse than pipelines that fail to run, pipelines that run and load bad data.

Bad data entering an ETL workflow can cause far more issues than a failed job. When poor-quality data is ingested, it creates a cascading effect where all downstream consumers are impacted. This means we not only have to fix the original error in the ETL pipeline, but also clean up every dependent process that has been affected.

In most cases, the data we receive comes from systems outside our control. Generally, we treat these sources as the source of truth and assume they have their own validation in place to ensure data quality. However, when we know specific aspects of the data could negatively affect our system, it's critical to include validation checks before ingestion.

## Asset checks

In Dagster, one way to handle data validation is through asset checks. Asset checks allow you to define custom logic to ensure your assets meet specific quality criteria. For example, we can add an asset check to import_file to verify that the file structure and contents are as expected.

Let’s write an asset check to ensure the "share price" in the file matches what we expect:

```python
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

1. Uses the @dg.asset_check decorator to define an asset check. Within the decorator, we reference the import_file asset and set blocking=True, which ensures that downstream assets will not execute if the check fails.
2. Reads the file path from import_file and returns a generator of dictionaries.
3. Iterates through each row to check whether any share prices are less than or equal to zero.
4. If any share price is less than or equal to zero, the check fails; otherwise, it passes.

When you launch dg dev again, you won’t see any additional nodes in the asset graph, the asset check is visually tied directly to the import_file asset.

Now, if you re-execute the pipeline, a green dot will appear within the import_file node to indicate that the asset successfully materialized and the asset check passed.