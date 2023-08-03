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