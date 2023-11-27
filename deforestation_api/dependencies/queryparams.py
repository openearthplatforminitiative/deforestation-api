from typing import Annotated

from fastapi import Depends, Query, HTTPException


def coordinates(
    lon: Annotated[
        float | None,
        Query(description="Longitude of the point to retrieve data for"),
    ] = None,
    lat: Annotated[
        float | None,
        Query(description="Latitude of the point to retrieve data for"),
    ] = None,
    lon_min: Annotated[
        float | None,
        Query(description="Minimal longitude for the query bounding box."),
    ] = None,
    lat_min: Annotated[
        float | None,
        Query(description="Minimal latitude for the query bounding box."),
    ] = None,
    lon_max: Annotated[
        float | None,
        Query(description="Maximal longitude for the query bounding box."),
    ] = None,
    lat_max: Annotated[
        float | None,
        Query(description="Maximal latitude for the query bounding box."),
    ] = None,
) -> tuple[float, float] | tuple[float, float, float, float]:
    if lon is not None and lat is not None:
        return lon, lat
    bbox = (lon_min, lat_min, lon_max, lat_max)
    if all(v is not None for v in bbox):
        return bbox
    raise HTTPException(
        status_code=400,
        detail="Missing coordinates in request. Request should either include both lat and lon, or all of lon_min, lat_min, lon_max, lat_max.",
    )


CoordinatesDep = Annotated[
    tuple[float, float] | tuple[float, float, float, float], Depends(coordinates)
]


def date_range(
    start_year: Annotated[
        int,
        Query(description="First year to return forest cover loss data for."),
    ] = 2001,
    end_year: Annotated[
        int,
        Query(description="Last year to return forest cover loss data for."),
    ] = 2022,
) -> (int, int):
    return start_year, end_year


DateRangeDep = Annotated[tuple[int, int], Depends(date_range)]
