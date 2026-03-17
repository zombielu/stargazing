import json
import boto3
from datetime import datetime, timezone

s3 = boto3.client("s3")

BUCKET = "weather-info-for-stargazing"

def lambda_handler(event, context):

    params = event.get("queryStringParameters") or {}

    lat = params.get("lat")
    lon = params.get("lon")
    d = params.get("date")

    if not lat or not lon:
        return {
            "statusCode": 400,
            "body": "lat and lon required"
        }

    if not d:
        d = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    key = f"processed/{d}.json"

    obj = s3.get_object(Bucket=BUCKET, Key=key)

    data = json.loads(obj["Body"].read().decode("utf-8"))


    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }



# event = {
#     "queryStringParameters": {
#         "lat": "43.65",
#         "lon": "-79.38",
#         "date": "2026-03-26"
#     }
# }
#
# print(lambda_handler(event, None))