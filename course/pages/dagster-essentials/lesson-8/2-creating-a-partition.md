---
title: 'Lesson 8: Creating a partition'
module: 'dagster_essentials'
lesson: '8'
---

# Creating a partition

In the previous lesson, you created monthly and weekly schedules to materialize assets. You’ll now modify the assets to partition the taxi trips data and add a new partition with every scheduled run.

Luckily for us, the trip data is stored in parquet files that are separated by month, but NYC OpenData has historical taxi information dating back to 2009. In this example, you’ll only ingest and partition data from the beginning of 2023 to be mindful of compute resources and time.

---

## Constructing a partition definition

The first step in partitioning an asset is setting up a `PartitionDefinition`. Dagster has prebuilt hourly, daily, weekly, and monthly partitions for date-partitioned data. Following Dagster’s best practices for project structure, all partitions should be located in the `partitions` folder. In this project, all partitions will be in the `defs/partitions.py` file.

Additionally, your Dagster project contains an `assets/constants.py` file. This file contains `START_DATE` and `END_DATE` variables that, when used together, define the date range of the trip data to bring into the data pipeline.

Now that you have all the info you need to start building partitions, let’s take a look at an example:

```python
import dagster as dg
from dagster_essentials.defs.assets import constants

start_date = constants.START_DATE
end_date = constants.END_DATE

monthly_partition = dg.MonthlyPartitionsDefinition(
    start_date=start_date,
    end_date=end_date
)
```

Using Dagster’s `MonthlyPartitionDefinition`, we created a partition named `monthly_partition` and used the start and end dates to set the parameters of the function.

---

## Cleaning up existing storage

Before continuing, you should first delete Dagster’s materialization history of the existing assets. This only needs to be done when running locally.

In your terminal, stop the running server with `Ctrl+C`, then re-run the `dagster dev` command to start it again. This will delete this history.
