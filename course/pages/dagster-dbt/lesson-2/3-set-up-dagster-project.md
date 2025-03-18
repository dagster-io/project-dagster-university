---
title: "Lesson 2: Set up the Dagster project"
module: 'dagster_dbt'
lesson: '2'
---

# Set up the Dagster project

To confirm everything works:

1. Run `dagster dev`  from the directory `dagster_university/dagster_and_dbt`.
2. Navigate to the Dagster UI ([`http://localhost:3000`](http://localhost:3000/)) in your browser.
3. Open the asset graph by clicking **Assets > View global asset lineage** and confirm the asset graph you see matches the graph below.

   ![The Asset Graph in the Dagster UI](/images/dagster-dbt/lesson-2/asset-graph.png)

4. Let's confirm that you can materialize these assets by:
   1. Navigating to **Overview > Jobs**
   2. Clicking on the `trip_update_job` job and then **Materialize all...**. 
   3. When prompted to select a partition, materialize the most recent one (`2023-03-01`). It will start a run/backfill and your assets should materialize successfully.