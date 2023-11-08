from shapely import Point
import geopandas as gpd
import pandas as pd
import json

from fastapi import APIRouter

from deforestation_api.dependencies.deforestationdata import (
    BasinDataDep,
    LossyearDataDep,
)
from deforestation_api.dependencies.queryparams import CoordinatesDep, DateRangeDep

router = APIRouter(prefix="/deforestation", tags=["deforestation"])


def spatial_filter(
    df: gpd.GeoDataFrame, lat: float, lon: float, predicate: str = "within"
) -> gpd.GeoDataFrame:
    p = Point(lon, lat)
    query_index = df.sindex.query(p, predicate=predicate)
    return df.iloc[query_index]


def add_treecover_loss_data(
    feature, treecover_loss: pd.DataFrame, startyear: int, endyear: int
) -> None:
    basin_loss = treecover_loss[treecover_loss["id"] == feature["id"]]
    basin_loss = basin_loss.loc[basin_loss["year"].between(startyear, endyear)]
    total_loss = basin_loss["area"].sum()
    relative_loss = basin_loss["relative_area"].sum()
    loss_per_year = basin_loss.drop(columns="id").to_json(orient="records")
    loss_per_year = json.loads(loss_per_year)
    feature["properties"]["daterange_tot_treeloss"] = total_loss
    feature["properties"]["daterange_rel_treeloss"] = relative_loss
    feature["properties"]["treeloss_per_year"] = loss_per_year


@router.get("/basin")
async def lossyear(
    coordinates: CoordinatesDep,
    date_range: DateRangeDep,
    basins: BasinDataDep,
    lossyear: LossyearDataDep,
):
    lat, lon = coordinates
    startyear, endyear = date_range
    filtered_basins = spatial_filter(basins, lat, lon)
    filtered_basins["startyear"] = startyear
    filtered_basins["endyear"] = endyear
    res = filtered_basins[
        [
            "downstream_id",
            "basin_area",
            "upstream_area",
            "startyear",
            "endyear",
            "geometry",
        ]
    ].to_json()
    res = json.loads(res)
    # Iterating though features and adding the treecover loss data for each basin polygon.
    # Currently with a single point query there should only be one feature.
    # If a bounding-box query feature is added there may be multiple polygons in the response.
    for basin_polygon in res["features"]:
        # The id field is annoyingly converted to str in the to_json method in geopandas
        basin_polygon["id"] = int(basin_polygon["id"])
        add_treecover_loss_data(basin_polygon, lossyear, startyear, endyear)
    return res
