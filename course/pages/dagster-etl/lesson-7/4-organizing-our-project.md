---
title: "Lesson 7: Organizing our project"
module: 'dagster_etl'
lesson: '7'
---

# Organizing our project

Organizing your Dagster project with components brings structure, scalability, and clarity to your data platform. Instead of building one large codebase where assets, resources, and configurations are tightly coupled, components allow you to break your project into self-contained modules. Each component bundles together related logic—such as a data source, transformation, or model training step—along with its resources and config schemas. This modular layout makes it easier to onboard new team members, reuse functionality across pipelines, and iterate on parts of your system without risking unrelated functionality.

A well-organized component-based project typically follows a pattern where each component lives in its own directory or package, complete with its own virtual environment, tests, and documentation. For example, you might have components/snowflake_ingestion, components/ml_training, and components/reporting_pipeline, each representing a logical slice of your platform. This structure encourages encapsulation and reduces dependency sprawl, allowing individual components to evolve at their own pace. By centralizing composition in your definitions.py file (or similar), you can declaratively stitch components together to build end-to-end workflows without compromising maintainability. As your team and projects grow, components provide the foundation for a scalable and collaborative development model.

## Navigating a large asset graph

As your project grows, the asset graph in the Dagster UI can become crowded. Asset groups and tags let you filter the graph without restructuring your code.

**Asset groups** assign a set of assets to a named category, which appears as a filter in the UI. You can set a group on any asset with the `group_name` parameter:

```python
@dg.asset(group_name="ingestion")
def raw_orders(): ...

@dg.asset(group_name="transforms")
def orders_by_customer(): ...
```

You can then click a group name in the asset graph to show only the assets in that group.

**Tags** offer finer-grained filtering. Any key-value pair works:

```python
@dg.asset(tags={"layer": "staging", "source": "postgres"})
def staging_orders(): ...
```

Use tags to filter by team, environment, data domain, or any dimension that makes sense for your project. Groups and tags compose: you can narrow the graph to a group and then filter further by tag.
