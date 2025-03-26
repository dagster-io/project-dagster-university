from setuptools import find_packages, setup

setup(
    name="dagster_and_dbt",
    packages=find_packages(exclude=["dagster_and_dbt_tests"]),
    install_requires=[
        "dagster==1.10.*",
        "dagster-webserver",
        "dagster-cloud",
        "dagster-duckdb",
        "dagster-dbt",
        "dbt-duckdb",
        "geopandas",
        "pandas[parquet]",
        "shapely",
        "matplotlib",
        "smart_open[s3]",
        "s3fs",
        "smart_open",
        "boto3",
        "pyarrow",
        "dagster-components",
    ],
    extras_require={"dev": ["ruff", "pytest"]},
)
