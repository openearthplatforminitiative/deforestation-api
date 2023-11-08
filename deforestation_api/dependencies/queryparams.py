from typing import Annotated

from fastapi import Depends


def coordinates(lat: float, lon: float) -> (float, float):
    return lat, lon


CoordinatesDep = Annotated[tuple[float, float], Depends(coordinates)]


def date_range(
    startyear: int | None = None,
    endyear: int | None = None,
) -> (int, int):
    if startyear is None:
        startyear = 2020
    if endyear is None:
        endyear = 2022
    return startyear, endyear


DateRangeDep = Annotated[tuple[int, int], Depends(date_range)]
