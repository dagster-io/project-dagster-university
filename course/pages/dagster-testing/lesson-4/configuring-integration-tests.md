---
title: 'Lesson 4: Configuring Integration Tests'
module: 'dagster_testing'
lesson: '4'
---

As already mentioned Postgres is an open source database. As such there are many free and publicly available distributions of it, including [Docker](https://www.docker.com/). Docker will allow us to spin up a Postgres database for the purposes of testing.

To begin we will define a `docker-compose.yml`. This defines all the Docker services needed to run our integration test. In this case it will just need a postgres database:

```yaml
---
version: "3.9"

services:
  postgresql:
    image: postgres:latest
    container_name: postgresql
    environment:
      POSTGRES_DB: "test_db"
      POSTGRES_USER: "test_user"
      POSTGRES_PASSWORD: "test_pass"
    ports:
      - "5432:5432"
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
```

Now we can define a test and provide it with the initialized PostgresResource resource. In this case because the `database` resource is specific to the test, we can hardcode the values to match the connection details defined in the Docker Compose:

```python
def test_my_sql_table():
    postgres_resource = PostgresResource(
        host="localhost", user="test_user", password="test_pass", database="test_db"
    )

    my_sql_table(postgres_resource)
```

In order to run this test we will need that Docker service running. To do this we will just need to run the following from the test directory:

```bash 
> docker compose up -d
[+] Running 2/2
 ✔ Network dagster_testing_tests_default  Created                                                   0.0s
 ✔ Container postgresql                   Started                                                   0.2s
```

The `-d` flag will just run the resource in the background. And if we need to stop the Docker service we can run:

```bash
docker compose down
```

## Fixture

Because we need Docker to be running for this test to execute, we can write a pytest fixture to ensure it spins up and down during the duration of the test. We will take the CLI command we used above and write a fixture around that.

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
2. Starts the Docker service using the `docker-compose` command
3. Waits for the service to be ready
4. Yields to the test execution
5. Spins down the docker compose service when testing has completed

Now that fixture can be used within our integration asset test to couple it directly with the Docker compose:

```python
def test_my_sql_table(docker_compose):
    postgres_resource = PostgresResource(
        host="localhost", user="test_user", password="test_pass", database="test_db"
    )

    my_sql_table(postgres_resource)
```