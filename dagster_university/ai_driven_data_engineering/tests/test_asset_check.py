from unittest.mock import MagicMock

import dagster as dg
from botocore.exceptions import ClientError

from ai_driven_data_engineering.defs.checks.fct_orders_parquet_exists import (
    fct_orders_parquet_exists,
)


def test_fct_orders_parquet_exists_pass():
    """Asset check passes when object exists in S3."""
    mock_client = MagicMock()
    mock_client.head_object.return_value = {"ContentLength": 12345}

    mock_s3 = MagicMock()
    mock_s3.get_client.return_value = mock_client

    context = dg.build_asset_check_context()
    result = fct_orders_parquet_exists(context, mock_s3)

    assert result.passed
    assert result.metadata["size_bytes"].value == 12345
    mock_client.head_object.assert_called_once_with(
        Bucket="test-bucket", Key="fct_orders.parquet"
    )


def test_fct_orders_parquet_exists_fail_404():
    """Asset check fails when object is not found (404)."""
    mock_client = MagicMock()
    error = ClientError(
        {"Error": {"Code": "404", "Message": "Not Found"}},
        "HeadObject",
    )
    mock_client.head_object.side_effect = error

    mock_s3 = MagicMock()
    mock_s3.get_client.return_value = mock_client

    context = dg.build_asset_check_context()
    result = fct_orders_parquet_exists(context, mock_s3)

    assert not result.passed
    assert "not found" in result.metadata["reason"].value
