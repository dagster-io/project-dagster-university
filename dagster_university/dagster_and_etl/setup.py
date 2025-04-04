from setuptools import find_packages, setup

setup(
    name="dagster_and_etl",
    packages=find_packages(exclude=["dagster_and_etl_tests"]),
    install_requires=[
        "dagster==1.10.*",
        "dagster-webserver",
        "dagster-snowflake",
        "dagster-duckdb",
        "dagster-aws",
        "dagster-sling",
        "dagster-dlt",
        "psycopg2-binary",
        "dlt[duckdb]",
        "pandas",
    ],
    extras_require={"dev": ["ruff", "pytest"]},
)
