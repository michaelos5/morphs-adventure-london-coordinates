import folium
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
export_path = os.path.join(current_dir, "exports", "gps_data_map.html")
def centerMapByPoints(gps_points):
    return [51.5225776,-0.1214206]

def generateMap(gps_points,nn_route):
    # Create a map centered at a specific location
    map_center = centerMapByPoints(gps_points=gps_points)  # Replace latitude and longitude with your GPS data
    map_zoom = 13  # Adjust the zoom level as needed
    map_osm = folium.Map(location=map_center, zoom_start=map_zoom)
    #gps_points = [x for _, x in sorted(zip(nn_route, gps_points))]
    line_coords = []
    for idx, point in enumerate(gps_points):
        lat, lng = point[0], point[1]
        line_coords.append([lat, lng])
        folium.Marker(location=[lat, lng],popup=str(idx)).add_to(map_osm)
    folium.PolyLine(locations=line_coords, color='blue').add_to(map_osm)
    map_osm.save(export_path)
    