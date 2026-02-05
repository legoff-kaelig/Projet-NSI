# https://capacitorjs.com/docs/apis/geolocation#interfaces

import json
import requests
import sqlite3
# from datetime import datetime

from API_KEY import API_KEY

locations_path = 'en_cours\\backend\\locations.json'
DB_PATH = "en_cours\\backend\\DATABASES\\weather.sqlite"

# Get datas about the user from the JSON files in a DICT
with open(locations_path, 'r', encoding='utf-8') as file:
    datas = json.load(file)

# Extract datas.dict values into variables
latitude = datas[0]["latitude"]
longitude = datas[0]["longitude"]
timestamp = datas[0]["timestamp"].split(", ")[1]
user_id = datas[0].get("user_id", 1)

# API request - Build URL with query parameters
location = f'{latitude},{longitude}'

fields_filter = [               # INDICATION FRONT END
    'weatherCode',              # Pour les icônes météo (Image avec les nuages/soleil/... en haut à gauche)
    'temperature',              # Température réelle ({IN FIRST BLOCK})
    'temperatureApparent',      # Ressenti (Feels like)
    'precipitationProbability', # Risque de pluie (Precipitation)
    'humidity',                 # Taux d'humidité (Humidity)
    'uvIndex',                  # Indice UV                             NON IMPLEMENTE DANS LE FRONT END 
    'windSpeed',                # Vitesse du vent (Wind)
    'windGust',                 # Rafales de vent                       NON IMPLEMENTE DANS LE FRONT END
    'windDirection',            # Direction du vent                     NON IMPLEMENTE DANS LE FRONT END
    'visibility',               # Visibilité                            NON IMPLEMENTE DANS LE FRONT END
    'pressureSeaLevel',         # Pression atmosphérique (Baromètre)    NON IMPLEMENTE DANS LE FRONT END
    'rainIntensity',            # Intensité de la pluie (mm/h)          NON IMPLEMENTE DANS LE FRONT END
    'snowIntensity',            # Intensité de la neige                 NON IMPLEMENTE DANS LE FRONT END
    'cloudCover',               # Couverture nuageuse (%)               NON IMPLEMENTE DANS LE FRONT END
]

# Build URL with all parameters
url = 'https://api.tomorrow.io/v4/weather/forecast'
params = {
    'location': location,
    'apikey': API_KEY,
    'units': 'metric',
    'timesteps': '1h'
}

def weather_get(url, params, fields_filter):
    # Get API response
    response = requests.get(url, params)

    if response.status_code != 200:
        print(f'Error: {response.status_code} - {response.content}')
        return None
    
    data = response.json()
    
    # Filter the weather data to only keep the fields we want
    hourly_timelines = data['timelines']['hourly']
    
    for timeline in hourly_timelines:
        # Get all the weather values for an hour
        all_values = timeline['values']
        
        # Create a dictionary with the fields in the list fields_filter
        filtered_values = {}
        for field_name, field_value in all_values.items():
            if field_name in fields_filter:
                filtered_values[field_name] = field_value
        
        timeline['values'] = filtered_values
    
    return data


def create_weather_database(db_path=DB_PATH):
    """Create SQLite database and table for weather data"""
    # Connect to database (creates it if it doesn't exist)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # Create table for weather forecasts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_forecast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id REAL NOT NULL,
            timestamp TEXT NOT NULL,
            weather_time TEXT NOT NULL,
            weatherCode INTEGER,
            temperature REAL,
            temperatureApparent REAL,
            precipitationProbability REAL,
            humidity REAL,
            uvIndex REAL,
            windSpeed REAL,
            windGust REAL,
            windDirection REAL,
            visibility REAL,
            pressureSeaLevel REAL,
            rainIntensity REAL,
            snowIntensity REAL,
            cloudCover REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    connection.commit()


def save_weather_data(connection, cursor, data, timestamp, user_id):
    """Save filtered weather data to SQLite database"""
    hourly_timelines = data['timelines']['hourly']
    
    for timeline in hourly_timelines:
        # Get the time and values for this forecast
        weather_time = timeline['time']
        values = timeline['values']
        
        # Prepare data for insertion
        row_data = [
            user_id,
            timestamp,
            weather_time,
            values.get('weatherCode'),
            values.get('temperature'),
            values.get('temperatureApparent'),
            values.get('precipitationProbability'),
            values.get('humidity'),
            values.get('uvIndex'),
            values.get('windSpeed'),
            values.get('windGust'),
            values.get('windDirection'),
            values.get('visibility'),
            values.get('pressureSeaLevel'),
            values.get('rainIntensity'),
            values.get('snowIntensity'),
            values.get('cloudCover')
        ]
        
        # Insert into database
        cursor.execute("""
            INSERT INTO weather_forecast 
            (user_id, timestamp, weather_time, weatherCode, temperature, 
             temperatureApparent, precipitationProbability, humidity, uvIndex, windSpeed, 
             windGust, windDirection, visibility, pressureSeaLevel, rainIntensity, 
             snowIntensity, cloudCover)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row_data)
    
    connection.commit()
    print(f'Saved {len(hourly_timelines)} weather records to database')


# Get weather data
weather_data = weather_get(url, params, fields_filter)

if weather_data:
    # Create database and save data
    connection, cursor = create_weather_database()
    save_weather_data(connection, cursor, weather_data, timestamp, user_id)
    connection.close()
    print(f'Database saved: {DB_PATH}')