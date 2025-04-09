---
title: 'Lesson 3: Asset materialization'
module: 'dagster_essentials'
lesson: '3'
---

# Asset materialization

Now that you’ve defined an asset in code, the next step is to **materialize** it. When an asset is materialized, Dagster runs the asset’s function and creates the asset by persisting the results in storage, such as in a data warehouse. When a materialization begins, it kicks off a **run.**

To better understand how materialization works, let’s take another look at the `taxi_trips_file` asset you created and what its function does:

```python
@dg.asset
def taxi_trips_file() -> None:
    """The raw parquet files for the taxi trips dataset. Sourced from the NYC Open Data portal."""
    month_to_fetch = "2023-03"
    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )

    with open(
        constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb"
    ) as output_file:
        output_file.write(raw_trips.content)
```

1. A description of the asset is added using a docstring (`”””`), which will display in the Dagster UI.

2. Next, a variable named `month_to_fetch` is defined. The value is `2023-03`, or March 2023.

3. A second variable named `raw_trips` is defined. This variable uses the `get` function from the `requests` library (`requests.get`) to retrieve a parquet file from the NYC Open Data portal website.

   Using the `month_to_fetch` variable, the URL to retrieve the file from becomes: `https://.../trip-data/yellow_tripdata_2023-03.parquet`

4. Next, the path where the file will be stored is constructed. The value of `TAXI_TRIPS_TEMPLATE_FILE_PATH`, stored in your project’s `assets/constants.py` file, is retrieved: `data/raw/taxi_trips_{}.parquet`

5. The parquet file is created and saved at `data/raw/taxi_trips_2023-03.parquet`

6. The asset function’s execution completes successfully. This completion indicates to Dagster that an asset has been materialized, and Dagster will update the UI to reflect that asset materialized successfully.

With the basics of materialization out of the way, let’s move on to actually materializing the `taxi_trips_file` asset.

---

## Materializing assets using dg

We can use `dg` to execute and launch assets. In order to execute an asset, use the `dg launch` command while providing the asset you wish to execute.

```bash
dg launch --assets taxi_trips_file
```

You will then see the logs as Dagster executes our asset:
```
2025-04-09 13:43:50 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15920 - RUN_START - Started execution of run for "__ASSET_JOB".
2025-04-09 13:43:50 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15920 - ENGINE_EVENT - Executing steps using multiprocess executor: parent process (pid: 15920)
2025-04-09 13:43:50 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15920 - taxi_trips_file - STEP_WORKER_STARTING - Launching subprocess for "taxi_trips_file".
2025-04-09 13:43:51 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15925 - taxi_trips_file - STEP_WORKER_STARTED - Executing step "taxi_trips_file" in subprocess.
2025-04-09 13:43:51 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15925 - taxi_trips_file - RESOURCE_INIT_STARTED - Starting initialization of resources [io_manager].
2025-04-09 13:43:51 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15925 - taxi_trips_file - RESOURCE_INIT_SUCCESS - Finished initialization of resources [io_manager].
2025-04-09 13:43:51 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15925 - LOGS_CAPTURED - Started capturing logs in process (pid: 15925).
2025-04-09 13:43:51 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15925 - taxi_trips_file - STEP_START - Started execution of step "taxi_trips_file".
2025-04-09 13:43:59 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15925 - taxi_trips_file - STEP_OUTPUT - Yielded output "result" of type "Nothing". (Type check passed).
2025-04-09 13:43:59 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15925 - taxi_trips_file - ASSET_MATERIALIZATION - Materialized value taxi_trips_file.
2025-04-09 13:43:59 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15925 - taxi_trips_file - STEP_SUCCESS - Finished execution of step "taxi_trips_file" in 7.71s.
2025-04-09 13:43:59 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15920 - ENGINE_EVENT - Multiprocess executor: parent process exiting after 8.35s (pid: 15920)
2025-04-09 13:43:59 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15920 - RUN_SUCCESS - Finished execution of run for "__ASSET_JOB".
```

