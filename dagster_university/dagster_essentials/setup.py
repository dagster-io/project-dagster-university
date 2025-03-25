from setuptools import find_packages, setup

setup(
    name="dagster_essentials",
    packages=find_packages(exclude=["dagster_essentials_tests"]),
    install_requires=[
        "dagster==1.10.*",
        "dagster-webserver",
        "dagster-cloud",
        "dagster-duckdb",
        "geopandas",
        "pandas[parquet]",
        "shapely",
        "matplotlib",
    ],
    extras_require={"dev": ["ruff", "pytest"]},
)