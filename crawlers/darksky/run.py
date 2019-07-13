#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import pandas as pd
import requests

output_path = Path("data/darksky")

def csv_append_create(csv_path: Path, df: pd.DataFrame):
    if csv_path.exists():
        pd.concat((pd.read_csv(csv_path), df), ignore_index=True).to_csv(csv_path, index=False)
    else:
        df.to_csv(csv_path, index=False)

def main():
    # coordinates for Regensburg
    lat = 49.0195333
    lon = 12.0974869

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    token = (Path(__file__).resolve().parent/"token").read_text().strip()
    response = requests.get(f"https://api.darksky.net/forecast/{token}/{lat},{lon}?units=ca")

    if response.status_code != 200:
        print("Unexpected status code:", response.status_code)
        exit(1)

    forecast = response.json()

    hourly_data = forecast["hourly"]["data"]
    df = pd.DataFrame({
        "forecast_time": [datetime.fromtimestamp(el["time"]) for el in hourly_data],
        "temp": [el["temperature"] for el in hourly_data],
        "precip_prob": [el["precipProbability"] for el in hourly_data],
        "current_time": [current_time] * len(hourly_data)
    })
    csv_append_create(output_path.with_name(output_path.name + "_hourly.csv"), df)

    daily_data = forecast["daily"]["data"]
    df = pd.DataFrame({
        "forecast_time": [datetime.fromtimestamp(el["time"]) for el in daily_data],
        "max_temp": [el["temperatureMax"] for el in daily_data],
        "min_temp": [el["temperatureMin"] for el in daily_data],
        "precip_prob": [el["precipProbability"] for el in daily_data],
        "current_time": [current_time] * len(daily_data)
    })
    csv_append_create(output_path.with_name(output_path.name + "_daily.csv"), df)

if __name__ == "__main__":
    main()
