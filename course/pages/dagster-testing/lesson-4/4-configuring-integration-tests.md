---
title: 'Lesson 4: Configuring Integration Tests'
module: 'dagster_testing'
lesson: '4'
---

As already mentioned Postgres is an open source database with a publicly available distribution. This includes a [Docker](https://www.docker.com/) image we can use.

Docker is an open-source platform that allows developers to run applications in lightweight, portable containers. It is a great way to run ephemeral versions of services we need for tests.

## Docker configuration

To begin we will create a `docker-compose.yml`. This defines all the Docker services needed to run our integration test. In this case it will just need a postgres database:

```yaml
---

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

We can spin up the Postgres database with the Docker CLI:

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

## Running Docker tests

With Docker running Postgres, we can define a test that initializes the `PostgresResource` resource using the credentials defined in the compose file:

```python
def test_my_sql_table():
    postgres_resource = PostgresResource(
        host="localhost", user="test_user", password="test_pass", database="test_db"
    )

    my_sql_table(postgres_resource)
```

This test will now connect to Postgres to run the SQL query in our asset. We can see that with pytest:

```
```bash
> pytest dagster_testing_tests/test_lesson_4.py::
test_my_sql_table
...
dagster_testing_tests/test_lesson_4.py .                                                          [100%]
```

Because this test actually relies on an external system it takes a little longer to run than the unit tests we have been writing so far.
