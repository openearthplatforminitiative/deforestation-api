from httpx import Client

with Client() as client:
    # Get yearly forest cover loss for the river basin at the given point
    response_point = client.get(
        url="$endpoint_url",
        params={"lon": 30.0619, "lat": -1.9441},
    )

    data_point = response_point.json()

    # Print the total forest cover loss within the returned river basin
    print(data_point["features"][0]["properties"]["daterange_tot_treeloss"])

    # Get yearly forest cover loss for all river basins within the given bounding box
    response_bbox = client.get(
        url="$endpoint_url",
        params={
            "min_lon": 28.850951,
            "min_lat": -2.840114,
            "max_lon": 30.909622,
            "max_lat": -1.041395,
        },
    )

    data_bbox = response_bbox.json()

    # Print the total forest cover loss within the first returned river basin
    print(data_bbox["features"][0]["properties"]["daterange_tot_treeloss"])
