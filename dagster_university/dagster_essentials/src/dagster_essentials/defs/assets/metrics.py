import dagster as dg


@dg.asset
def metrics(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...
