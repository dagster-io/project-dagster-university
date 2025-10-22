---
title: "Lesson 5: Overview"
module: 'dagster_etl'
lesson: '5'
---

# Overview

The pipelines we've built so far are great for learning the foundations of ETL pipeline construction and exploring how to apply various Dagster features. However, these aren't necessarily the kinds of pipelines you’d want to deploy directly to production. The main issue is that we're reinventing too many parts of the ETL process, developing logic and handling edge cases that could be handled more efficiently with existing tools.

The good news is that ETL is a universal problem, one that nearly every data-driven organization faces. As a result, a wide range of tools and frameworks have emerged to simplify and standardize ETL workflows, from data extraction and transformation to orchestration and monitoring. Leveraging these tools not only reduces boilerplate and bugs, but also allows you to focus on the parts of the pipeline that are unique to your business logic.
