---
title: "Lesson 6: Sling database replication set up"
module: 'dagster_etl'
lesson: '6'
---

# Sling database replication set up

For this course, we’ll keep things lightweight by using a simple Postgres database with a basic schema and a few rows of sample data, just enough to confirm that everything is working correctly.

One of the easiest ways to spin up a temporary database is with [Docker](https://www.docker.com/). We’ve provided a pre-configured Docker Compose file that starts a Postgres container and automatically seeds it with data.

To get started, run the following command:

```bash
docker compose -f dagster_and_etl_tests/docker-compose.yaml up -d
```

**Note:** The first time you run this command, Docker may need to download the required image, so it could take a few minutes.

This Docker Compose will launch a Postgres instance and populate it with a small schema containing a few sample tables and rows, perfect for development and testing.

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
