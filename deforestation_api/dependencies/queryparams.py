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
    startyear: Annotated[
        int | None,
        Query(
            description="Inclusive lower bound for the range of years to return data for. Defaults to 2020."
        ),
    ] = 2020,
    endyear: Annotated[
        int | None,
        Query(
            description="Inclusive lower bound for the range of years to return data for. Defaults to 2020."
        ),
    ] = 2022,
) -> (int, int):
    return startyear, endyear


DateRangeDep = Annotated[tuple[int, int], Depends(date_range)]
