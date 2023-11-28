from shapely import Point, box
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


def point_query(df: gpd.GeoDataFrame, lon: float, lat: float) -> gpd.GeoDataFrame:
    p = Point(lon, lat)
    query_index = df.sindex.query(p, predicate="within")
    return df.iloc[query_index]


def bbox_query(
    df: gpd.GeoDataFrame,
    lon_min: float,
    lat_min: float,
    lon_max: float,
    lat_max: float,
) -> gpd.GeoDataFrame:
    bbox = box(lon_min, lat_min, lon_max, lat_max)
    query_index = df.sindex.query(bbox, predicate="intersects")
    return df.iloc[query_index]


def filter_basin_df(
    df: gpd.GeoDataFrame,
    coordinates: tuple[float, float] | tuple[float, float, float, float],
) -> gpd.GeoDataFrame:
    if len(coordinates) == 2:
        return point_query(df, *coordinates)
    if len(coordinates) == 4:
        return bbox_query(df, *coordinates)


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
    summary="Get yearly forest cover loss within a river basin",
    description=(
        "Returns the estimated deforested area per year within a river basin "
        "for the given location."
    ),
    response_model=DeforestationBasinGeoJSON,
)
async def lossyear(
    coordinates: CoordinatesDep,
    date_range: DateRangeDep,
    basins: BasinDataDep,
    lossyear: LossyearDataDep,
) -> DeforestationBasinGeoJSON:
    start_year, end_year = date_range
    filtered_basins = filter_basin_df(basins, coordinates)
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
