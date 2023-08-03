from geopy.distance import geodesic
from itertools import permutations
import sys,os

current_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(current_dir, "visualization-helpers")
sys.path.append(module_path)
import output_folium_map

def calculate_distance(coords1, coords2):
    return geodesic(coords1, coords2).kilometers

def calculate_total_distance(route, points):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += calculate_distance(points[route[i]], points[route[i+1]])
    return total_distance

def nearest_neighbor_algorithm(points):
    n = len(points)
    unvisited = list(range(n))
    route = [0]  # Start at the first point (index 0)
    unvisited.remove(0)

    while unvisited:
        nearest_point = min(unvisited, key=lambda x: calculate_distance(points[route[-1]], points[x]))
        route.append(nearest_point)
        unvisited.remove(nearest_point)

    route.append(0)  # Return to the starting point to complete the cycle
    return route

def find_optimal_route(points):
    n = len(points)
    optimal_route = None
    min_distance = float('inf')

    for perm in permutations(range(1, n)):
        route = [0] + list(perm) + [0]
        total_distance = calculate_total_distance(route, points)
        if total_distance < min_distance:
            min_distance = total_distance
            optimal_route = route

    return optimal_route, min_distance

def approximatePathOrdering(datasetFeatures):
    # Using Nearest Neighbor algorithm to get an approximate optimal route
    gps_points = []
    for feature in datasetFeatures:
        gps_points.append((feature['geometry']['coordinates'][1], feature['geometry']['coordinates'][0]))
    nn_route = nearest_neighbor_algorithm(gps_points)
    print("Nearest Neighbor route:", nn_route)
    output_folium_map.generateMap(gps_points,nn_route)

    # Finding the truly optimal route by brute-force (works well for small number of points)
    """
    optimal_route, min_distance = find_optimal_route(gps_points)
    print("Optimal route:", optimal_route)
    print("Total distance (optimal):", min_distance, "km")
    """
    return datasetFeatures