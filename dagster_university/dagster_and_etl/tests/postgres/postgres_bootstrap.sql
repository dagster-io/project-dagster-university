CREATE ROLE replication_user WITH LOGIN REPLICATION;
GRANT CREATE ON DATABASE postgres TO replication_user;

CREATE SCHEMA IF NOT EXISTS data;

CREATE TABLE data.customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE
);

CREATE TABLE data.products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2)
);

CREATE TABLE data.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES data.customers(customer_id),
    product_id INTEGER REFERENCES data.products(product_id),
    quantity INTEGER DEFAULT 1,
    total_amount DECIMAL(10, 2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO data.customers (first_name, last_name, email) VALUES
    ('Alice', 'Johnson', 'alice.johnson@example.com'),
    ('Bob', 'Smith', 'bob.smith@example.com'),
    ('Charlie', 'Lee', 'charlie.lee@example.com');

INSERT INTO data.products (name, description, price) VALUES
    ('Wireless Mouse', 'Ergonomic wireless mouse with USB receiver', 25.99),
    ('Mechanical Keyboard', 'Backlit mechanical keyboard with blue switches', 89.50),
    ('Laptop Stand', 'Adjustable aluminum stand for laptops', 39.95);

INSERT INTO data.orders (customer_id, product_id, quantity, total_amount, order_date) VALUES
    (1, 1, 2, 51.98, '2024-05-01 10:30:00'),
    (2, 2, 1, 89.50, '2024-05-02 14:15:00'),
    (1, 3, 1, 39.95, '2024-05-03 09:00:00'),
    (3, 1, 1, 25.99, '2024-05-03 11:45:00');