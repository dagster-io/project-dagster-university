---
title: "Lesson 2: Set up with Github Codespaces"
module: 'dagster_etl'
lesson: '2'
---

# Set up with Github Codespace

Instead of you setting up a local environment, you can use [Github Codespaces](https://github.com/features/codespaces). This will allow you to work through this course and edit code in this repository in a cloud based environment.

## Creating a Github Codespace

There are unique Codespaces for the different courses in Dagster University. Be sure to select the create one creating a Codespace.

1. While logged into Github, go to the [Codespaces page](https://github.com/codespaces).
2. In the top right, select "New Codespace"
3. Create a Codespace using the following.

    | Field | Value |
    |--- | --- |
    | Repository | dagster-io/project-dagster-university |
    | Branch | main |
    | Dev container configuration | Dagster & ETL |
    | Region | US East |
    | Machine type | 2-core |

    ![Codespace Create](/images/shared/codespaces/codespaces-create.png)

4. Click "Create codespace"

The first time you create a codespace it may take a minute for everything to start. You will then be dropped in an interactive editor containing the code for the entire Dagster University repository.

## Working in the Codespace

In the terminal of the Codespace IDE the bottom navigate to the specific course.

```bash
cd dagster_university/dagster_and_etl
```

To ensure everything is working you can launch the Dagster UI.

```bash
dagster dev
```

After Dagster starts running you will be prompted to open the Dagster UI within your browser. Click "Open in Browser".

![Codespace Launch](/images/shared/codespaces/codespaces-launch.png)

## Stopping your Github Codespace

Be sure to stop your Codespace when you are not using it. Github provides personal accounts [120 cores hours per month](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces#monthly-included-storage-and-core-hours-for-personal-accounts).

![Stop Codespace](/images/shared/codespaces/codespaces-stop.png)
