from __future__ import annotations

from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field


class FeatureCollectionType(Enum):
    FeatureCollection = "FeatureCollection"


class FeatureType(Enum):
    Feature = "Feature"


class GeometryType(Enum):
    Polygon = "Polygon"


PolygonCoordinateType = Annotated[list[float], Field(min_length=2, max_length=2, example=[20.4291, 0.7083])]


class PolygonGeometry(BaseModel):
    type: GeometryType
    coordinates: list[list[PolygonCoordinateType]]