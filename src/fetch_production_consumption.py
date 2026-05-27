import json
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://api.energidataservice.dk/dataset/ProductionConsumptionSettlement"

def fetch_production_consumption(start: str, end: str, price_area: str = "DK2",) -> pd.DataFrame:
    params = {
        "start": start,
        "end": end,
        "filter": json.dumps({"PriceArea": [price_area]}),
        "limit": 10000,
        "sort": "HourDK",
    }

    response = requests.get(API_URL, params=params, timeout=30)

    print("URL:", response.url)
    print("Status code:", response.status_code)

    if response.status_code == 429:
        print("Rate limit reached. Wait before trying again.")
        print(response.text)
        return pd.DataFrame()

    response.raise_for_status()

    records = response.json().get("records", [])
    df = pd.DataFrame(records)

    if df.empty:
        print("No records returned.")
        return df

    print("Columns:", df.columns.tolist())
    print(df.head())
    print(df.tail())
    print(df.info())

    return df

def main():
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Primero probamos solo 7 días para ver columnas reales.
    df = fetch_production_consumption(
        start="2024-01-01",
        end="2025-02-20",
        price_area="DK2",
    )

    if df.empty:
        print("No file saved.")
        return

    output_path = output_dir / "production_consumption_DK2_2024_01_01_2025_02_20.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()