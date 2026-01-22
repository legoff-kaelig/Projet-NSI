# https://capacitorjs.com/docs/apis/geolocation#interfaces

import json
import USER_VARIABLES
import FUNCTIONS as func

with open('locations.json', 'r', encoding='utf-8') as file:
    datas = json.load(file)

latitude = datas[0]["latitude"]
longitude = datas[0]["longitude"]
timestamp = datas[0]["timestamp"].split(", ")[1]

if USER_VARIABLES.is_24_hour_format:
    timestamp = func.to_24h(timestamp)