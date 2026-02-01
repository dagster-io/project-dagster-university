import os

import dlt

data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]


@dlt.source
def simple_source():
    @dlt.resource
    def load_dict():
        yield data

    return load_dict


pipeline = dlt.pipeline(
    pipeline_name="simple_pipeline",
    destination=dlt.destinations.duckdb(os.getenv("DUCKDB_DATABASE")),
    dataset_name="mydata",
)

# Run with write_disposition to control how data is loaded:
# - "replace": Replace the entire table (default for fresh loads)
# - "append": Add records to existing data
# - "merge": Upsert based on primary_key (requires primary_key parameter)

if __name__ == "__main__":
    load_info = pipeline.run(simple_source())
