from setuptools import find_packages, setup

setup(
    name="cereals",
    packages=find_packages(exclude=["cereals_tests"]),
    install_requires=[
        "dagster",
        "dagster-snowflake",
        "dagster-snowflake-pandas",
        "dagster-aws"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
