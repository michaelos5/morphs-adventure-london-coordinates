from geopy.distance import geodesic
from itertools import permutations
import math

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


def distance(point1, point2):
    lat1, lng1 = point1
    lat2, lng2 = point2
    return math.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2)

def nearest_neighbor_tsp(points, start_point):
    tour = [start_point]
    remaining_points = set(points)
    remaining_points.remove(start_point)

    while remaining_points:
        nearest_point = min(remaining_points, key=lambda x: distance(tour[-1], x))
        tour.append(nearest_point)
        remaining_points.remove(nearest_point)

    #tour.append(start_point) # enable for return to starting point

    return tour

def approximatePathOrdering(datasetFeatures):
    # Using Nearest Neighbor algorithm to get an approximate optimal route
    gps_points = []
    for feature in datasetFeatures:
        gps_points.append((feature['geometry']['coordinates'][1], feature['geometry']['coordinates'][0]))
        
    #nn_route = nearest_neighbor_algorithm(gps_points)
    starting_point = (51.50448,-0.07662)

    # Find the optimal tour starting from the chosen data point
    ordered_gps_points = nearest_neighbor_tsp(points=gps_points, start_point=starting_point)
    print("Nearest Neighbor route calculated")
    return ordered_gps_points