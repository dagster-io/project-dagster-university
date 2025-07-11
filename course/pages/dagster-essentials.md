---
title: Dagster Essentials
---

- Lesson 1: Introduction
  - [What's data engineering?](/dagster-essentials/lesson-1/0-whats-data-engineering)
  - [What's an orchestrator?](/dagster-essentials/lesson-1/1-whats-an-orchestrator)
  - [Orchestration approaches](/dagster-essentials/lesson-1/2-orchestration-approaches)
  - [Why is asset-centric orchestration good for data engineering?](/dagster-essentials/lesson-1/3-why-is-asset-centric-orchestration-good-for-data-engineering)
  - [Project preview](/dagster-essentials/lesson-1/4-project-preview)

- Lesson 2: Requirements & installation
  - [Requirements](/installation/requirements)
  - [Set up local](/installation/set-up-local)
  - [Set up Codespace](/installation/set-up-codespace)
  - [Project files](/dagster-essentials/lesson-2/3-project-files)

- Lesson 3: SDAs
  - [Overview](/dagster-essentials/lesson-3/0-overview)
  - [What's an asset?](/dagster-essentials/lesson-3/1-whats-an-asset)
  - [Defining your first asset](/dagster-essentials/lesson-3/2-defining-your-first-asset)
  - [Asset materialization](/dagster-essentials/lesson-3/3-asset-materialization)
  - [Viewing run details](/dagster-essentials/lesson-3/4-viewing-run-details)
  - [Troubleshooting failed runs](/dagster-essentials/lesson-3/5-troubleshooting-failed-runs)
  - [Coding practice: Create a taxi_zones_file asset](/dagster-essentials/lesson-3/6-coding-practice-taxi-zones-file-asset)
  - [Recap](/dagster-essentials/lesson-3/7-recap)

- Lesson 4: Asset dependencies
  - [Overview](/dagster-essentials/lesson-4/0-overview)
  - [What's a dependency?](/dagster-essentials/lesson-4/1-whats-a-dependency)
  - [Assets and database execution](/dagster-essentials/lesson-4/2-assets-and-database-execution)
  - [Loading data into a database](/dagster-essentials/lesson-4/3-loading-data-into-a-database)
  - [Practice: Create a taxi_zones asset](/dagster-essentials/lesson-4/4-coding-practice-taxi-zones-asset)
  - [Assets with in-memory computations](/dagster-essentials/lesson-4/5-assets-with-in-memory-computations)
  - [Practice: Create a trips_by_week asset](/dagster-essentials/lesson-4/6-coding-practice-trips-by-week-asset)

- Lesson 5: Definitions & code locations
  - [Overview](/dagster-essentials/lesson-5/0-overview)
  - [What's the Definitions object?](/dagster-essentials/lesson-5/1-whats-the-definitions-object)
  - [What's a code location?](/dagster-essentials/lesson-5/2-whats-a-code-location)
  - [Code locations in the Dagster UI](/dagster-essentials/lesson-5/3-code-locations-dagster-ui)

- Lesson 6: Resources
  - [Overview](/dagster-essentials/lesson-6/0-overview)
  - [What's a resource?](/dagster-essentials/lesson-6/1-whats-a-resource)
  - [Setting up a database resource](/dagster-essentials/lesson-6/2-setting-up-a-database-resource)
  - [Using resources in assets](/dagster-essentials/lesson-6/3-using-resources-in-assets)
  - [Practice: Refactoring assets to use resources](/dagster-essentials/lesson-6/4-coding-practice-refactoring-assets)
  - [Analyzing resource usage using the Dagster UI](/dagster-essentials/lesson-6/5-analyzing-resources-dagster-ui)
  - [Lesson recap](/dagster-essentials/lesson-6/6-recap)

- Lesson 7: Schedules
  - [Overview](/dagster-essentials/lesson-7/0-overview)
  - [What are schedules?](/dagster-essentials/lesson-7/1-what-are-schedules)
  - [Practice: Create a weekly_update_job](/dagster-essentials/lesson-7/2-coding-practice-weekly-update-job)
  - [Creating a schedule](/dagster-essentials/lesson-7/3-creating-a-schedule)
  - [Practice: Create a weekly_update_schedule](/dagster-essentials/lesson-7/4-coding-practice-weekly-update-schedule)
  - [Updating the Definitions object](/dagster-essentials/lesson-7/5-updating-the-definitions-object)
  - [Jobs and schedules in the Dagster UI](/dagster-essentials/lesson-7/6-jobs-schedules-dagster-ui)

- Lesson 8: Partitions and backfills
  - [Overview](/dagster-essentials/lesson-8/0-overview)
  - [What are partitions and backfills?](/dagster-essentials/lesson-8/1-what-are-partitions-and-backfills)
  - [Creating a partition](/dagster-essentials/lesson-8/2-creating-a-partition)
  - [Practice: Create a weekly partition](/dagster-essentials/lesson-8/3-coding-practice-weekly-partition)
  - [Adding partitions to assets](/dagster-essentials/lesson-8/4-adding-partitions-to-assets)
  - [Practice: Partition the taxi_trips asset](/dagster-essentials/lesson-8/5-coding-practice-partition-taxi-trips)
  - [Creating a schedule with a date-based partition](/dagster-essentials/lesson-8/6-creating-a-schedule-with-a-date-based-partition)
  - [Practice: Partition the trips_by_week asset](/dagster-essentials/lesson-8/7-coding-practice-partition-trips-by-week)
  - [Partitions and backfills in the Dagster UI](/dagster-essentials/lesson-8/8-partitions-backfills-dagster-ui)
  - [Recap](/dagster-essentials/lesson-8/9-recap)

- Lesson 9: Sensors
  - [Overview](/dagster-essentials/lesson-9/0-overview)
  - [What's a sensor?](/dagster-essentials/lesson-9/1-whats-a-sensor)
  - [Configuring asset creation](/dagster-essentials/lesson-9/2-configuring-asset-creation)
  - [Creating an asset triggered by a sensor](/dagster-essentials/lesson-9/3-creating-an-asset-triggered-by-a-sensor)
  - [Creating a job](/dagster-essentials/lesson-9/4-creating-a-job)
  - [Building the sensor](/dagster-essentials/lesson-9/5-building-the-sensor)
  - [Updating the Definitions object](/dagster-essentials/lesson-9/6-updating-the-definitions-object)
  - [Sensors in the Dagster UI](/dagster-essentials/lesson-9/7-sensors-dagster-ui)
  - [Enabling the sensor](/dagster-essentials/lesson-9/8-enabling-the-sensor)

- [Capstone](/dagster-essentials/capstone)

- Extra credit: Metadata
  - [Overview](/dagster-essentials/extra-credit/0-overview)
  - [What's metadata?](/dagster-essentials/extra-credit/1-whats-metadata)
  - [Definition metadata - Asset descriptions](/dagster-essentials/extra-credit/2-definition-metadata-asset-descriptions)
  - [Definition metadata - Asset groups](/dagster-essentials/extra-credit/3-definition-metadata-asset-groups)
  - [Practice: Grouping assets](/dagster-essentials/extra-credit/4-coding-practice-grouping-assets)
  - [Materialization metadata](/dagster-essentials/extra-credit/5-materialization-metadata)
  - [Practice: Add metadata to taxi_zones_file](/dagster-essentials/extra-credit/6-coding-practice-metadata-taxi-zones-file)
  - [Asset metadata as Markdown](/dagster-essentials/extra-credit/7-asset-metadata-as-markdown)
