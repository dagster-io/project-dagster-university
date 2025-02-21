---
title: 'Lesson 4: Integration fixtures'
module: 'dagster_testing'
lesson: '4'
---

Because we will always need Docker to run Postgres for this test, we can create a pytest fixture to ensure the test handles the starting and stopping of the service. We will take the CLI command we used before and write a fixture around that.

```python
@pytest.fixture(scope="session", autouse=True)
def docker_compose():
    # Start Docker Compose
    file_path = Path(__file__).absolute().parent / "docker-compose.yaml"
    subprocess.run(["docker-compose", "-f", file_path, "up", "-d"], check=True)

    max_retries = 5
    for i in range(max_retries):
        result = subprocess.run(
            ["docker", "exec", "postgresql", "pg_isready"],
            capture_output=True,
        )
        if result.returncode == 0:
            break
        time.sleep(5)

    yield

    # Tear down Docker Compose
    subprocess.run(["docker-compose", "-f", file_path, "down"], check=True)
```

The code above does the following:

1. Gets the file path of the `docker-compose.yaml` relative to the test (which is in the same directory)
2. Starts the Docker service using the `docker compose` command
3. Waits for the service to be ready by checking when the database is ready using `pg_isready`
4. Yields to the test execution (running the test)
5. Spins down the Docker service when testing has completed

Now that fixture can be used within our integration test and couple it together:

```python
def test_my_sql_table(docker_compose):
    postgres_resource = PostgresResource(
        host="localhost", user="test_user", password="test_pass", database="test_db"
    )

    my_sql_table(postgres_resource)
```