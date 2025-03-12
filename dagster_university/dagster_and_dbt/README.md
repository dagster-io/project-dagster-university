# Dagster and dbt

## Overview

In this course, you'll learn how to integrate and orchestrate dbt projects with Dagster. You'll load dbt models into Dagster as assets, build dependencies, and ready your project for production deployment.

## Completed code

If you are stuck you can reference the completed code for each lesson.

```
dagster_and_dbt
├── completed
│   ├── lesson_3
│   ├── lesson_4
│   ├── lesson_5
│   └── lesson_6
```

## Dagster UI

To launch the UI for your project you can execute.

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

> [!NOTE]
> Running `dagster dev` will put you in the starter Dagster project. To see any of the completed lessons execute.
> `dagster dev -m dagster_and_dbt.lesson_{LESSON NUMBER}.definitions`

## Deploy on Dagster Cloud

The easiest way to deploy your Dagster project is to use Dagster Cloud.

Check out the [Dagster Cloud Documentation](https://docs.dagster.cloud) to learn more. 