You do not need to follow every line of the output, for now the most important thing is last line that the execution was successful.

```
2025-04-09 13:43:59 -0500 - dagster - DEBUG - __ASSET_JOB - 5b735e96-e6d4-4f37-80f4-641c22ef896d - 15920 - RUN_SUCCESS - Finished execution of run for "__ASSET_JOB".
```

## Materializing assets using the Dagster UI

If you don’t still have the Dagster UI running from Lesson 2, use the command line to run the following command in the root of your Dagster project (the top-level `dagster-university/dagster_essentials` directory):

```bash
dg dev
```

Navigate to [`localhost:3000`](http://localhost:3000/) in your browser. The page should look like the following - if it doesn’t, click **Overview** in the top navigation bar:

![The Overview page in the Dagster UI](/images/dagster-essentials/lesson-3/overview-page.png)

The page is empty for now, but it’ll look more interesting shortly. Let’s get started materializing the asset.

{% table %}

- Step one

---

- {% width="60%" %}
  Click **Assets** in the top navigation bar. The page that opens should look like the one to the right.

  **Note:** If this page is empty when you open it, click **Reload definitions**. We’ll discuss what this does in more detail in a later lesson.

  In this page, you’ll find a list of assets in the project and some high-level information about them, including:

  - The Code location and Asset group the asset belongs to, which we’ll cover in a later lesson
  - The asset’s status, which in the case of `taxi_trips_file`, is **Never materialized**

  Next, click the **View global asset lineage** link. This opens the global asset graph, which is where you can view your DAG.

- ![The Asset overview page in the Dagster UI](/images/dagster-essentials/lesson-3/assets-overview.png) {% rowspan=2 %}

{% /table %}

{% table %}

- Step two

---

- {% width="60%" %}
  It looks pretty empty right now, as there’s only one asset. But once you start adding more assets and dependencies, it’ll get more interesting.

  Additionally, notice that the asset’s description, pulled from its docstring, displays within the asset!

- ![The Global Asset Lineage page in the Dagster UI](/images/dagster-essentials/lesson-3/global-asset-view.png) {% rowspan=2 %}

{% /table %}

{% table %}

- Step three

---

- {% width="60%" %}
  Click the **Materialize** button, highlighted in the image to the right, to materialize the asset. This will run the function in the asset’s code to create the asset.

- ![Highlighted Materialize button in the Global Asset Lineage page of the Dagster UI](/images/dagster-essentials/lesson-3/materialize-button.png) {% rowspan=2 %}

{% /table %}

{% table %}

- Step four

---

- {% width="60%" %}
  After you click **Materialize**, a purple box will display at the top of the page like in the image on the right. This indicates that the run started successfully.

  A **run** is an instance of execution that materializes one or more assets.

- ![A materialized asset in the Global Asset Lineage page of the Dagster UI](/images/dagster-essentials/lesson-3/materialized-asset.png) {% rowspan=2 %}

{% /table %}

{% table %}

- Step five

---

- {% width="60%" %}
  Navigate to `data/raw` in your Dagster project to check out the file created by the asset materialization: `data/raw/taxi_trips_2023-03.parquet`

  **Note:** As the download may take a minute, this file may not show up right away.

- ![A materialized asset in the Global Asset Lineage page of the Dagster UI](/images/dagster-essentials/lesson-3/data-raw-parquet.png) {% rowspan=2 %}

{% /table %}

That’s it! You’ve successfully materialized your first asset! 🎉

## When to use `dg launch` vs `dg dev`

You now know two different ways to launch your asset. You may be wondering which one to use. Luckily there is no wrong answer. You might find it easier to execute an asset with `dg launch` when you need to quickly test something out while you may want to use `dg dev` as your Dagster project becomes more sophisticated.

For the majority of this course we will use `dg dev` to showcase more of the features of Dagster.