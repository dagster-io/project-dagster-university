---
title: "Lesson 2: Verify dbt installation"
module: 'dagster_dbt'
lesson: '2'
---

# Verify dbt installation

Before continuing, let’s run the dbt project from the command line to confirm that everything is configured correctly.

From the `dagster_university/dagster_and_dbt/dagster_and_dbt/analytics`  directory, run the following command:

```bash
dbt build
```

The two staging models should materialize successfully and pass their tests:

```bash
19:12:41  Running with dbt=1.9.3
19:12:42  Registered adapter: duckdb=1.9.2
19:12:43  Found 2 models, 2 data tests, 2 sources, 540 macros
19:12:43  
19:12:43  Concurrency: 1 threads (target='dev')
19:12:43  
19:12:43  1 of 4 START sql table model main.stg_trips .................................... [RUN]
19:12:49  1 of 4 OK created sql table model main.stg_trips ............................... [OK in 6.07s]
19:12:49  2 of 4 START sql table model main.stg_zones .................................... [RUN]
19:12:49  2 of 4 OK created sql table model main.stg_zones ............................... [OK in 0.03s]
19:12:49  3 of 4 START test accepted_values_stg_zones_borough__Manhattan__Bronx__Brooklyn__Queens__Staten_Island__EWR  [RUN]
19:12:49  3 of 4 PASS accepted_values_stg_zones_borough__Manhattan__Bronx__Brooklyn__Queens__Staten_Island__EWR  [PASS in 0.03s]
19:12:49  4 of 4 START test not_null_stg_zones_zone_id ................................... [RUN]
19:12:49  4 of 4 PASS not_null_stg_zones_zone_id ......................................... [PASS in 0.02s]
19:12:49  
19:12:49  Finished running 2 table models, 2 data tests in 0 hours 0 minutes and 6.28 seconds (6.28s).
19:12:49  
19:12:49  Completed successfully
19:12:49  
19:12:49  Done. PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4
```