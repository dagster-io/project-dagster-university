---
title: "Lesson 6: dlt database replication set up"
module: 'dagster_etl'
lesson: '6'
---

# dlt database replication set up

After discussing so many potential pitfalls around database replication, you might be surprised by how easy it is to configure replication using a tool like dlt.

# Source database set up

To replicate data, we first need a source database. For the purposes of this course, we’ll keep things lightweight, a simple Postgres database with a basic schema and a few rows of data, just enough to validate that everything is working correctly.

One of the easiest ways to spin up a temporary database is with [Docker](https://www.docker.com/). We’ve provided a pre-configured Docker Compose setup that will start a Postgres container and automatically seed it with some data.

To get started, run the following command:

```bash
docker compose -f dagster_and_etl_tests/docker-compose.yaml up -d
```

**Note:** The first time you run this command, Docker may need to download the required image, so it could take a few minutes.

This Docker Compose setup will launch a Postgres instance and populate it with a small schema containing a few sample tables and rows, perfect for development and testing.

`data.customers`
| Column        | Type         | Description                             |
|---------------|--------------|-----------------------------------------|
| customer_id   | `SERIAL`     | Primary key, auto-incrementing ID       |
| first_name    | `VARCHAR(100)` | Customer's first name                  |
| last_name     | `VARCHAR(100)` | Customer's last name                   |
| email         | `VARCHAR(255)` | Unique email address                   |

`data.products`
| Column        | Type             | Description                             |
|---------------|------------------|-----------------------------------------|
| product_id    | `SERIAL`         | Primary key, auto-incrementing ID       |
| name          | `VARCHAR(255)`   | Name of the product                     |
| description   | `TEXT`           | Product description                     |
| price         | `DECIMAL(10, 2)` | Product price with two decimal places   |

`data.orders`
| Column        | Type              | Description                                              |
|---------------|-------------------|----------------------------------------------------------|
| order_id      | `SERIAL`          | Primary key, auto-incrementing ID                        |
| customer_id   | `INTEGER`         | Foreign key referencing `data.customers(customer_id)`    |
| product_id    | `INTEGER`         | Foreign key referencing `data.products(product_id)`      |
| quantity      | `INTEGER`         | Quantity of product ordered, defaults to 1               |
| total_amount  | `DECIMAL(10, 2)`  | Total price for the order                                |
| order_date    | `TIMESTAMP`       | Timestamp of the order, defaults to current time         |

The specifics of the schema aren’t critical for our purposes, we just need some sample data to replicate and, most importantly, the connection details for the Postgres database running in Docker:

| Field             | Value              |
|------------------|---------------------|
| **Host**         | `localhost`         |
| **Port**         | `5432`              |
| **Database**     | `test_db`           |
| **Username**     | `test_user`         |
| **Password**     | `test_pass`         |

# dlt Set up

The next step is to initialize the dlt connection. Up to this point, we’ve been building our dlt sources from scratch, which is useful for custom integrations like the NASA API. However, for more standard use cases such as database replication, dlt provides out-of-the-box connectors that simplify the setup process.

To begin, run the following command to initialize your dlt project and generate the necessary configuration structure:

```bash
dlt init sql_database duckdb
```

This will initialize a `.dlt` directory where we can set our configuration values. We then need to update the `secrets.toml` with the connection details for our database. These will match the details of our Docker configuration.

```yaml
[sources.sql_database.credentials]
drivername = "postgresql"
database = "test_db"
password = "test_pass"
username = "test_user"
host = "localhost"
port = 5432
```
