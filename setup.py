from setuptools import find_packages, setup

setup(
    name="dagster_university",
    packages=find_packages(exclude=["dagster_university_tests"]),
    install_requires=[
        "dagster==1.3.9",
        "dagster-cloud",
        "pandas",
        "seaborn",
        "dagster-slack"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
