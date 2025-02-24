---
title: 'Lesson 4: Overview'
module: 'dagster_testing'
lesson: '4'
---

# Overview

By this point you should feel comfortable writing unit tests for your assets, even those that rely on external systems. However while it helpful to know how tests function with expected results, it can still be good to have tests that function by talking to actual systems. These tests usually require more set up and tend to be run less often than unit tests, but they add another level of safety for our code before it reaches production.