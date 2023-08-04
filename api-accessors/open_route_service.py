import requests
import openrouteservice
from openrouteservice import convert
API_TOKEN = ''

test_coords=[(8.34234,48.23424),(8.34423,48.26424)]

def sendOptimizationRequest(approximateRoute):
    coords = []
    for point in approximateRoute:
        coords.append((point['geometry']['coordinates'][0],point['geometry']['coordinates'][1]))
    client = openrouteservice.Client(key=API_TOKEN)
    routes = client.directions(coordinates=coords, profile='foot-walking')['routes'][0]['geometry']
    return convert.decode_polyline(routes)