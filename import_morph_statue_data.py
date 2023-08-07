import json

# This script is responsible for taking in reading source-data and generating a geojson file
# This geojson file is then used by the visualization script to generate a map
# The import data consists of two files (both in source-data):
# 1. mini-morph-locations-manual.json
# 2. regular-morph-location-web-response.json
# 
# The first file is a manual list of mini morph locations
# The second file is a list of regular morph locations

def create_geojson(json_mini_morph_data, json_morph_data):
    geojson_template = '''{{
    "type": "FeatureCollection",
    "features": [
        {point_data}
    ]}}'''
    point_template = '''
    {{
        "type": "Feature",
        "properties": {{
            "title": "{name}",
            "address": "{address}",
            "index": {id},
            "morphType": "{morphType}"
        }},
        "geometry": {{
            "coordinates": [
            {longitude},
             {latitude}
        ],
        "type": "Point"
        }}
    }},'''

    point_data = ""
    for index, marker in enumerate(json_mini_morph_data['markers']):
        point_data += point_template.format(
            id=index,
            name=marker['title'],
            address=marker['address'],
            latitude=marker['lat'],
            longitude=marker['lng'],
            morphType='Mini'
        )

    for index, marker in enumerate(json_morph_data['markers']):
        point_data += point_template.format(
            id=index,
            name=marker['title'],
            address=marker['address'],
            latitude=marker['lat'],
            longitude=marker['lng'],
            morphType='Regular'
        )
    point_data = point_data[:-1]
    geojson_content = geojson_template.format(point_data=point_data)

    
    return geojson_content

# Read JSON data from file
with open('source-data/regular-morph-location-web-response.json', 'r') as json_file:
    json_morph_data= json.load(json_file)

with open('source-data/mini-morph-locations-manual.json', 'r') as json_file:
    json_mini_morph_data= json.load(json_file)

geojson_content = create_geojson(json_mini_morph_data,json_morph_data)
# Save the GPX content to a file
with open('exported-data/morph-art-trail-geo.json', 'w') as gpx_file:
    gpx_file.write(geojson_content)

print("Conversion successful. GeoJSON file created.")