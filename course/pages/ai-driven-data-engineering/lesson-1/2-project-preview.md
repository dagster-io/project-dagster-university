---
title: "Lesson 1: Project preview"
module: 'ai_driven_data_engineering'
lesson: '1'
---

## What we're building

Over the course of these lessons, you'll build a complete end-to-end ELT pipeline for a fictional e-commerce company. The pipeline has three stages:

Extract and load — Raw assets pull data from the web and load it into DuckDB tables.
Transform — A dbt project takes those raw tables and builds staging models and final models.
Export — A Sling component that reads the finished model from DuckDB and exports it to S3 as a Parquet file, ready for downstream consumption by BI tools or other pipelines.

By the end, your asset graph will look like this:

[Final Asset Graph](/images/ai-driven-data-engineering/lesson-3/final-dag.png)

But you will also know enough about how to use AI and Dagster to easily extend it to do just about anything.

## How we'll build it

Here's the part that makes this course different from other Dagster University courses: we'll build this entire pipeline from prompts, not by writing code by hand.

Using a coding agent equipped with Dagster skills and the `dg` CLI, you'll take that blank project to a fully wired ELT solution by describing what you want and letting the agent scaffold, write, and validate the code. You'll watch it install dependencies, scaffold files in the right locations, validate definitions, and suggest next steps—all because the skills and CLI give it the right context to do that work correctly.

That means you'll spend your energy thinking about your data—what you need, how it should flow, where it should land—rather than remembering which APIs to call or which file to edit.

## What's ahead

Before we build anything, we'll set up the tools (Lesson 2) and take a tour of the Dagster AI ecosystem so you understand how the pieces fit together (Lesson 3). Then in Lessons 4 and 5 you'll build the pipeline step by step, and Lesson 7 closes out with a code quality pass using the `dignified-python` skill.

By the end you'll have a real project—not a toy example—built the way Dagster recommends, from a series of prompts.

As you get more comfortable, diving into [Dagster Essentials](https://courses.dagster.io/courses/dagster-essentials) or the specific docs will help you understand *why* things are structured the way they are and how to customize further. But you don't need to wait for that to start shipping.
