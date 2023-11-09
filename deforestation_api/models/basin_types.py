from __future__ import annotations

from pydantic import BaseModel, Field

from deforestation_api.models.geometry_types import (
    PolygonGeometry,
    FeatureType,
    FeatureCollectionType,
)


class LossYear(BaseModel):
    year: int = Field(example=2022)
    area: float = Field(example=8.5095)
    relative_area: float = Field(example=0.0036)


class BasinProperties(BaseModel):
    downstream_id: int = Field(
        example=1071114980,
        description="Id of the next downstream polygon for the current basin polygon. The value 0 means that there is no downstream connection."
    )
    basin_area: float = Field(
        example=2350.0,
        description="Area of the basin polygon in square kilometers."
    )
    upstream_area: float = Field(
        example=29444.1,
        description="Total upstream area in square kilometers, including the current polygon."
    )
    start_year: int = Field(example=2020)
    end_year: int = Field(example=2022)
    daterange_tot_treeloss: float = Field(
        example=35.7217,
        description="Total tree cover loss, in square kilometers, within the basin polygon over the time period from start_year to end_year (inclusive)"
    )
    daterange_rel_treeloss: float = Field(
        example=0.0152,
        description="Tree cover loss within the basin polygon relative to the area of the polygon, over the time period from start_year to end_year (inclusive). Equivalent to daterange_tot_treeloss / basin_area."
    )
    treeloss_per_year: list[LossYear]


class DeforestationBasinFeature(BaseModel):
    id: int = Field(example=1071119930)
    type: FeatureType
    properties: BasinProperties
    geometry: PolygonGeometry


class DeforestationBasinGeoJSON(BaseModel):
    type: FeatureCollectionType
    features: list[DeforestationBasinFeature]
