---
title: 'Lesson 5: Configuring integration tests'
module: 'dagster_testing'
lesson: '5'
---

# Configuring integration tests

As already mentioned, Postgres is an open source database with a publicly available distribution. This includes a [Docker](https://www.docker.com/) image we can use for testing purposes.

Docker is an open-source platform that allows developers to run applications in lightweight, portable containers. It is a great way to run ephemeral versions of services we need for tests.

## Docker configuration

{% callout %}

> 💡 **Docker:** We will not go into too much detail about Docker. The important thing to see is how it can help build more elaborate integration tests.

> {% /callout %}

In order to configure Docker, let's think about what we need.

1. A service running Postgres.
2. A seeded table `data.city_population` with some sample records to query.

To begin we will create a `docker-compose.yml`. This defines all the Docker services needed to run our integration test. In this case it is just the Postgres database:

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

If you are familiar with Docker you will notice that we give it build context directory rather than an image. That build context contains a Dockerfile file that contains the Postgres image and a initialization file.

```yaml
FROM postgres:17-alpine

COPY postgres_bootstrap.sql /docker-entrypoint-initdb.d/
```

This two step build does two things. Uses the `postgres:17-alpine` image and copies ane executes the `postgres_bootstrap.sql` file which will seed the database. This SQL file creates the schema, table and inserts a few sample records.

```sql
CREATE SCHEMA data;

CREATE TABLE data.city_population (
    state_name VARCHAR(100),
    city_name VARCHAR(100),
    population INT
);

INSERT INTO data.city_population VALUES
('NY', 'New York', 8804190),
('NY', 'Buffalo', 278349),
('CA', 'Los Angeles', 3898747);
```

## Executing Docker

That is all the configuration required for Docker. We can now spin up the Postgres database with the Docker CLI:

```bash 
> docker compose up -d
[+] Running 2/2
 ✔ Network dagster_testing_tests_default  Created                                                   0.0s
 ✔ Container postgresql                   Started                                                   0.2s
```

The `-d` flag will run the resource in the background. If this is the first time you have run this service it may take a little longer as your machine will need to pull the Postgres image and initialize the database. But it will be faster in subsequent runs.

If we need to stop the Docker service we can run:

```bash
docker compose down
```

## Running Docker tests

With Docker running Postgres, we can define a test that initializes the `PostgresResource` resource.

```python
def test_state_population_database():
    postgres_resource = PostgresResource(
        host="localhost",
        user="test_user",
        password="test_pass",
        database="test_db",
    )

    result = integration_assets.state_population_database(postgres_resource)
    assert result == [
        ("New York", 8804190),
        ("Buffalo", 278349),
    ]
```

You can see all the parts of the testing code working together.

![Docker Test](/images/dagster-testing/lesson-5/docker-test.png)

1. The `postgres_resource` is initialized using the connection details of the Docker compose service.
2. The results of the Postgres database are those set in the SQL script.

We can confirm everything is working with pytest.

```bash
> pytest dagster_testing_tests/test_lesson_5.py::test_state_population_database
...
dagster_testing_tests/test_lesson_5.py .                                                          [100%]
```
