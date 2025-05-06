-- https://dlthub.com/docs/dlt-ecosystem/verified-sources/pg_replication#setup-user
CREATE ROLE replication_user WITH LOGIN REPLICATION;

GRANT CREATE ON DATABASE postgres TO replication_user;

-- Seed data

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
