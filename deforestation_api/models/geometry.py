from __future__ import annotations

from typing import Annotated, Literal
from pydantic import BaseModel, Field

Longitude = Annotated[float, Field(ge=-180, le=180)]
Latitude = Annotated[float, Field(ge=-90, le=90)]
Position = tuple[Longitude, Latitude]
LinearRing = Annotated[
    list[Position],
    Field(
        examples=[
            [[-20.0, -10.0], [50.0, -10.0], [50.0, 10.0], [-20.0, 10.0], [-20.0, -10.0]]
        ],
        min_length=4,
    ),
]
PolygonCoords = list[LinearRing]
MultiPolygonCoords = list[PolygonCoords]


class Polygon(BaseModel):
    type: Literal["Polygon"]
    coordinates: PolygonCoords


class MultiPolygon(BaseModel):
    type: Literal["MultiPolygon"]
    coordinates: MultiPolygonCoords
