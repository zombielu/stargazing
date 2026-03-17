from datetime import date

import requests


def fetch_weather_for_astronomy(latitude, longitude, d=date.today().isoformat()):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "sunrise,sunset",
        "hourly": "cloudcover,precipitation,apparent_temperature,visibility,windspeed_10m",
        "timezone": "auto",
        "start_date": d,
        "end_date": d
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Failed to fetch weather data")
        return

    data = response.json()
    return data