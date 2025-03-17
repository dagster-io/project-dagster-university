---
title: "Lesson 5: What's the Definitions object?"
module: 'dagster_essentials'
lesson: '5'
---

# What's the Definitions object?

A `Definitions` object is a set of Dagster definitions available and loadable by Dagster tools. The `Definitions` object is used to assign definitions to a code location, and each code location can only have a single `Definitions` object. This object maps to one code location. With code locations, users isolate multiple Dagster projects from each other without requiring multiple deployments. You’ll learn more about code locations a bit later in this lesson.

Let’s use our cookie example to demonstrate. In this case, our cookie assets - like our dry and wet ingredients, cookie dough, chocolate chip cookie dough, and eventually, chocolate chip cookies - can all be thought of as (cookie) **definitions:**

![In this example, our cookie assets, like our dry and wet ingredients, can be likened to Dagster definitions](/images/dagster-essentials/lesson-5/cookie-definitions.png)

In Dagster, the `Definitions` object is located in the `definitions.py` file. If we wanted to create a `Definitions` object for the cookie definitions we have so far, it would look something like this:

```python
defs = Definitions(
    assets=[
        dry_ingredients,
        wet_ingredients,
        chocolate_chips,
        cookie_dough,
        chocolate_chip_cookie_dough,
        chocolate_chip_cookies,
    ]
)
```

Note that assets aren’t the only type of definition in Dagster: there are also others like resources, schedules, and sensors. We’ll go into detail on each of these in later lessons, but for now, keep this in mind.

You’ll only have one code location (and therefore one `Definitions` object) in this course, but as your project grows, you’ll need to update the `Definitions` object to include new definitions.

---

## How Dagster uses the Definitions object

Now that we’ve discussed what the `Definitions` object is, let’s go into how Dagster uses it.

When running `dagster dev`, Dagster looks to the `pyproject.toml` file. This file contains all of the Python dependencies necessary to run Dagster as well as Dagster specific settings on where the `Definitions` object should be loaded.

```yaml
[tool.dagster]
module_name = "dagster_essentials.definitions"
code_location_name = "dagster_essentials"
```

In your project, open the `dagster_university/definitions.py` file. It should look like the following code:

```python
import dagster as dg

from .assets import trips, metrics

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules([metrics])

defs = dg.Definitions(
    assets=[*trip_assets, *metric_assets]
)
```

---

## Anatomy of the `definitions.py` file

Let’s break down this file’s code line-by-line.

The following line introduces the `Definitions` object we were talking about. It also imports a method called `load_assets_from_modules`, which we’ll use to tell Dagster to retrieve the assets you defined:

```python
import dagster as dg
```

Following Dagster’s recommended file structure, assets should be stored in a separate Python module. In this example, we used Python’s relative import functionality to import the `trips` and `metrics` sub-modules from the `.assets` module:

```python
from .assets import trips, metrics
```

These lines use the `load_assets_from_modules` function to store the assets into variables called `trip_assets` and `metric_assets`:

```python
trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules([metrics])
```

When loading a code location, Dagster looks for a variable that contains a `Definitions` object. This is the most important section of the `definitions.py` file. Here, everything is combined and added into the `Definitions` object.

The `Definitions` object takes multiple arguments, one for each of the possible Dagster definitions (ex., `assets`, `resources`, `schedules`). In this case, we passed in the assets we loaded into the `assets` argument:

```python
defs = dg.Definitions(
    assets=[*trip_assets, *metric_assets],
)
```
