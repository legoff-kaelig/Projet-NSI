# https://capacitorjs.com/docs/apis/geolocation#interfaces

import os
import sys
import requests
import sqlite3
from datetime import datetime, timedelta

api_dir = os.path.dirname(__file__)
backend_dir = os.path.abspath(os.path.join(api_dir, ".."))
if api_dir not in sys.path:
    sys.path.append(api_dir)
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from API_KEY import API_KEY
from libs.reversegeocoding import ReverseGeocoding
from user_manager import UserManager

DB_PATH = "en_cours\\backend\\DATABASES\\weather.sqlite"

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
aqi_url = 'https://air-quality-api.open-meteo.com/v1/air-quality'


def _build_params(location):
    return {
        'location': location,
        'apikey': API_KEY,
        'units': 'metric',
        'timesteps': '1h'
    }


def _build_aqi_params(latitude, longitude):
    return {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'european_aqi',
        'timezone': 'GMT'
    }


def _resolve_city(latitude, longitude):
    if latitude is None or longitude is None:
        return None

    request = ReverseGeocoding(str(latitude), str(longitude))
    city = request.find_city()
    request.close_connection()
    return city

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


def aqi_get(url, params):
    response = requests.get(url, params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.content}")
        return None

    return response.json()


def create_weather_database(db_path=DB_PATH):
    """Create SQLite database and table for weather data"""
    # Connect to database (creates it if it doesn't exist)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # Create table for weather forecasts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_forecast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
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
            aqi_time TEXT,
            european_aqi REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    return connection, cursor


def _get_last_update_time(user_id, db_path=DB_PATH):
    if not os.path.exists(db_path):
        return None

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'weather_forecast'
        """
    )
    table_row = cursor.fetchone()
    if not table_row:
        connection.close()
        return None

    cursor.execute(
        """
            SELECT created_at
            FROM weather_forecast
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        """,
        (user_id,),
    )
    row = cursor.fetchone()
    connection.close()

    if not row:
        return None

    return _parse_sqlite_timestamp(row[0])


def _parse_sqlite_timestamp(value):
    if not value or len(value) != 19:
        return None

    if value[4] != "-" or value[7] != "-" or value[10] != " " or value[13] != ":" or value[16] != ":":
        return None

    parts = [
        value[0:4],
        value[5:7],
        value[8:10],
        value[11:13],
        value[14:16],
        value[17:19],
    ]
    if not all(part.isdigit() for part in parts):
        return None

    year, month, day, hour, minute, second = [int(part) for part in parts]
    if not (1 <= month <= 12):
        return None
    if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
        return None

    if month == 2:
        leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_day = 29 if leap_year else 28
    elif month in {4, 6, 9, 11}:
        max_day = 30
    else:
        max_day = 31

    if not (1 <= day <= max_day):
        return None

    return datetime(year, month, day, hour, minute, second)


def _get_refresh_rate_minutes(user_id):
    with UserManager() as manager:
        user = manager.get_user(user_id)
    if not user:
        return None
    return user[8]


def _check_refresh_rate(user_id):
    refresh_rate = _get_refresh_rate_minutes(user_id)
    if refresh_rate is None:
        return False, "User not found"

    last_update = _get_last_update_time(user_id)
    if not last_update:
        return True, None

    now = datetime.utcnow()
    elapsed = now - last_update
    if elapsed >= timedelta(minutes=refresh_rate):
        return True, None

    remaining = timedelta(minutes=refresh_rate) - elapsed
    remaining_seconds = int(remaining.total_seconds())
    return False, f"Refresh not ready, wait {remaining_seconds}s"


def _parse_request_timestamp(timestamp_str):
    if not timestamp_str:
        return None
    try:
        return datetime.strptime(timestamp_str, "%m/%d/%Y, %I:%M:%S %p")
    except ValueError:
        return None


def _parse_timeline_time(timeline_time):
    # API returns ISO-8601 with Z suffix (UTC); make it naive for comparison
    parsed = datetime.fromisoformat(timeline_time.replace("Z", "+00:00"))
    if parsed.tzinfo is not None:
        return parsed.replace(tzinfo=None)
    return parsed


def _parse_aqi_time(time_str):
    parsed = datetime.fromisoformat(time_str)
    if parsed.tzinfo is not None:
        return parsed.replace(tzinfo=None)
    return parsed


def _select_current_timeline(hourly_timelines, request_time):
    # Choose the closest hourly record to the request time
    closest = None
    smallest_diff = None
    for timeline in hourly_timelines:
        diff = abs(_parse_timeline_time(timeline["time"]) - request_time)
        if smallest_diff is None or diff < smallest_diff:
            smallest_diff = diff
            closest = timeline
    return closest


def _select_closest_aqi(time_list, request_time):
    closest_index = 0
    smallest_diff = abs(_parse_aqi_time(time_list[0]) - request_time)
    index = 1
    for time_value in time_list[1:]:
        diff = abs(_parse_aqi_time(time_value) - request_time)
        if diff < smallest_diff:
            smallest_diff = diff
            closest_index = index
        index += 1
    return closest_index


def _extract_aqi(aqi_data, request_time):
    hourly = aqi_data.get('hourly')
    if not hourly:
        return None

    time_list = hourly.get('time', [])
    aqi_list = hourly.get('european_aqi', [])
    if not time_list or not aqi_list:
        return None

    index = _select_closest_aqi(time_list, request_time)
    return time_list[index], aqi_list[index]


def save_weather_data(connection, cursor, data, timestamp, user_id, aqi_time, european_aqi):
    """Save current (request time) weather data to SQLite database"""
    hourly_timelines = data['timelines']['hourly']
    request_time = _parse_request_timestamp(timestamp)
    if request_time is None:
        return False
    timeline = _select_current_timeline(hourly_timelines, request_time)

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
        values.get('cloudCover'),
        aqi_time,
        european_aqi
    ]

    # Insert into database
    cursor.execute("""
        INSERT INTO weather_forecast 
        (user_id, timestamp, weather_time, weatherCode, temperature, 
         temperatureApparent, precipitationProbability, humidity, uvIndex, windSpeed, 
         windGust, windDirection, visibility, pressureSeaLevel, rainIntensity, 
         snowIntensity, cloudCover, aqi_time, european_aqi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row_data)

    connection.commit()
    print('Saved current weather record to database')
    return True


