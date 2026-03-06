import dagster as dg


@dg.asset
def trips(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...
