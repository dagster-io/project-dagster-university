# Dagster Essentials

## Overview

Learn the basics of Dagster, a Python-based platform that enables you to build robust, production-ready data pipelines. In this course, you’ll learn how to represent a data pipeline as the data assets it produces and orchestrate a pipeline you’ll make with Dagster.

## Completed code

If you are stuck you can reference the completed code for each lesson.

```
dagster_essentials
├── completed
│   ├── lesson_3
│   ├── lesson_4
│   ├── lesson_5
│   ├── lesson_6
│   ├── lesson_7
│   ├── lesson_8
│   └── lesson_9
```

## Dagster UI

To launch the UI for your project you can execute.

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

> [!NOTE]
> Running `dagster dev` will put you in the starter Dagster project. To see any of the completed lessons execute.
> `dagster dev -m dagster_essentials.lesson_{LESSON NUMBER}.definitions`

## Deploy on Dagster Cloud

The easiest way to deploy your Dagster project is to use Dagster Cloud.

Check out the [Dagster Cloud Documentation](https://docs.dagster.cloud) to learn more. 
