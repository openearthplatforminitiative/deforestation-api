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
from deforestation_api.models.basin import (
    DeforestationBasinGeoJSON,
    DeforestationBasinFeature,
)


router = APIRouter(tags=["deforestation"])


def spatial_filter(
    df: gpd.GeoDataFrame, lon: float, lat: float, predicate: str = "within"
) -> gpd.GeoDataFrame:
    p = Point(lon, lat)
    query_index = df.sindex.query(p, predicate=predicate)
    return df.iloc[query_index]


def add_treecover_loss_data(
    feature: DeforestationBasinFeature,
    treecover_loss: pd.DataFrame,
    start_year: int,
    end_year: int,
) -> None:
    basin_loss = treecover_loss[treecover_loss["id"] == feature["id"]]
    basin_loss = basin_loss.loc[basin_loss["year"].between(start_year, end_year)]
    total_loss = basin_loss["area"].sum()
    relative_loss = basin_loss["relative_area"].sum()
    loss_per_year = basin_loss.drop(columns="id").to_json(orient="records")
    loss_per_year = json.loads(loss_per_year)
    feature["properties"]["daterange_tot_treeloss"] = total_loss
    feature["properties"]["daterange_rel_treeloss"] = relative_loss
    feature["properties"]["treeloss_per_year"] = loss_per_year


@router.get(
    "/basin",
    summary="Get forest cover loss in river basin",
    description=(
        "Returns the total deforested area within the river basin "
        "containing the given location over a time period."
    ),
    response_model=DeforestationBasinGeoJSON,
)
async def lossyear(
    coordinates: CoordinatesDep,
    date_range: DateRangeDep,
    basins: BasinDataDep,
    lossyear: LossyearDataDep,
) -> DeforestationBasinGeoJSON:
    lon, lat = coordinates
    start_year, end_year = date_range
    filtered_basins = spatial_filter(basins, lon, lat)
    res = filtered_basins[
        [
            "downstream_id",
            "basin_area",
            "upstream_area",
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
        basin_polygon["properties"]["start_year"] = start_year
        basin_polygon["properties"]["end_year"] = end_year
        add_treecover_loss_data(basin_polygon, lossyear, start_year, end_year)
    return res
