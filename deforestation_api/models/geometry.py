from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal
from pydantic import BaseModel, Field

Longitude = Annotated[float, Field(ge=-180, le=180)]
Latitude = Annotated[float, Field(ge=-90, le=90)]
Position = tuple[Longitude, Latitude]
LinearRing = Annotated[list[Position], Field(min_length=4)]
PolygonCoords = list[LinearRing]


class Polygon(BaseModel):
    type: Literal["Polygon"]
    coordinates: PolygonCoords
