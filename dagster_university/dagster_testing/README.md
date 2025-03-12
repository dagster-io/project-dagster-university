# [WIP] Testing with Dagster

> [!NOTE]  
> This module is currently a work in progress.

## Completed code

Most of this module involves running tests with [`pytest`](https://docs.pytest.org/en/stable/). The code you will be testing is located within `dagster_testing`. The tests are in `dagster_testing_tests`. Each lesson has its own file for tests.

```
dagster_testing_tests
├── test_lesson_3.py
├── test_lesson_4.py
├── test_lesson_5.py
└── test_lesson_6.py
```

The completed tests are located within a subdirectory `completed`.

```
dagster_testing_tests
├── completed
│   ├── test_lesson_3.py
│   ├── test_lesson_4.py
│   ├── test_lesson_5.py
│   └── test_lesson_6.py
```

## Dagster UI

You should not need to use the UI for this module but if you want to see Dagster objects you can execute.

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.
