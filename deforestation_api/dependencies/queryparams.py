from typing import Annotated

from fastapi import Depends, Query, HTTPException


def coordinates(
    lon: Annotated[
        float | None,
        Query(description="Longitude of the point to retrieve data for."),
    ] = None,
    lat: Annotated[
        float | None,
        Query(description="Latitude of the point to retrieve data for."),
    ] = None,
    min_lon: Annotated[
        float | None,
        Query(
            description="Minimal longitude of the bounding box to retrieve data for."
        ),
    ] = None,
    min_lat: Annotated[
        float | None,
        Query(description="Minimal latitude of the bounding box to retrieve data for."),
    ] = None,
    max_lon: Annotated[
        float | None,
        Query(
            description="Maximal longitude of the bounding box to retrieve data for."
        ),
    ] = None,
    max_lat: Annotated[
        float | None,
        Query(description="Maximal latitude of the bounding box to retrieve data for."),
    ] = None,
) -> tuple[float, float] | tuple[float, float, float, float]:
    if lon is not None and lat is not None:
        return lon, lat
    bbox = (min_lon, min_lat, max_lon, max_lat)
    if all(v is not None for v in bbox):
        return bbox
    raise HTTPException(
        status_code=400,
        detail="Missing coordinates in request. Request must either include both lat and lon, or all of min_lon, min_lat, max_lon, max_lat.",
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
) -> tuple[int, int]:
    return start_year, end_year


DateRangeDep = Annotated[tuple[int, int], Depends(date_range)]
