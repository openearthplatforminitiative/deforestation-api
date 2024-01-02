from typing import Annotated

from fastapi import Depends, Query, HTTPException

from deforestation_api.settings import settings


def point_in_roi(lon: float, lat: float, roi: dict[str, float]) -> bool:
    return (
        roi["min_lon"] <= lon <= roi["max_lon"]
        and roi["min_lat"] <= lat <= roi["max_lat"]
    )


def bbox_in_roi(
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
    roi: dict[str, float],
) -> bool:
    """Check if a bounding box intersects the ROI. Return True if any part of the bounding box is within the ROI."""
    return (
        point_in_roi(min_lon, min_lat, roi)
        or point_in_roi(max_lon, min_lat, roi)
        or point_in_roi(max_lon, max_lat, roi)
        or point_in_roi(min_lon, max_lat, roi)
    )


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
            description="Minimum longitude of the bounding box to retrieve data for."
        ),
    ] = None,
    min_lat: Annotated[
        float | None,
        Query(description="Minimum latitude of the bounding box to retrieve data for."),
    ] = None,
    max_lon: Annotated[
        float | None,
        Query(
            description="Maximum longitude of the bounding box to retrieve data for."
        ),
    ] = None,
    max_lat: Annotated[
        float | None,
        Query(description="Maximum latitude of the bounding box to retrieve data for."),
    ] = None,
) -> tuple[float, float] | tuple[float, float, float, float]:
    point = (lon, lat)
    bbox = (min_lon, min_lat, max_lon, max_lat)
    if None not in point and None not in bbox:
        raise HTTPException(
            status_code=400,
            detail=(
                "Ambiguous coordinates. Request contains both point coordinates (lon,"
                " lat) and bounding box coordinates (min_lon, min_lat, max_lon,"
                " max_lat). Request should only include either point coordinates or"
                " bounding box coordinates, not both."
            ),
        )
    if None not in point:
        if not point_in_roi(*point, settings.gfc_roi):
            raise HTTPException(
                status_code=404, detail="No data exists for the queried point."
            )
        return point
    if None not in bbox:
        if not bbox_in_roi(*bbox, settings.gfc_roi):
            raise HTTPException(
                status_code=404, detail="No data exists for the queried bounding box."
            )
        return bbox
    raise HTTPException(
        status_code=400,
        detail=(
            "Missing coordinates in request. Request must either include point"
            " coordinates (lon, lat) or bounding box coordinates (min_lon, min_lat,"
            " max_lon, max_lat)."
        ),
    )


CoordinatesDep = Annotated[
    tuple[float, float] | tuple[float, float, float, float], Depends(coordinates)
]


def date_range(
    start_year: Annotated[
        int,
        Query(description="First year in the date range to return data for."),
    ] = 2001,
    end_year: Annotated[
        int,
        Query(description="Last year in the data range to return data for."),
    ] = 2022,
) -> tuple[int, int]:
    if start_year > end_year:
        raise HTTPException(
            status_code=400,
            detail="Ivalid date range. start_year can not be greater than end_year.",
        )
    return start_year, end_year


DateRangeDep = Annotated[tuple[int, int], Depends(date_range)]
