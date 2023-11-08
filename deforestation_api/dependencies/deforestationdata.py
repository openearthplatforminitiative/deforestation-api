from typing import Annotated

import geopandas as gpd
import pandas as pd
from fastapi import Depends
from deforestation_api.settings import settings


def load_geoparquet(path) -> gpd.GeoDataFrame:
    df = gpd.read_parquet(
        path,
        storage_options={"anon": True},
    )
    df = df.set_index("id")
    df.sindex  # Initializing the spatial index speeds up spatial queries
    return df


def load_parquet(path) -> pd.DataFrame:
    df = pd.read_parquet(
        path,
        storage_options={"anon": True},
    )
    return df


def get_lossyear_data() -> gpd.GeoDataFrame:
    df = pd.read_parquet(
        settings.lossyear_data_path,
        storage_options={"anon": True},
    )
    return df


def get_basin_data() -> gpd.GeoDataFrame:
    df = gpd.read_parquet(
        settings.basin_data_path,
        storage_options={"anon": True},
    )
    df = df.set_index("id")
    df.sindex  # Initializing the spatial index speeds up spatial queries
    return df


BasinDataDep = Annotated[gpd.GeoDataFrame, Depends(get_basin_data)]
LossyearDataDep = Annotated[gpd.GeoDataFrame, Depends(get_lossyear_data)]
