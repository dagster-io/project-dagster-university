import dagster as dg
from dagster_duckdb import DuckDBResource
from pathlib import Path


# Write an asset that finds all CSV files in the data/source directory
@dg.asset()
def import_file(context: dg.AssetExecutionContext) -> list[str]:
    project_root = Path(__file__).resolve().parents[3]  # Go up to project root
    source_dir = project_root / "data/source"
    
    # Find all CSV files in the directory
    csv_files = sorted(source_dir.glob("*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {source_dir}")
    
    # Return list of resolved file paths as strings
    file_paths = [str(f.resolve()) for f in csv_files]
    context.log.info(f"Found {len(file_paths)} CSV files: {[f.name for f in csv_files]}")
    
    return file_paths


# Another asset that creates a DuckDB table if it doesn't exist and loads all files
@dg.asset(
    kinds={"duckdb"},
)
def duckdb_table(
    context: dg.AssetExecutionContext,
    database: DuckDBResource,
    import_file: list[str],
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
        
        # Load all CSV files into the table
        for file_path in import_file:
            context.log.info(f"Loading file: {file_path}")
            conn.execute(f"copy {table_name} from '{file_path}';")
        

