import json
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://api.energidataservice.dk/dataset/Elspotprices"

def fetch_day_ahead_prices(start: str, end: str, price_area: str = "DK2") -> pd.DataFrame:
    params = {
        "start": start,
        "end": end,
        "filter": json.dumps({"PriceArea": [price_area]}),
        "limit": 10000,
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    records = response.json().get("records", [])
    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("No data returned. Check dates, dataset name, or PriceArea.")

    return df

def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Print columns first because the API can change field names
    print("Columns:", df.columns.tolist())

    # Most likely time column
    time_col = "HourDK" if "HourDK" in df.columns else "HourUTC"

    df[time_col] = pd.to_datetime(df[time_col])
    df = df.sort_values(time_col)

    return df

def main():
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = fetch_day_ahead_prices(
        start="2024-01-01",
        end="2025-02-20",
        price_area="DK2",
    )

    df = clean_prices(df)

    output_path = output_dir / "elspotprices_DK2_2024_01_01_2025_02_20.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(df.head())
    print(df.tail())

if __name__ == "__main__":
    main()