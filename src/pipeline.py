from fetch_weather import fetch_weather_for_astronomy
from compute_score import compute_score
from s3_utils import save_raw, save_processed
from datetime import date, timedelta

# toronto lat, lon
lat = 43.65
lon = -79.38
date_after_15_days = date.today() + timedelta(days=15)

def run_pipeline():
    raw = fetch_weather_for_astronomy(latitude=lat, longitude=lon, d=date_after_15_days)
    save_raw(raw)
    score = compute_score(raw)
    save_processed(score)

if __name__ == '__main__':
    run_pipeline()