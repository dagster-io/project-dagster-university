---
title: "Lesson 3: What's an asset?"
module: 'dagster_essentials'
lesson: '3'
---

# What's an asset?

An asset is an object in persistent storage that captures some understanding of the world. If you have an existing data pipeline, you’re likely already creating assets. For example, your pipeline might incorporate objects like:

- **A database table or view**, such as those in a Google BigQuery data warehouse
- **A file**, such as a file in your local machine or blob storage like Amazon S3
- **A machine learning model**, such as TensorFlow or PyTorch
- **An asset from an integration,** such as a dbt model or a Fivetran connector

Assets aren’t limited to just the objects listed above - these are just some common examples.

---

## Anatomy of an asset

To create an asset, you write code that describes an asset that you want to exist, along with any other assets that the asset is derived from, and a function that computes the contents of the asset.

Specifically, an asset includes:

- **An `@dg.asset` decorator.** This tells Dagster that the function produces an asset.
- **An asset key** that uniquely identifies the asset in Dagster. By default, this is the function name. However, asset keys can have prefixes, much like how files are in folders or database tables are in schemas.
- **A set of upstream asset dependencies**, referenced using their asset keys. We’ll talk about this more in the next lesson, which focuses on asset dependencies.
- **A Python function** that defines how the asset is computed.

**Let’s look at our cookie example to demonstrate**. The following code creates a `cookie_dough` asset, which depends on the upstream `dry_ingredients` and `wet_ingredients` assets:

```python
@dg.asset
def cookie_dough(dry_ingredients, wet_ingredients):
    return dry_ingredients + wet_ingredients
```

When naming assets, it’s best practice to use a **noun**, specifically **a descriptor of what is produced,** and not the steps required to produce it.

For example, the example asset combines the `dry_ingredients` and `wet_ingredients` assets to create cookie dough. We named it `cookie_dough` because that’s what the asset produces, whereas a name like `combine_ingredients` focuses on an action and not the end result.

---

## Assets vs Dagster Components

Introduced in Dagster 1.11, [Dagster Components](https://docs.dagster.io/guides/build/components/) provide a structured and modular way to:

* Organize and scaffold Dagster projects efficiently.
* Simplify configuration of common workflows using predefined or custom templates.
* Enable reusable abstractions that make complex orchestration easier to manage and maintain.

Components are an incredibly powerful abstraction in Dagster, and we’ll cover in detail how to use the [dg CLI](https://docs.dagster.io/api/dg) to scaffold and navigate your project. However, we won’t explore all the details of using components for integrations or custom workflows, as these will make more sense once you’re familiar with the foundational objects in a Dagster project. This course will focus primarily on those fundamentals.

For more information on applying components in practice, explore the following resources:

* [ETL Tutorial Pipeline](https://docs.dagster.io/etl-pipeline-tutorial/)
* [Dagster & ETL](https://courses.dagster.io/courses/dagster-etl)
