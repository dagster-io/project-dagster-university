import dagster as dg
from botocore.exceptions import ClientError
from dagster_aws.s3 import S3Resource

BUCKET = "test-bucket"
KEY = "fct_orders.parquet"


@dg.asset_check(asset=dg.AssetKey(["target", "s3_test_bucket_fct_orders", "parquet"]))
def fct_orders_parquet_exists(
    context: dg.AssetCheckExecutionContext, s3: S3Resource
) -> dg.AssetCheckResult:
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
            return dg.AssetCheckResult(
                passed=False, metadata={"reason": f"s3://{BUCKET}/{KEY} not found"}
            )
        raise
