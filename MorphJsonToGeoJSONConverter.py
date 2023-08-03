import json
import sys, os
import requests
import geo_json_creator
import approximate_route
import mapbox_apis
current_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(current_dir, "test-data", "mapbox-api-responses")
sys.path.append(module_path)
import dataset_features_response
    

    


def splitPerAPIRestrictions(dataset_features, API_CEILING_LIMIT_PER_REQUEST):
    group_size = API_CEILING_LIMIT_PER_REQUEST
    split_data = [dataset_features[i:i + group_size] for i in range(0, len(dataset_features), group_size)]

    # Modify lat/lng for each group (except the first one)
    for i in range(1, len(split_data)):
        prev_group = split_data[i - 1]
        current_group = split_data[i]

        # Set the lat/lng of the first object in the current group
        # to match the lat/lng of the last object in the previous group
        
        # Represents feature.geometry.coordinates[0] = lat e.g. -0.100134
        # Represents feature.geometry.coordinates[1] = lng e.g. 51.508584
        current_group[0]['geometry']['coordinates'][0] = prev_group[-1]['geometry']['coordinates'][0]
        current_group[0]['geometry']['coordinates'][1] = prev_group[-1]['geometry']['coordinates'][1]

    return split_data

def launchOptimizationJob(orderedDatasetFeatures):
    # print(dataset_features)
    GPS_POINT_LIMIT_PER_REQUEST = 12
    requestBundle = []
    for requestBundle in splitPerAPIRestrictions(orderedDatasetFeatures, GPS_POINT_LIMIT_PER_REQUEST):
        requestBundle += mapbox_apis.sendOptimizationRequest('walking',orderedDatasetFeatures)
    return requestBundle


# Read JSON data from file
with open('source-data/regular-morph-location-web-response.json', 'r') as json_file:
    json_morph_data= json.load(json_file)

with open('source-data/mini-morph-locations-manual.json', 'r') as json_file:
    json_mini_morph_data= json.load(json_file)

geojson_content = geo_json_creator.create_geojson(json_mini_morph_data,json_morph_data)
"""
## TODO ##
Use Travelling sales man algorithm to find the shortest path between all points
order the points according to the order of the above TSP algorithm
Divide the gps points to the max mapbox query limit for running directions
Split the points and run the directions query to Mapbox ensuring the start/end points of each subset split can bee chained together
Tie the directions together containing the shortest path following the road network and present it in GPX format
Export the GPX file to be imported into Strava Route Creator or other GPS tracking software
"""
# Save the GPX content to a file
with open('exported-data/morph-art-trail-geo.json', 'w') as gpx_file:
    gpx_file.write(geojson_content)

print("Conversion successful. GeoJSON file created.")

print("Retrieve Mapbox Dataset Features")
#datasetFeatures = mapbox_apis.getDatasetFeatures()
datasetFeatures = dataset_features_response.fetchDatasetFeatures()
print('Retrieved {0} features from Mapbox Dataset'.format(len(datasetFeatures)))
print(datasetFeatures)
orderedFeatures = approximate_route.approximatePathOrdering(datasetFeatures)
#launchOptimizationJob(orderedFeatures)
