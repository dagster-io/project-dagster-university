from setuptools import find_packages, setup

setup(
    name="dagster_testing",
    packages=find_packages(exclude=["dagster_testing_tests"]),
    install_requires=[
        "dagster==1.10.*",
        "dagster-webserver",
        "dagster-snowflake",
        "psycopg2-binary",
        "pytest",
    ],
    extras_require={"dev": ["ruff"]},
)
