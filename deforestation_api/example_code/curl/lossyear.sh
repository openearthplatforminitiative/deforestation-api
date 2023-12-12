# Get yearly forest cover loss for the river basin at the given point
curl -i -X GET $endpoint_url?lon=30.0619&lat=-1.9441

# Get yearly forest cover loss for all river basins within the given bounding box
curl -i -X GET $endpoint_url?min_lon=28.850951&min_lat=30.909622&max_lon=-2.840114&max_lat=-1.041395

