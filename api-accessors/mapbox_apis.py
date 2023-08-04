import requests

URL_START = "https://api.mapbox.com"
API_TOKEN = 'sk.eyJ1IjoidGVjaG5vd29sZiIsImEiOiJjbGt2Z2MwZjUwOTZoM3BtenE0bW51a204In0.V7_wHrtToXeC1bexppCUAg'


def sendOptimizationRequest(travel_style,approximate_route):
    enabled_travel_styles = ['walking']
    optimization_api_template = '{URL_START}/optimized-trips/v1/mapbox/{travel_style}/{gps_points}?access_token={API_TOKEN}'
    if travel_style not in enabled_travel_styles:
        return None
    request_format = ""
    for point in approximate_route:
        request_format += "{lng},{lat};".format(lng=point['geometry']['coordinates'][0],lat=point['geometry']['coordinates'][1])
    request_format = request_format[:-1]
    optimizationRequest = optimization_api_template.format(
        URL_START=URL_START, API_TOKEN=API_TOKEN, travel_style=travel_style, gps_points=request_format
    )
    response = requests.get(optimizationRequest)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def getDatasetList():
    listDatasetsAPI = '{URL_START}/datasets/v1/technowolf?access_token={API_TOKEN}'.format(URL_START=URL_START, API_TOKEN=API_TOKEN)
    
    response = requests.get(listDatasetsAPI)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def getDataset():
    DATASET_ID = "clkua6me70f3j2opap2apzd2g"
    getDataset = '{URL_START}/datasets/v1/technowolf/{DATASET_ID}?access_token={API_TOKEN}'.format(
        URL_START=URL_START, API_TOKEN=API_TOKEN, DATASET_ID=DATASET_ID
    )
    response = requests.get(getDataset)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def getDatasetFeatures():
    DATASET_ID = "clkua6me70f3j2opap2apzd2g"
    getDatasetFeatures = '{URL_START}/datasets/v1/technowolf/{DATASET_ID}/features?access_token={API_TOKEN}'.format(
        URL_START=URL_START, API_TOKEN=API_TOKEN, DATASET_ID=DATASET_ID
    )
    response = requests.get(getDatasetFeatures)
    if response.status_code == 200:
        return response.json().get('features',[])
    else:
        return None
    
    '-0.07662,51.50448;-0.075579,51.503723;-0.078326,51.504999;-0.078716,51.505134;-0.079417,51.504854;-0.08042,51.50517;-0.080236,51.505772;-0.081057,51.505808;-0.083008,51.504919;-0.083398,51.505862;-0.08371,51.50619;-0.084975,51.505823;'