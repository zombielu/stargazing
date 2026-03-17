import json, boto3, requests
from datetime import datetime, timezone

s3 = boto3.client("s3")
bucket = "weather-info-for-stargazing"

cities = [
    {"name": "Toronto", "lat": 43.65, "lon": -79.38},
    {"name": "New York", "lat": 40.71, "lon": -74.01},
    {"name": "London", "lat": 51.51, "lon": -0.13}
]

def lambda_handler(event, context):
    for city in cities:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={city['lat']}&longitude={city['lon']}&current_weather=true"
        r = requests.get(url)
        key = f"raw/{city['name']}/{datetime.now(timezone.utc).isoformat()}.json"
        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(r.json()))
    return {"status": "success"}
