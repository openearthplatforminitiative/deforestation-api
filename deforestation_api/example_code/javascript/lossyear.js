// Get yearly forest cover loss for the river basin at the given point
const response_point = await fetch(
    "$endpoint_url?" + new URLSearchParams({
        lat: -1.9441,
        lon: 30.0619
    })
);
const data_point = await response_point.json();

// Print the total forest cover loss within the returned river basin
console.log(data_point.features[0].properties.daterange_tot_treeloss);


// Get yearly forest cover loss for all river basins within the given bounding box
const response_bbox = await fetch(
    "$endpoint_url?" + new URLSearchParams({
        min_lon: 28.850951,
        min_lat: -2.840114,
        max_lon: 30.909622,
        max_lat: -1.041395
    })
);
const data_bbox = await response_bbox.json();

// Print the total forest cover loss within the first returned river basin
console.log(data_bbox.features[0].properties.daterange_tot_treeloss);