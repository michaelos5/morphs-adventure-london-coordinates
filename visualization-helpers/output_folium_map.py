import folium
import os
import webbrowser
import polyline
from math import radians, sin, cos, sqrt, atan2

current_dir = os.path.dirname(os.path.abspath(__file__))
export_path = os.path.join(current_dir, "exports", "gps_data_map.html")

def createPopup(idx,point):
    title = point['properties']['title']
    address = point['properties']['address']
    template = '''
    <h3>Stop {idx}</h3><br>
    <b>Morph Name:</b>{title}<br>
    <b>Address:</b>{address}<br>
    '''
    return template.format(idx=idx,title=title,address=address)

def centerMapByPoints(gps_points):
    return [51.5225776,-0.1214206]

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    earth_radius = 6371  # Earth's radius in kilometers
    distance = earth_radius * c

    return distance

def routeLength(route):
    total_length = 0
    for i in range(len(route) - 1):
        lat1, lon1 = route[i]
        lat2, lon2 = route[i + 1]
        segment_length = haversine_distance(lat1, lon1, lat2, lon2)
        total_length += segment_length

    return total_length
def generateMap(ordered_features,nn_route,geometry):
    # Create a map centered at a specific location
    map_center = centerMapByPoints(gps_points=ordered_features)  # Replace latitude and longitude with your GPS data
    map_zoom = 13  # Adjust the zoom level as needed
    map_osm = folium.Map(location=map_center, zoom_start=map_zoom)
    #gps_points = [x for _, x in sorted(zip(nn_route, gps_points))]
    line_coords = []
    for idx, point in enumerate(ordered_features):
        lat, lng = point['geometry']['coordinates'][1], point['geometry']['coordinates'][0]
        line_coords.append([lat, lng])
        popup = createPopup(idx+1,point)
        folium.Marker(location=[lat, lng],popup=popup).add_to(map_osm)
    folium.PolyLine(locations=nn_route, color='red', tooltip="Approximate Route").add_to(map_osm)
    for direction_split in geometry:
        folium.GeoJson(direction_split).add_to(map_osm)
    print("Total length of the Route:", routeLength(nn_route), "kilometers")
    map_osm.save(export_path)
    webbrowser.open(export_path)
    return None
    