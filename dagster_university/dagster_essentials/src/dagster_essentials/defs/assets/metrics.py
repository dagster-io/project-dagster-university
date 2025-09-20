import dagster as dg

import matplotlib.pyplot as plt
import geopandas as gpd

import duckdb
import os

from dagster_essentials.defs.assets import constants

@dg.asset
def metrics(context: dg.AssetExecutionContext) -> dg.MaterializeResult: ...
