---
title: "Lesson 5: Modifying our project"
module: 'ai_driven_data_engineering'
lesson: '5'
---

# Modifying our project

Once the dbt Component and models are in place, you can refine the project with follow-up prompts. The **`dagster-integrations`** skill knows how to wire dependencies, set asset metadata (like group names), and add dbt tests.

---

## Connect dbt assets to the raw assets

First, make sure the dbt assets are correctly dependent on the raw assets so that materializing the dbt models runs after the raw tables are populated:

```bash
/dagster-integrations Connect the dbt assets to the raw assets
```

The agent will ensure the Dagster asset graph has the right edges: raw assets → dbt staging (and downstream) models. That might involve updating the Component config or the definitions that load the dbt project.

---

## Set a group name for dbt assets

To keep the UI organized, put the dbt-derived assets in a group (e.g. `transformation`):

```bash
/dagster-integrations The dbt assets should have a group name of "transformation"
```

The agent will update the Component configuration. With YAML-based config, the change often looks like adding a `translation` block that sets the group name for assets produced by the Component. For example, in the component’s config (e.g. in `defs.yaml` or the equivalent):

```yaml
attributes:
  project: '{{ context.project_root }}/dbt_project'
  translation:
    group_name: transformation
```

So all dbt assets show up under the **transformation** group in the Dagster UI.

![Asset graph with dbt assets in the transformation group](/images/ai-driven-data-engineering/lesson-5/project-dbt-translator.png)

---

## Include dbt tests

Add dbt tests so you can catch bad data (e.g. NULLs in id columns) as part of your pipeline:

```bash
/dagster-integrations Include some dbt tests to ensure that there are not NULLs for the id columns
```

The agent will add the appropriate dbt tests (e.g. `unique` and `not_null` on id columns) in your dbt project. When the dbt Component is configured to expose tests as Dagster assets or as check ops, those tests will run as part of your graph and show up in the UI. You get both dbt’s semantics and Dagster’s visibility and dependency tracking.
