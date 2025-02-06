---
title: 'Lesson 3: Practice: Create a taxi_zones_folder asset'
module: 'dagster_essentials'
lesson: '3'
---

# Practice: Create a taxi_zones_folder asset

To practice what you’ve learned, create an asset in `trips.py` that:

- Is named `taxi_zones_folder`. This asset will contain a unique identifier, name, and boundary coordinates for each part of NYC as a distinct taxi zone.
- Uses the `requests` library to obtain [NYC Taxi Zones](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) data from [this link](https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip): `https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip`
- Uses zipfile and io modules to extract and store the unzipped directory in `data/raw/taxi_zones`; this path is provided for you in `constants.TAXI_ZONES_FOLDER_PATH`
- The relevant file (`taxi_zones.shp`) is now stored in the path `constants.TAXI_ZONES_FILE_PATH`

---

## Check your work

The asset you built should look similar to the following code. Click **View answer** to view it.

**If there are differences**, compare what you wrote to the asset below and change them, as this asset will be used as-is in future lessons.

```python {% obfuscated="true" %}
@asset
def taxi_zones_folder() -> None:
    """
    Downloads a zip file that contains a directory where our taxi_zones.shp file is located
    """

    # download the zip file content
    r = requests.get(
        "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip"
    )

    # create a zip file object from the downloaded content
    z = zipfile.ZipFile(io.BytesIO(r.content))

    # save the directory to specified folder
    z.extractall(constants.TAXI_ZONES_FOLDER_PATH)
```
