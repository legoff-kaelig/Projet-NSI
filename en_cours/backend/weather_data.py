# https://capacitorjs.com/docs/apis/geolocation#interfaces

import json
import requests

import USER_VARIABLES
import FUNCTIONS as func
from private.API_KEY import API_KEY

locations_path = 'en_cours\\backend\\locations.json'

# Get datas about the user from the JSON files in a DICT
with open(locations_path, 'r', encoding='utf-8') as file:
    datas = json.load(file)

# Extract datas.dict values into variables
latitude = datas[0]["latitude"]
longitude = datas[0]["longitude"]
timestamp = datas[0]["timestamp"].split(", ")[1]

# API request
url = f'https://api.tomorrow.io/v4/weather/forecast?location={latitude},{longitude}&apikey={API_KEY}'
fields = [
    'humidity', 'freezingRainIntensity',
    'precipitationProbability',
    'cloudCover',
    'windDirection', 'windSpeed',
    "iceAccumulation"
]

print(timestamp)