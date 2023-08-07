import json
import sys, os
import approximate_route

current_dir = os.path.dirname(os.path.abspath(__file__))
api_access_path = module_path = os.path.join(current_dir, "api-accessors")
sys.path.append(api_access_path)
import mapbox_apis
import gmaps_api
import open_route_service
module_path = os.path.join(current_dir, "test-data", "mapbox-api-responses")
sys.path.append(module_path)
import dataset_features_response

current_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(current_dir, "visualization-helpers")
sys.path.append(module_path)
import output_folium_map
    
#Set to false if you want to use the live Mapbox and OpenRouteService API services
TEST_DATA_SOURCE=True

    


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

def sortByIndex(feature):
    return feature['properties']['index']


# Set the GPS_POINT_LIMIT_PER_REQUEST to the maximum number of GPS points that can be sent to the API in a single request
def launchOptimizationJob(orderedDatasetFeatures):
    GPS_POINT_LIMIT_PER_REQUEST = 11
    API_PROVIDER_OPTIONS = ['open_route_service', 'mapbox', 'gmaps']
    DEFAULT_PROVIDER='open_route_service'
    requestBundle = []
    for request in splitPerAPIRestrictions(orderedDatasetFeatures, GPS_POINT_LIMIT_PER_REQUEST):
        if(DEFAULT_PROVIDER == 'open_route_service'):
            requestBundle.append(open_route_service.sendOptimizationRequest(request))
        elif(DEFAULT_PROVIDER == 'mapbox'):
            requestBundle.append(mapbox_apis.sendOptimizationRequest('walking',request))
        else:
            requestBundle.append(gmaps_api.sendOptimizationRequest(request))
    
    return requestBundle

# Retrieving Mapbox Dataset Features from test data source or live API hosted on personal maopbox account datasets
print("Retrieving Mapbox Dataset Features")
datasetFeatures = dataset_features_response.fetchDatasetFeatures() if TEST_DATA_SOURCE else mapbox_apis.getDatasetFeatures()
print('Retrieved {0} features from Mapbox Dataset'.format(len(datasetFeatures)))

# sort by index to get some semblance of real world placement order
print("Index sorting morph locations..")
datasetFeatures.sort(key=lambda x: x['properties']['index'], reverse=True)

# approximae route using Travelling Salesman Problem algorithm in preparation for relevant directions APIs
print("Approximating route..")
approximate_ordered_gps_points = approximate_route.approximatePathOrdering(datasetFeatures)
ordered_features = []
for point in approximate_ordered_gps_points:
    for feature in datasetFeatures:
        if feature['geometry']['coordinates'][1] == point[0] and feature['geometry']['coordinates'][0] == point[1]:
            ordered_features.append(feature)

print("Calculating optimal running routes..")
routeBundles = launchOptimizationJob(ordered_features)
print("Routes generated and stored..")
output_folium_map.generateMap(ordered_features,approximate_ordered_gps_points,routeBundles)