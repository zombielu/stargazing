from datetime import datetime


def compute_score(data):
    d = data["daily"]["time"][0]
    latitude = data["latitude"]
    longitude = data["longitude"]
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

        # nighttime data
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
        reasons.append(
            f"Partly cloudy (average cloud cover {cloud_mean:.1f}%)")
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
        reasons.append(
            f"Good atmospheric transparency (visibility {vis_mean:.0f} m)")
    else:
        reasons.append(f"Moderate visibility ({vis_mean:.0f} m)")

    # wind speed
    if wind_mean < 15:
        score += 1
        reasons.append(f"Calm wind ({wind_mean:.1f} km/h)")
    else:
        reasons.append(f"Strong wind ({wind_mean:.1f} km/h)")

    # output
    print(
        f"\nAstronomy observation conditions ({d}, lat {latitude}, lon {longitude}):")
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
            "latitude": data["latitude"],
            "longitude": data["longitude"],
        },
        "date": data["daily"]["time"][0],
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

    return output