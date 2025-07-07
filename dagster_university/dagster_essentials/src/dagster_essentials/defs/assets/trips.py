import requests
from dagster_essentials.defs.assets import constants

#To turn the function into an asset in Dagster, you’ll need to do two things:
import dagster as dg

'''
Note: dg check defs:
command in Dagster is used to validate the definitions of a Dagster project, ensuring they are correctly defined and can be loaded without errors.
It performs a static analysis of the project's definitions, including assets, jobs, resources, and sensors, to identify potential issues before runtime.

'''

'''

@dg.asset decorator, you can easily turn any existing Python function into a Dagster asset.

#Add the @dg.asset decorator before the function



'''
@dg.asset
def taxi_trips_file() -> None:
    """
      The raw parquet files for the taxi trips dataset. Sourced from the NYC Open Data portal.
    """
    month_to_fetch = '2023-03'
    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb") as output_file:
        output_file.write(raw_trips.content)
