---
title: 'Lesson 4: Practice: Create a taxi_zones asset'
module: 'dagster_essentials'
lesson: '4'
---

# Practice: Create a taxi_zones asset

Let’s use what you learned about creating dependencies between assets to practice creating an asset with dependencies.

In Lesson 3, you created a `taxi_zones_folder` asset that downloads a zipped directory containing a shapefile about NYC taxi zones.

Now, create a `taxi_zones` asset that uses the shapefile inside the `taxi_zones_folder` folder to create a table called `zones` in your DuckDB database. Recall that the path to this shapefile is stored in `constants.TAXI_ZONES_FILE_PATH`. This new table should have four columns:

- `zone_id`, which is the `LocationID` column, renamed
- `zone`
- `borough`
- `geometry`

You will need to use geopandas to open the shapefile, and the geopandas functions [set_crs()](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.set_crs.html), [to_crs()](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_crs.html), and [to_wkt()](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_wkt.html) to transform the Coordinate Reference System encoding from 'EPSG:2263' to 'EPSG:4326'; see [OpenNYC maintainer on GIS Stack Exchange](https://gis.stackexchange.com/a/27808) for additional details.

---

## Check your work

The asset you built should look similar to the following code. Click **View answer** to view it.

**If there are differences**, compare what you wrote to the asset below and change them, as this asset will be used as-is in future lessons.

```python {% obfuscated="true" %}
@asset(
    deps=["taxi_zones_folder"]
)
def taxi_zones() -> None:
    """
    The raw taxi zones shapefile with the following transformations:
    - Open as a geopandas df
    - Set the CRS encoding of the geometry column to 'EPSG:2263' -> See link https://gis.stackexchange.com/a/27808
    - Transform the CRS encoding of the geometry column from 'EPSG:2263' to 'EPSG:4326' (Enable lat / long visualizations)
    - Transform geometry column from geometry format to wkt (well known text) format, to store as a string
    - Load into the DuckDB database table
    """

    # read the shape file into a geopandas df
    gdf = gpd.read_file(constants.TAXI_ZONES_FILE_PATH)

    # set the coordinate reference system to EPSG:2263/NAD83
    gdf = gdf.set_crs(
        crs="EPSG:2263",
        inplace=True,
        allow_override=True)

    # transform the geometry column spatial encoding from EPSG:2263/NAD83 (NY specific) to EPSG:4326/WSG84 (global LAT/LONG)
    gdf.to_crs('EPSG:4326', inplace=True)

    # transform the geometry column into well known text (wkt) format
    gdf['geometry'] = gdf['geometry'].to_wkt()

    query = f"""
    create or replace table zones as (
        select 
            LocationId as zone_id,
            zone,
            borough,
            geometry
        from gdf
    );
    """

    conn = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={
            "database": os.getenv("DUCKDB_DATABASE"),
        },
        max_retries=10,
    )
    conn.execute(query)
```
