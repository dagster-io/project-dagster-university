# Testing with Dagster

## Overview

Learn how to write tests in Python and apply them to Dagster. In this course, you'll learn how to write unit, mock and integration tests in the context of Dagster and the best practices to ensure high quality for your Dagster project.

## Completed code

Most of this module involves running tests with [`pytest`](https://docs.pytest.org/en/stable/). The code you will be testing is located within `dagster_testing`. The tests are in `tests`. Each lesson has its own file for tests.

```
tests
├── test_lesson_3.py
├── test_lesson_4.py
├── test_lesson_5.py
└── test_lesson_6.py
```

The completed tests are located within a subdirectory `completed`.

```
tests
└── completed
    ├── test_lesson_3.py
    ├── test_lesson_4.py
    ├── test_lesson_5.py
    └── test_lesson_6.py
```

## Dagster UI

You should not need to use the UI for this module but if you want to see Dagster objects you can execute.

```bash
dg dev
```

Open http://localhost:3000 with your browser to see the project.
