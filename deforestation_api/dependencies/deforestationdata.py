import logging
from datetime import timezone
from typing import Annotated

import asyncio
import geopandas as gpd
import pandas as pd
from aiocron import crontab
from fastapi import FastAPI, Request, Depends

from deforestation_api.settings import settings

logger = logging.getLogger(__name__)


def fetch_geoparquet(path: str) -> gpd.GeoDataFrame:
    logger.info(f"Reloading data from {path}")

    gdf = gpd.read_parquet(
        path,
        storage_options={"anon": True},
    )
    gdf = gdf.set_index("id")
    gdf.sindex  # Initializing the spatial index speeds up spatial queries
    logger.info(f"Done reloading data from {path}")
    return gdf

def fetch_parquet(path) -> pd.DataFrame:
    logger.info(f"Reloading data from {path}")

    df = pd.read_parquet(
        path,
        storage_options={"anon": True},
    )
    logger.info(f"Done reloading data from {path}")
    return df


def get_lossyear_data(request: Request) -> pd.DataFrame | None:
    return request.app.lossyear_data


def get_basin_data(request: Request) -> gpd.GeoDataFrame | None:
    return request.app.basin_data


LossyearDataDep = Annotated[pd.DataFrame, Depends(get_lossyear_data)]
BasinDataDep = Annotated[gpd.GeoDataFrame, Depends(get_basin_data)]


async def deforestation_data_fetcher(app: FastAPI):
    logger.info("Deforestation data fetcher running")
    schedule = crontab("0 0 1 * * *", tz=timezone.utc)
    while True:
        await schedule.next()
        await fetch_deforestation_data(app)


async def fetch_deforestation_data(app: FastAPI):
    loop = asyncio.get_event_loop()
    (
        app.lossyear_data,
        app.basin_data,
    ) = await asyncio.gather(
        # loop.run_in_executor to prevents blocking the main thread
        loop.run_in_executor(None, fetch_parquet, settings.lossyear_data_path),
        loop.run_in_executor(None, fetch_geoparquet, settings.basin_data_path),
    )