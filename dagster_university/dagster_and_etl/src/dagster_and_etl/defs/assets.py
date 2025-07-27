import dagster as dg
from dagster_duckdb import DuckDBResource
from pathlib import Path


# Generates a run_configuration. More information at: 
#   https://docs.dagster.io/guides/operate/configuration/run-configuration
class IngestionFileConfig(dg.Config):
    path: str

# Write an asset that reads a file and returns its content. Fixed relative path for simplicity.
@dg.asset()
def import_file(context: dg.AssetExecutionContext, config: IngestionFileConfig) -> str:
    file_path = (
        Path(__file__).absolute().parent / f"../../data/source/{config.path}"
    )

    return str(file_path.resolve())


# Another asset that creates a DuckDB table if it doesn't exist
@dg.asset(
    kinds={"duckdb"},
)
def duckdb_table(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    import_file: str,
):
    table_name = "raw_data"
    # Connect to duckdb using DuckDBResource
    with database.get_connection() as conn:
        table_query = f"""
            create table if not exists {table_name} (
                date date,
                share_price float,
                amount float,
                spend float,
                shift float,
                spread float
            ) 
        """
        # run create table statement
        conn.execute(table_query)
        # run copy into statement
        conn.execute(f"copy {table_name} from '{import_file}';")
        

