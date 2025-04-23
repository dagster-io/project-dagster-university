---
title: "Lesson 7: Pushing the project to GitHub"
module: 'dbt_dagster'
lesson: '7'
---

# Pushing the project to GitHub

We’ll be using GitHub in this lesson because Dagster+ has a native integration with GitHub to quickly get deployment set up. This functionality can be easily replicated if your company uses a different version control provider, but we’ll standardize on using GitHub for now. Whether you use the command line or an app like GitHub Desktop is up to you.

Because you cloned this project, it’ll already have a git history and context. Let’s use a new repository on GitHub, instead.

1. Create the repository in GitHub, then clone it to your workstation.
2. Copy the contents of `project-dagster-university/dagster_university/dagster_and_dbt/` from the Dagster University cloned repo into the root of your new repository. For example, `cp -R ~/project-dagster-university/dagster_university/dagster_and_dbt/* ~/my-dagster-and-dbt-repo/`.
3. To avoid committing environment variables or a large DuckDB file, copy the .gitignore from the Dagster University repo into your new repo. For example, `cp ~/project-dagster-university/.gitignore ~/my-dagster-and-dbt-repo/`
4. Push the code from your project into this GitHub repository’s `main` branch.

{% callout %}
> 💡 **Important!** Make sure the `.env` file in your project isn’t included in your commit! The starter project for this course should have it listed in `.gitignore`, but it’s wise to double-check before accidentally committing sensitive files.
{% /callout %}