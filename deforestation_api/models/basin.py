from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal

from deforestation_api.models.geometry import Polygon, MultiPolygon


class LossYear(BaseModel):
    year: int = Field(examples=[2022], description="Year when the loss was detected.")
    area: float = Field(
        examples=[8.5095],
        description="Total tree cover loss within the basin polygon, in square kilometers.",
    )
    relative_area: float = Field(
        examples=[0.0036],
        description=(
            "Tree cover loss within the basin polygon "
            "relative to the total area of the polygon."
        ),
    )


class BasinProperties(BaseModel):
    downstream_id: int = Field(
        examples=[1071114980],
        description=(
            "Id of the next downstream polygon for the current basin polygon. "
            "The value 0 means that there is no downstream connection."
        ),
    )
    basin_area: float = Field(
        examples=[2350.0], description="Area of the basin polygon in square kilometers."
    )
    upstream_area: float = Field(
        examples=[29444.1],
        description=(
            "Total upstream area in square kilometers, "
            "including the current polygon."
        ),
    )
    start_year: int = Field(examples=[2020])
    end_year: int = Field(examples=[2022])
    daterange_tot_treeloss: float = Field(
        examples=[35.7217],
        description=(
            "Total tree cover loss, in square kilometers, "
            "within the basin polygon over the time period "
            "from start_year to end_year (inclusive)"
        ),
    )
    daterange_rel_treeloss: float = Field(
        examples=[0.0152],
        description=(
            "Tree cover loss within the basin polygon "
            "relative to the total area of the polygon, "
            "over the time period from start_year to end_year (inclusive). "
            "Equivalent to `daterange_tot_treeloss / basin_area`."
        ),
    )
    treeloss_per_year: list[LossYear]


class DeforestationBasinFeature(BaseModel):
    id: int = Field(
        examples=[1071119930], description="Unique basin polygon identifier."
    )
    type: Literal["Feature"]
    properties: BasinProperties
    geometry: Polygon | MultiPolygon


class DeforestationBasinGeoJSON(BaseModel):
    type: Literal["FeatureCollection"]
    features: list[DeforestationBasinFeature]
