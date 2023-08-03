import requests

URL_START = "https://api.mapbox.com"
API_TOKEN="INSERT_TOKEN_HERE"
def sendOptimizationRequest(travel_style,json_payload):
    enabled_travel_styles = ['walking']
    if travel_style not in enabled_travel_styles:
        return None
    
    optimizationRequest = '{URL_START}/optimized-trips/v1/mapbox/{travel_style}?access_token={API_TOKEN}'.format(
        URL_START=URL_START, API_TOKEN=API_TOKEN, travel_style=travel_style
    )
    response = requests.post(optimizationRequest, json=json_payload)
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