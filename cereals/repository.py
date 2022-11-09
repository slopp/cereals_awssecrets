from dagster import asset, repository, with_resources, define_asset_job, AssetSelection
from dagster_snowflake import build_snowflake_io_manager
from dagster_snowflake_pandas import SnowflakePandasTypeHandler
import pandas as pd
import csv
import requests

#  This function will load environment variables from 
#  AWS secrets if they are not already set
from .utils.load_aws_secrets import load_aws_secret
# load a secret stored as a key-value string by name
# if the secret is KEY=VALUE 
# the result is an environment variable KEY set to VALUE
load_aws_secret("aws-snowflake-password")

# load a secret that is a simple string
# if the secret is VALUE 
# the result is an environment variable SNOWFLAKE_USER set to VALUE
load_aws_secret("SNOWFLAKE_USER")


# initialize resources using the now set environment variables
snowflake_io_manager = build_snowflake_io_manager([SnowflakePandasTypeHandler()])


resources = {
    "io_manager": snowflake_io_manager.configured({
        "database": "DEMO_DB2_BRANCH", 
        "account": {"env": "SNOWFLAKE_ACCOUNT"},
        "user": {"env": "SNOWFLAKE_USER"},
        "password": {"env": "SNOWFLAKE_PASSWORD"},
        "warehouse": "TINY_WAREHOUSE"
    })
}

# define assets, a key prefix is used to specify the snowflake schema

@asset(key_prefix="CEREAL")
def cereals():
    response = requests.get("https://docs.dagster.io/assets/cereal.csv")
    lines = response.text.split("\n")
    return pd.DataFrame([row for row in csv.DictReader(lines)])


@asset(key_prefix="CEREAL")
def nabisco_cereals(cereals: pd.DataFrame):
    """Cereals manufactured by Nabisco"""
    return cereals[(cereals["mfr"] == "N")]


# bind assets to resources

cereal_assets_with_resources = with_resources(
    definitions = [cereals, nabisco_cereals], 
    resource_defs=resources
)

# optional create a job that targets assets
cereal_updater = define_asset_job("cereal_updater", selection = AssetSelection.keys(["CEREAL", "cereals"]).downstream())

@repository
def cereals():
    return [cereal_assets_with_resources, cereal_updater]
