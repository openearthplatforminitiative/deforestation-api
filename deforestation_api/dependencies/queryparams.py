from typing import Annotated

from fastapi import Depends, Query


def coordinates(
    lon: Annotated[
        float,
        Query(description="Longitude of the coordinate to retrieve data for"),
    ],
    lat: Annotated[
        float,
        Query(description="Latitude of the coordinate to retrieve data for"),
    ],
) -> (float, float):
    return lon, lat


CoordinatesDep = Annotated[tuple[float, float], Depends(coordinates)]


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
