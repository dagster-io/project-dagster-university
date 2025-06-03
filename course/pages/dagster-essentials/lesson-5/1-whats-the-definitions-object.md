---
title: "Lesson 5: What's the Definitions object?"
module: 'dagster_essentials'
lesson: '5'
---

# What's the Definitions object?

Whenever you define an asset, resource, or schedule in your Dagster deployment, it needs to be part of a `Definitions` object for the code location you’re working in. Each code location can only have a single Definitions object. This object maps to one code location. With code locations, users isolate multiple Dagster projects from each other without requiring multiple deployments. You’ll learn more about code locations a bit later in this lesson.

Let’s use our cookie example to demonstrate. In this case, our cookie assets - like our dry and wet ingredients, cookie dough, chocolate chip cookie dough, and eventually, chocolate chip cookies - can all be thought of as (cookie) **definitions:**

![In this example, our cookie assets, like our dry and wet ingredients, can be likened to Dagster definitions](/images/dagster-essentials/lesson-5/cookie-definitions.png)

In Dagster, the `Definitions` object is located in the `definitions.py` file. If we wanted to create a `Definitions` object for the cookie definitions it would look something like this:

```python
import dagster_cookies.defs as defs

defs = dg.components.load_defs(defs)
```

We do not need to explicitly list all the assets in our project. Dagster can automatically load most objects (we will later see there are other object types besides assets) by importing the contents of the `defs` module.

Remember that using `dg scaffold` has been placing all our asset files within the `defs` directory.

```
.
└── dagster_essentials
    └── defs
        └── assets
            ├── __init__.py
            ├── constants.py
            ├── metrics.py
            └── trips.py
```

You’ll only have one code location (and therefore one `Definitions` object) in this course, but as your project grows, you’ll need to update the `Definitions` object to include new definitions.

---

## How Dagster uses the Definitions object

Now that we’ve discussed what the `Definitions` object is, let’s go into how Dagster uses it.

When running `dg dev`, Dagster looks to the `pyproject.toml` file. This file contains all of the Python dependencies necessary to run Dagster as well as Dagster specific settings on where the `Definitions` object should be loaded.

```yaml
[tool.dg]
directory_type = "project"

[tool.dg.project]
root_module = "dagster_essentials"
code_location_target_module = "dagster_essentials.definitions"
```

In your project, open the `dagster_university/dagster_essentials/definitions.py` file. It should look like the following code:

```python
import dagster as dg

import dagster_essentials.defs


@dg.definitions
def defs():
    return dg.load_defs(defs_root=dagster_essentials.defs)
```
