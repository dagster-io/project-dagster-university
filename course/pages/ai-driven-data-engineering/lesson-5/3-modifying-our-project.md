---
title: "Lesson 5: Modifying our project"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Modifying our project

The dbt Component and models are in place, but the project isn't quite right yet. The dbt assets aren't connected to the raw assets in the graph, they're not organized into a group, and we don't have any data quality checks. Each of these is a follow-up prompt, and the `dagster-integrations` skill knows how to handle all of them.

## Connect dbt assets to the raw assets

The most important fix is wiring the dependency: dbt models should only materialize after the raw assets have run. Without this connection, Dagster doesn't know the order things need to happen in. Ask the skill to make the connection:

```bash {% obfuscated="true" %}
> /dagster-integrations Connect the dbt assets to the raw assets
```

The agent updates the asset graph so the dbt staging models depend on the corresponding raw assets. After this change, materializing `stg_customers` will automatically trigger `raw_customers` first if it's stale. That's the lineage working as intended.

## Set a group name for dbt assets

With multiple layers of assets in the catalog—raw tables, staging models, a facts table, eventually an S3 export—organization matters. Putting the dbt-derived assets in a `transformation` group makes the asset graph easier to read and the catalog easier to navigate:

```bash {% obfuscated="true" %}
> /dagster-integrations The dbt assets should have a group name of "transformation"
```

The agent updates the Component configuration. With YAML-based config, this typically means adding a `translation` block that sets the group name for all assets produced by the Component:

```yaml
attributes:
  project: '{{ context.project_root }}/dbt_project'
  translation:
    group_name: transformation
```

Once applied, all dbt assets appear under the **transformation** group in the Dagster UI, visually separated from the raw ingestion layer.

![Asset graph with dbt assets in the transformation group](/images/ai-driven-data-engineering/lesson-6/project-dbt-translator.png)

## Add dbt tests

Data quality checks catch problems before they propagate downstream. Adding `not_null` and `unique` tests on id columns is a good starting point—they're low effort and catch a large class of real problems:

```bash {% obfuscated="true" %}
> /dagster-integrations Include some dbt tests to ensure that there are not NULLs for the id columns
```

The agent adds the appropriate dbt tests to your models. When the dbt Component is configured to expose tests as Dagster asset checks, those tests run as part of your graph and show up in the UI alongside the assets they validate. You get dbt's semantics and Dagster's visibility and dependency tracking at the same time.

After these three changes, open the asset catalog and take stock of what you've built. You should see the raw assets and dbt models connected with the right dependencies, the dbt group organized separately, and test checks associated with the staging models. If anything looks off, that's a prompt away from being fixed.
