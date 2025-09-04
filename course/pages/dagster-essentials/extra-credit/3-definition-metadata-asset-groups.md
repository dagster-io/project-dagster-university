---
title: 'Extra credit: Definition metadata - Asset groups'
module: 'dagster_essentials'
lesson: 'extra-credit'
---

# Definition metadata - Asset groups

As you add more assets over time, it’s likely that similarities between assets will become more obvious. For example, several assets may be related to dbt or data transformation, while others may be focused on extracting raw CSV data. These could logically be classified into **asset groups.**

An asset group is a way you can keep your assets tidy and simplify keeping track of them in the UI. Additionally, asset groups can make selecting assets for a job easier, as you can refer to an asset group instead of specifying a list of assets.

There are two ways to specify asset groups in Dagster:

- On all assets in a module
- On individual assets

---

## Things to note

When adding assets to groups, keep the following in mind:

- If an asset isn’t a member of a group, it will be placed into a group named `default`
- A single asset can only belong to one group at a time

---

## Grouping individual assets using the asset decorator

You can also specify groups on individual assets by using the `group_name` parameter in the asset decorator. For example:

```python
# src/dagster_essentials/defs/assets/trips.py
import dagster as dg

@dg.asset(
    group_name="raw_files",
)
def taxi_zones_file() -> None:
    """
      The raw CSV file for the taxi zones dataset. Sourced from the NYC Open Data portal.
    """
    raw_taxi_zones = requests.get(
        "https://community-engineering-artifacts.s3.us-west-2.amazonaws.com/dagster-university/data/taxi_zones.csv"
    )

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as output_file:
        output_file.write(raw_taxi_zones.content)
```

In this example, the `taxi_zones_file` asset is grouped into the `raw_files` asset group.

---

## Grouping assets using the `DefsFolderComponent`

Another option is to include the `group_name` at the directory level. Here, you can specify metadata for all of your assets using YAML. To do this, create a new file within the `src/dagster_essentials/defs/` directory called `defs.yaml`:

```yaml
# src/dagster_essentials/defs/defs.yaml
type: dagster.DefsFolderComponent

post_processing:
  assets:
    - target: "taxi_zones_file"
      attributes:
        group_name: "raw_files"
```

This allows you to name assets in your project and associate various metadata with them.

With this approach, you can include multiple metadata attributes for your assets. For example, if you also want to add a tag for the course name to all assets in your project, you can extend the YAML as follows:

```yaml
# src/dagster_essentials/defs/defs.yaml
type: dagster.DefsFolderComponent

post_processing:
  assets:
    - target: "taxi_zones_file"
      attributes:
        group_name: "raw_files"
    - target: "*"
      attributes:
        tags:
          course: "dagster_essentials"
```

Adding the `defs.yaml` file is an example of a [Dagster Component](https://docs.dagster.io/guides/build/components). Components provide a way to intelligently manage your project layout by using YAML DSLs to dynamically generate Dagster code. In this case, we are using the `DefsFolderComponent`.

**Note:** This course does not cover components in depth. For a more detailed example of using components, see the [Dagster & ETL course](https://courses.dagster.io/courses/dagster-etl).

---

## Asset groups in the Dagster UI

When asset groups are defined, the **Global Asset Lineage** page will place group members into separate grey boxes. For example, the following image shows three asset groups:

- `raw_files`, which currently includes only `taxi_zones_file`
- `metrics`, which includes all assets from the `metrics` submodule
- `default`, which includes the assets that don’t currently belong to a group. **Note**: If no other asset groups are defined, the `default` group won’t display here.

![The Global Asset Lineage page with three defined asset groups](/images/dagster-essentials/extra-credit/ui-asset-groups.png)
