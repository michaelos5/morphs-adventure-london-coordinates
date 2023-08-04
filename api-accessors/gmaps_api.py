import requests

URL_START = "https://routes.googleapis.com/"
API_KEY = ''


def sendOptimizationRequest(approximateRoute):
    api_url = '{url}directions/v2:computeRoutes?key={key}'.format(url=URL_START,key=API_KEY)

    JSON_REQUEST = '''
    {{
    "origin":
        {0}
    }},
    "destination":
        {1}
    }},
    "intermediates": {2},
    "travelMode": "WALK",
    "polylineQuality": "HIGH_QUALITY",
    "polylineEncoding": "ENCODED_POLYLINE",
    "units": "METRIC",
    "computeAlternativeRoutes": false,
    "routeModifiers": {{
        "avoidTolls": false,
        "avoidHighways": false,
        "avoidFerries": false
    }},
    "languageCode": "en-US"
    }}
    '''

    route_list = []
    for route in approximateRoute:
        lat = route['geometry']['coordinates'][0]
        lng = route['geometry']['coordinates'][1]
        route_list.append(
            """
            {{
                "location":{{
                    "latLng":{{
                        "latitude": {lat},
                        "longitude": {lng}
                    }}
                }}
            }}""".replace("\n", "").format(lat=lat,lng=lng)
        )
    route_list[:-1] = route_list[:-1][:-1]
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline'
    }
    start_point = route_list[0][:-1]
    end_point = route_list[len(route_list)-1][:-1]
    waypoints = route_list[1:-1]
    request_body = JSON_REQUEST.format(start_point,end_point,waypoints).replace("\n", "").replace("\'","")
    response = requests.post(
        url=api_url, 
        data=request_body,
        headers=headers
    )
    print(request_body)
    return None