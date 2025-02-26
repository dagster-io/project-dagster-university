---
title: 'Lesson 5: Configuring integration tests'
module: 'dagster_testing'
lesson: '4'
---

# Configuring integration tests

As already mentioned Postgres is an open source database with a publicly available distribution. This includes a [Docker](https://www.docker.com/) image we can use for testing purposes.

Docker is an open-source platform that allows developers to run applications in lightweight, portable containers. It is a great way to run ephemeral versions of services we need for tests.

## Docker configuration

To begin we will create a `docker-compose.yml`. This defines all the Docker services needed to run our integration test. In this case it will just need a postgres database:

```yaml
---

services:
  postgresql:
    build:
      context: ./postgres
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

If you are familiar with Docker you will notice that we give it build context directory rather than an image. That build context contains a Dockerfile file that contains the Postgres image and a initialize file:

```yaml
FROM postgres:17-alpine

COPY postgres_bootstrap.sql /docker-entrypoint-initdb.d/
```

We need this file to seed our database with the `data.city_population` table and some example records.

That is everything need so we can spin up the Postgres database with the Docker CLI:

```bash 
> docker compose up -d
[+] Running 2/2
 ✔ Network dagster_testing_tests_default  Created                                                   0.0s
 ✔ Container postgresql                   Started                                                   0.2s
```

The `-d` flag will run the resource in the background. If we need to stop the Docker service we can run:

```bash
docker compose down
```

## Running Docker tests

With Docker running Postgres, we can define a test that initializes the `PostgresResource` resource using the credentials defined in the compose file:

```python
def test_state_population_database():
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

This test connects to Postgres, runs the SQL query and returns results from the seeded data. We can confirm everything is working with pytest:

```bash
> pytest dagster_testing_tests/test_lesson_4.py::
test_state_population_database
...
dagster_testing_tests/test_lesson_4.py .                                                          [100%]
```
