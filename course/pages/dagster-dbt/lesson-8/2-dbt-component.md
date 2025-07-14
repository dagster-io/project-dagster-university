---
title: 'Lesson 8: dbt component'
module: 'dbt_dagster'
lesson: '8'
---

# dbt component

We will be working with the dbt component, which will replace most of the code previously needed for dbt assets and the dbt resource.

## What are components?

You might be wondering what components are and how they can help with this project. Components provide a structured, opinionated project layout that supports scaffolding in Dagster. They simplify the process by transforming configuration files (like YAML) into Dagster definitions, eliminating unnecessary code. This is especially useful for integrations that follow common patterns—dbt being a great example.

In our dbt project, most of the logic was contained within our SQL models, and the mapping of Dagster onto our project followed a standard approach.

With components, much of the boilerplate code we previously had to write is removed, allowing us to get up and running much faster.

## dbt Component Scaffolding

First, we will use the `dg` command to scaffold a dbt component.

```bash
dg scaffold defs dagster_dbt.DbtProjectComponent transform --project-path src/dagster_and_dbt/analytics
```

This will add a new directory and file to the Dagster project.

```
src
└── dagster_and_dbt
    └── defs
        └── transform
            └── defs.yaml
```

The `defs.yaml` contain all of the configuration necessary for our dbt component.

```yaml
type: dagster_dbt.DbtProjectComponent

attributes:
  project: '{{ project_root }}/src/dagster_and_dbt/analytics'
```

The `project` attribute is the location of the dbt project (which we specified with the `dg` command). The component is responsible for handling the rest and turns this dbt project into assets.

Nothing else needs to be configured. It may not look like much now, but we can now use this component to replace a lot of existing code in our Dagster project.

## Code cleanup

Almost all of the code we had written around our dbt assets can now be replaced. To begin, remove the following files:

* `src/dagster_and_dbt/defs/project.py`
* `src/dagster_and_dbt/defs/assets/dbt.py`

These are no longer necessary since generating the dbt assets is handled by the component. Likewise we no longer need an explicit dbt resource. You can remove the dbt resource from the `src/dagster_and_dbt/defs/resources.py` which should currently look like this.

```python
@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "database": database_resource,
            "dbt": dbt_resource, # can be removed
        },
    )
```

The dbt component replaces all of this code with just a few lines of YAML! You can now launch `dg dev` to view the assets.

## Asset mapping

If you look at the asset graph right now, it may not look quite correct.

![Asset graph no attribute mapping](/images/dagster-dbt/lesson-8/before-asset-attributes.png)

All of the assets from our dbt project are present but they are not lining up with the non dbt assets how we want.

You might remember that we encountered this problem before. In order our assets to properly map to each other we needed to create a `DagsterDbtTranslator` class with a `get_asset_key` key method.

This is what Dagster used to handle the mapping of our source assets to the dbt model assets.

```python
class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):
    ...
    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if resource_type == "source":
            return dg.AssetKey(f"taxi_{name}")
        else:
            return super().get_asset_key(dbt_resource_props)
```

Implementing an entire `DagsterDbtTranslator` class can be cumbersome. Instead we will include the mapping in our `defs.yaml` file.

The most import part of the `DagsterDbtTranslator` we want is prefacing `taxi_` to the name of assets for mapping. In the translator that is handled with the line.

```python
return dg.AssetKey(f"taxi_{name}")
```

We will take that logic and add it component yaml.

```yaml
type: dagster_dbt.DbtProjectComponent

attributes:
  project: '{{ project_root }}/src/dagster_and_dbt/completed/lesson_8/analytics'
  translation:
    key:  "taxi_{{ node.name }}"
```

That is all we need to do. Again we can see much work can get saved with components. If we launch `dagster dev` again and see that everything now lines up.

![Asset graph attribute mapping](/images/dagster-dbt/lesson-8/after-asset-attributes.png)