def update_weather_for_user(user_id, latitude, longitude, timestamp):
    if latitude is None or longitude is None or timestamp is None:
        return False, "Missing location data"

    allowed, reason = _check_refresh_rate(user_id)
    if not allowed:
        return False, reason

    city = _resolve_city(latitude, longitude)
    with UserManager() as manager:
        manager.update_user_city(user_id, city)

    request_time = _parse_request_timestamp(timestamp)
    if request_time is None:
        return False, "Invalid timestamp format"
    location = f'{latitude},{longitude}'
    params = _build_params(location)

    weather_data = weather_get(url, params, fields_filter)
    if not weather_data:
        return False, "Weather fetch failed"

    aqi_params = _build_aqi_params(latitude, longitude)
    aqi_data = aqi_get(aqi_url, aqi_params)
    if not aqi_data:
        return False, "AQI fetch failed"

    aqi_selection = _extract_aqi(aqi_data, request_time)
    if not aqi_selection:
        return False, "AQI data missing"

    aqi_time, european_aqi = aqi_selection

    connection, cursor = create_weather_database()
    saved = save_weather_data(
        connection,
        cursor,
        weather_data,
        timestamp,
        user_id,
        aqi_time,
        european_aqi,
    )
    connection.close()

    if not saved:
        return False, "Invalid timestamp format"

    return True, {
        "db_path": DB_PATH,
        "user_id": user_id,
        "timestamp": timestamp,
        "aqi_time": aqi_time,
        "european_aqi": european_aqi,
        "city": city,
    }


if __name__ == "__main__":
    print("This module is intended to be used by the HTTP server.")