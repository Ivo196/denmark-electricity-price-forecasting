from pathlib import Path

import pandas as pd
import requests

def fetch_open_meteo_weather(
    start_date: str,
    end_date: str,
    latitude: float = 55.6761,
    longitude: float = 12.5683,
) -> pd.DataFrame:
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "temperature_2m",
            "wind_speed_10m",
            "wind_speed_100m",
            "cloud_cover",
            "shortwave_radiation",
        ],
        "timezone": "UTC",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    hourly = data["hourly"]

    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    df = df.rename(columns={"time": "HourUTC"})

    return df


def main():
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    weather = fetch_open_meteo_weather(
        start_date="2024-01-01",
        end_date="2025-02-19",
    )

    output_path = output_dir / "weather_copenhagen_2024_01_01_2025_02_19.csv"
    weather.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(weather.head())
    print(weather.tail())
    print(weather.info())


if __name__ == "__main__":
    main()