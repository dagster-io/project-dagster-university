from datetime import datetime, timedelta

import dlt
from dlt.sources.rest_api import rest_api_source

start_date = datetime.now().strftime("%Y-%m-%d")
end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

source = rest_api_source(
    {
        "client": {
            "base_url": "https://api.nasa.gov/",
        },
        "resources": [
            {
                "name": "neo",
                "write_disposition": "append",
                "endpoint": {
                    "path": "neo/rest/v1/feed",
                    "params": {
                        "start_date": start_date,
                        "end_date": end_date,
                        "api_key": dlt.secrets["nasa_api_key"],
                    },
                },
            },
        ],
    }
)

pipeline = dlt.pipeline(
    pipeline_name="nasa_neo",
    destination="duckdb",
    dataset_name="nasa_neo",
)

load_info = pipeline.run(source)
