---
title: 'Extra credit: dbt component'
module: 'dbt_dagster'
lesson: 'extra-credit'
---

# dbt component

We will be working with the dbt component, which will replace almost all of the code previously needed for dbt assets and the dbt resource.

First, we’ll create a directory for the component code called `components`. Inside this directory, we'll add another directory, `defs`, which will contain a `dbt` directory with a component.yaml file.

To make this importable in Python, we’ll also include `__init__.py` files within the directories. The final structure should look like this.

```
components
├── __init__.py
└── defs
    ├── __init__.py
    └── dbt
        └── component.yaml
```

The `component.yaml` file will contain all of the configuration for our dbt project. To begin we will give it a component type and the location of our dbt project.

```yaml
type: dagster_components.dagster_dbt.DbtProjectComponent

attributes:
  dbt:
    project_dir: ../../../analytics
```

That is all we need. It not look like much now, but we can now use this to replace a lot of existing code in our Dagster project.

## Update definitions object

Next we will go back to the `definitions.py` of our project. It should look something like this.

```python
defs = dg.Definitions(
    assets=[*trip_assets, *metric_assets, *requests_assets, *dbt_analytics_assets],
    resources={
        "database": database_resource,
        "dbt": dbt_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
    sensors=all_sensors,
)
```

We want to replace all dbt code we had written with components. So let's remove `*dbt_analytics_assets*` from the assets parameter and the `dbt` from the resource mapping.

```python
defs = dg.Definitions(
    assets=[*trip_assets, *metric_assets, *requests_assets],
    resources={
        "database": database_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
    sensors=all_sensors,
)
```

Now, we need to include the component code. Since components are designed to work alongside other components, the object they return is a Dagster `Definitions`.

We already have a Definitions object that includes our non-dbt assets, jobs, schedules, and sensors. To integrate our component definitions into a single definition, we’ll use `dg.Definitions.merge()` to combine everything.

First import the components module in the `definitions.py` file. We will also need the `load_defs` function from `dagster_components`.

```python
from dagster_components import load_defs
import dagster_and_dbt.components.defs
```

Next update the definitions object to merge and include the components module with `load_defs`.

```python
defs = dg.Definitions.merge(
    dg.Definitions(
        assets=[*trip_assets, *metric_assets, *requests_assets,],
        resources={
            "database": database_resource,
        },
        jobs=all_jobs,
        schedules=all_schedules,
        sensors=all_sensors,
    ),
    load_defs(dagster_and_dbt.components.defs),
)
```

This all we need to do. With just a few lines of YAML and some small tweaks to the project definitions, we have replaced all of our dbt code!

You can now launch `dagster dev` to view the assets.

# Asset attributes

If you look at the asset graph right now, it may not look quite correct.

![Asset graph no attribute mapping](/images/dagster-dbt/extra-credit/before-asset-attributes.png)

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

Implementing an entire `DagsterDbtTranslator` class can be cumbersome. Instead we will include the mapping in our `components.yaml` file.

The most import part of the `DagsterDbtTranslator` we want is prefacing `taxi_` to the name of assets for mapping. In the translator that is handled with the line.

```python
return dg.AssetKey(f"taxi_{name}")
```

We will take that logic and add it component yaml.

```yaml
type: dagster_components.dagster_dbt.DbtProjectComponent

attributes:
  dbt:
    project_dir: ../../../analytics
  asset_attributes:
    key:  "taxi_{{ node.name }}"
```

That is all we need to do. Again we can see much work can get saved with components. If we launch `dagster dev` again and see that everything now lines up.

![Asset graph attribute mapping](/images/dagster-dbt/extra-credit/after-asset-attributes.png)
