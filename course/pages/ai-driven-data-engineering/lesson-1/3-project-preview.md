---
title: "Lesson 1: Project preview"
module: 'ai_driven_data_engineering'
lesson: '1'
---

# Project preview

This course is **not** primarily a deep dive into Dagster fundamentals. For that, we recommend [Dagster Essentials](https://courses.dagster.io/courses/dagster-essentials), where you'll learn assets, resources, schedules, partitions, and more from the ground up.

What this course *is* about is showing you how quickly a modern AI-driven workflow can get you from a blank directory to a production-quality Dagster project—one you'd actually deploy.

---

## What we're building

Over the course of these lessons, you'll build a complete **end-to-end ELT pipeline** for a fictional e-commerce company. The pipeline has three stages:

**Extract and load** — Three raw assets pull CSV data from the web and load it into DuckDB tables: customers, orders, and payments. These form the foundation of everything downstream.

**Transform** — A dbt project takes those raw tables and builds staging models (`stg_customers`, `stg_orders`, `stg_payments`) that clean and standardize the data, then a final `fct_orders` model that joins them together into something analysts can actually use.

**Export** — A Sling component reads the finished `fct_orders` table from DuckDB and exports it to S3 as a Parquet file, ready for downstream consumption by BI tools or other pipelines.

By the end, your asset graph will look like this:

![Finished asset graph](/images/ai-driven-data-engineering/lesson-5/project-dbt-sling.png)

The raw assets feed into the dbt models, which feed into the Sling export. Every piece of data is represented as an asset with explicit dependencies, giving you a complete picture of your pipeline at a glance.

---

## How we'll build it

Here's the part that makes this course different: **we'll build this entire pipeline from prompts**, not by writing code by hand.

Using a coding agent equipped with Dagster skills and the `dg` CLI, you'll take that blank project to a fully wired ELT solution by describing what you want and letting the agent scaffold, write, and validate the code. You'll watch it install dependencies, scaffold files in the right locations, validate definitions, and suggest next steps—all because the skills and CLI give it the right context to do that work correctly.

That means you'll spend your energy thinking about your data—what you need, how it should flow, where it should land—rather than remembering which APIs to call or which file to edit.

---

## What's ahead

Before we build anything, we'll set up the tools (Lesson 2) and take a tour of the Dagster AI ecosystem so you understand how the pieces fit together (Lesson 3). Then in Lessons 4 and 5 you'll build the pipeline step by step, and Lesson 6 closes out with a code quality pass using the `dignified-python` skill.

By the end you'll have a real project—not a toy example—built the way Dagster recommends, from a series of prompts.

As you get more comfortable, diving into [Dagster Essentials](https://courses.dagster.io/courses/dagster-essentials) or the specific docs will help you understand *why* things are structured the way they are and how to customize further. But you don't need to wait for that to start shipping.
