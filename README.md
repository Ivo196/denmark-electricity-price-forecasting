# Denmark Electricity Price Forecasting

A machine learning project to forecast day-ahead electricity spot prices in Denmark (DK1/DK2) and simulate battery storage arbitrage strategies.

## Project Overview

This project uses historical electricity price data from Energi Data Service combined with weather features to train forecasting models. The best model is then used to drive a battery simulator that backtests a simple buy-low/sell-high strategy.

## Data Sources

- **Energi Data Service** – spot prices, production mix, load (`energidataservice.dk`)
- **Open-Meteo / KNMI** – historical weather (wind speed, solar irradiance, temperature)

## Project Structure

```
denmark-electricity-price-forecasting/
├── data/           # Raw, processed, and external datasets
├── notebooks/      # Exploratory and modelling notebooks
├── src/            # Source modules (fetching, features, training, evaluation)
├── reports/        # Figures and final report
└── app/            # Streamlit dashboard
```

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-user/denmark-electricity-price-forecasting.git
cd denmark-electricity-price-forecasting

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your API keys if needed
```

## Usage

```bash
# Run the Streamlit app
streamlit run app/streamlit_app.py
```

## Notebooks

| Notebook | Description |
|---|---|
| `01_data_exploration.ipynb` | EDA of price and weather data |
| `02_feature_engineering.ipynb` | Feature creation and selection |
| `03_model_training.ipynb` | Model training and hyperparameter tuning |
| `04_battery_backtest.ipynb` | Battery arbitrage backtesting |
