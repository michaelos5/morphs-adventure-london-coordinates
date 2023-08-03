import json

def create_gpx(json_data):
    gpx_template = '''<?xml version="1.0" encoding="UTF-8"?>
<gpx creator="Michael O'Sullivan" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" xmlns="http://www.topografix.com/GPX/1/1">
 <metadata>
  <name>Morphs Epic Adventure - Morphy Trail</name>
  <desc>Find all 56 Morphs</desc>
  <author>
   <name>Michael O Sullivan</name>
   <link href="https://www.strava.com/athletes/39559723"/>
  </author>
 </metadata>
 {waypoints}
</gpx>'''

    waypoint_template = '''
    <wpt lat="{latitude}" lon="{longitude}">
    <name>{name}</name>
    </wpt>
    '''

    waypoints = ""
    for index, marker in enumerate(json_data['markers']):
        waypoints += waypoint_template.format(
            id=index,
            name=marker['title'],
            address=marker['address'],
            latitude=marker['lat'],
            longitude=marker['lng']
        )

    gpx_content = gpx_template.format(waypoints=waypoints)
    return gpx_content

# Read JSON data from file
with open('websiteResponseMorphLocations.json', 'r') as json_file:
    json_data_imported = json.load(json_file)

gpx_content = create_gpx(json_data_imported)

# Save the GPX content to a file
with open('output.gpx', 'w') as gpx_file:
    gpx_file.write(gpx_content)

print("Conversion successful. GPX file created.")