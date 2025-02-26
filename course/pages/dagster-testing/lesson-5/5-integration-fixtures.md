---
title: 'Lesson 5: Integration fixtures'
module: 'dagster_testing'
lesson: '4'
---

# Integration fixtures

Because we will always need Docker to run Postgres for this test, we can create a pytest fixture to ensure the test handles the management of Docker. We will take the CLI command we used before and write a fixture around them:

```python
@pytest.fixture(scope="session", autouse=True)
def docker_compose():
    # Start Docker Compose
    file_path = Path(__file__).absolute().parent / "docker-compose.yaml"
    subprocess.run(
        ["docker", "compose", "-f", file_path, "up", "--build", "-d"],
        check=True,
        capture_output=True,
    )

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
    subprocess.run(["docker", "compose", "-f", file_path, "down"], check=True)
```

The code above does the following:

1. Gets the file path of the `docker-compose.yaml` relative to the test (which is in the same directory)
2. Starts the Docker service using the `docker compose` command
3. Waits for the service to be ready by checking when the database is ready using `pg_isready`
4. Yields to the test execution (running the test)
5. Spins down the Docker service when testing has completed

Now that fixture can be used within the parameters of the integration test and couple our test and the underlying services:

```python
def test_state_population_database(docker_compose):  # noqa: F811
    postgres_resource = PostgresResource(
        host="localhost",
        user="test_user",
        password="test_pass",
        database="test_db",
    )

    result = assets.state_population_database(postgres_resource)
    assert result == [
        ("New York", 8804190),
        ("Buffalo", 278349),
    ]
```

Also because our pytest fixture is scoped to the session, it will remain active for all the tests run. This can be very helpful because you may notice these tests take longer than the unit tests. Most of this is the set up time to spin up the necessary services (the tests themselves are relatively quick).

Scoping everything to the session ensures that we do not have to needlessly spin the services up and down for each test.