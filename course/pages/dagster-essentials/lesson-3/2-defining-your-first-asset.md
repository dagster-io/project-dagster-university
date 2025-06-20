---
title: 'Lesson 3: Defining your first asset'
module: 'dagster_essentials'
lesson: '3'
---

# Defining your first asset

In this course, you’ll use data from [NYC OpenData](https://opendata.cityofnewyork.us/) to analyze New York City taxi rides. The first asset you’ll define uses data from [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), which contains trip records for several types of vehicles. However, we’ll focus on trip data for yellow cabs in this asset.

Your first asset, which you’ll name `taxi_trips_file`, will retrieve the yellow taxi trip data for March 2023 and save it to a location on your local machine.

## Project structure

Before we write our first asset, let's talk a little about project structures in Dagster. In the previous lesson we mentioned `dg` and how it offers a lot of helpful functionality to quickstart our project. We can use commands like `dg scaffold project` to initialize a `uv` virtual environment for us but we already took care of that when we set up the course in lesson 2.

However we can use `dg` to scaffold a file for our first asset. Run the following command to create the file that will contain our first asset.

```bash
dg scaffold defs dagster.asset assets/trips.py
```

This will add a `trips.py` file to our Dagster project.

```
.
└── src
    └── dagster_essentials
        └── defs
            └── assets
                ├── __init__.py
                ├── constants.py # already present
                └── trips.py
```

**Note:** If we were starting a Dagster project from scratch we would use [`uvx create-dagster`](https://docs.dagster.io/getting-started/installation) which will handle the creation of full Dagster project and virtual environment. However since we working in a repository that has already been initialized, we can skip this step.


Using `dg` to scaffold your project will ensure that files are placed in the correct location. We can ensure that everything is configured correctly also using `dg`.

```bash
> dg check defs
All components validated successfully.
All definitions loaded successfully.
```

This makes sense because even though we created the file that will contain our asset, we have not yet included the code.

## Defining your first asset

With the files set we can now add our first asset.

1. Navigate and open the newly created `src/dagster_essentials/defs/assets/trips.py` file in your Dagster project. This is where you’ll write your asset code.

2. Within the `trips.py` file, remove the generated code from the scaffolding and replace it with the following imports:

   ```python
   import requests
   from src.dagster_essentials.defs.assets import constants
   ```

3. Below the imports, let's define a function that takes no inputs and returns nothing (type-annoted with `None`). Add the following code to create a function to do this named `taxi_trips_file`:

   ```python
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
   ```

4. To turn the function into an asset in Dagster, you’ll need to do two things:

   1. Import the Dagster library:

      ```python
      import dagster as dg
      ```

   2. Add the `@dg.asset` decorator before the `taxi_trips_file` function. At this point, your code should look like this:

      ```python
      import requests
      from src.dagster_essentials.defs.assets import constants
      import dagster as dg

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
      ```

That’s it - you’ve created your first Dagster asset! Using the `@dg.asset` decorator, you can easily turn any existing Python function into a Dagster asset.

We can use `dg` again to check our asset:

```bash
> dg check defs
All components validated successfully.
All definitions loaded successfully.
```

**Questions about the `-> None` bit?** That's a Python feature called **type annotation**. In this case, it's saying that the function returns nothing. You can learn more about type annotations in the [Python documentation](https://docs.python.org/3/library/typing.html). We highly recommend using type annotations in your code to make it easier to read and understand.