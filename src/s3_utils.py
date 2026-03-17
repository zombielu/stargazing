import json

import boto3

BUCKET = "weather-info-for-stargazing"

def save_raw(raw_data):
    s3 = boto3.client("s3")
    bucket = BUCKET
    d = raw_data["daily"]["time"][0]
    print(d)
    key = f"raw/{d}.json"

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(raw_data),
        ContentType="application/json"
    )

def save_processed(data):
    s3 = boto3.client("s3")
    bucket = BUCKET
    d = data["date"]
    print(d)
    key = f"processed/{d}.json"

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )