import os
import json

import requests
from datetime import datetime, date
import boto3

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
    print(data)

    # daily data
    daily = data.get("daily", {})
    sunrise = daily.get("sunrise", [None])[0]
    sunset = daily.get("sunset", [None])[0]
    print(daily)

    # hourly data
    hourly = data.get("hourly", {})
    sunrise_dt = datetime.fromisoformat(sunrise)
    sunset_dt = datetime.fromisoformat(sunset)

    times = [datetime.fromisoformat(t) for t in hourly["time"]]

    night_cloud = []
    night_vis = []
    night_wind = []
    night_precip = []
    night_temp = []

    for i, t in enumerate(times):

        # night time data
        if t < sunrise_dt or t > sunset_dt:
            night_cloud.append(hourly["cloudcover"][i])
            night_vis.append(hourly["visibility"][i])
            night_wind.append(hourly["windspeed_10m"][i])
            night_precip.append(hourly["precipitation"][i])
            night_temp.append(hourly["apparent_temperature"][i])

    cloud_mean = sum(night_cloud) / len(night_cloud)
    vis_mean = sum(night_vis) / len(night_vis)
    wind_mean = sum(night_wind) / len(night_wind)
    precip_sum = sum(night_precip)
    temp_mean = sum(night_temp) / len(night_temp)

    # simple evaluation
    score = 0
    reasons = []

    # cloud cover
    if cloud_mean < 30:
        score += 2
        reasons.append(f"Clear sky (average cloud cover {cloud_mean:.1f}%)")
    elif cloud_mean < 60:
        score += 1
        reasons.append(f"Partly cloudy (average cloud cover {cloud_mean:.1f}%)")
    else:
        reasons.append(f"Cloudy (average cloud cover {cloud_mean:.1f}%)")

    # precipitation
    if precip_sum == 0:
        score += 2
        reasons.append("No precipitation during the night")
    else:
        reasons.append(f"Precipitation during the night ({precip_sum:.1f} mm)")

    # visibility
    if vis_mean > 10000:
        score += 1
        reasons.append(f"Good atmospheric transparency (visibility {vis_mean:.0f} m)")
    else:
        reasons.append(f"Moderate visibility ({vis_mean:.0f} m)")

    # wind speed
    if wind_mean < 15:
        score += 1
        reasons.append(f"Calm wind ({wind_mean:.1f} km/h)")
    else:
        reasons.append(f"Strong wind ({wind_mean:.1f} km/h)")

    # output
    print(f"\nAstronomy observation conditions ({d}, lat {latitude}, lon {longitude}):")
    print(f"Sunset: {sunset}, Sunrise: {sunrise}")
    print(f"Average night temperature: {temp_mean:.1f}°C")
    print(f"Observation score: {score}/7")
    print("Reasons:")
    for r in reasons:
        print("-", r)

    if score >= 6:
        print("✅ Excellent conditions for stargazing / meteor observation")
    elif score >= 4:
        print("⚠️ Acceptable conditions but may have some limitations")
    else:
        print("❌ Not suitable for observation")

    output = {
        "location": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "date": d,
        "sunset": sunset,
        "sunrise": sunrise,
        "night_temperature_avg": round(temp_mean, 2),
        "conditions": {
            "cloud_cover_avg": round(cloud_mean, 2),
            "precipitation_total": round(precip_sum, 2),
            "visibility_avg": round(vis_mean, 2),
            "wind_speed_avg": round(wind_mean, 2)
        },
        "observation_score": f"{score}/7"
    }

    # os.makedirs("scores", exist_ok=True)
    # filename = f"{date}.json"
    # with open(filename, "w") as f:
    #     json.dump(output, f, indent=2)
    return output

def upload_to_s3(data):
    s3 = boto3.client("s3")
    bucket = "weather-info-for-stargazing"
    today = date.today().isoformat()
    key = f"processed/{today}.json"

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )


if __name__ == "__main__":
    # Example
    # Toronto coordinates
    output = fetch_weather_for_astronomy(43.65, -79.38, "2026-03-26")
    # upload_to_s3(output)
