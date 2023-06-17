from setuptools import find_packages, setup

setup(
    name="dagster_university",
    packages=find_packages(exclude=["dagster_university_tests"]),
    install_requires=[
        "dagster==1.3.9",
        "dagster-cloud",
        "dagster-gcp",
        "dagster-slack",
        "geopandas",
        "kaleido",
        "pandas",
        "plotly",
        "shapely"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
