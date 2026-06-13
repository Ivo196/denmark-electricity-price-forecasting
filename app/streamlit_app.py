from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"


FALLBACK_FINAL_MODEL_COMPARISON = pd.DataFrame(
    [
        {
            "stage": "Robust validation",
            "model": "Walk-forward XGBoost",
            "horizon": "24h ahead",
            "validation": "expanding walk-forward",
            "MAE": 25.48,
            "RMSE": 34.04,
            "notes": "Most realistic validation setup so far",
        },
        {
            "stage": "Robust baseline",
            "model": "Current price baseline",
            "horizon": "24h ahead",
            "validation": "expanding walk-forward",
            "MAE": 28.85,
            "RMSE": 41.83,
            "notes": "Baseline used for walk-forward comparison",
        },
        {
            "stage": "ML model",
            "model": "XGBoost",
            "horizon": "24h ahead",
            "validation": "fixed split",
            "MAE": 25.38,
            "RMSE": 34.53,
            "notes": "Best fixed-split model",
        },
        {
            "stage": "Deep learning",
            "model": "PyTorch LSTM",
            "horizon": "24h ahead",
            "validation": "fixed split",
            "MAE": 34.43,
            "RMSE": 46.71,
            "notes": "Benchmark model",
        },
    ]
)

FALLBACK_FEATURE_SETS = pd.DataFrame(
    [
        {"feature_set": "all_features", "n_features": 32, "MAE": 25.05, "RMSE": 34.41},
        {"feature_set": "price_calendar", "n_features": 13, "MAE": 25.13, "RMSE": 35.02},
        {"feature_set": "price_energy", "n_features": 27, "MAE": 25.15, "RMSE": 34.67},
        {"feature_set": "price_weather", "n_features": 18, "MAE": 25.61, "RMSE": 34.84},
        {"feature_set": "price_only", "n_features": 8, "MAE": 26.62, "RMSE": 36.97},
        {"feature_set": "calendar_only", "n_features": 5, "MAE": 28.00, "RMSE": 37.72},
        {"feature_set": "current_price_baseline", "n_features": 1, "MAE": 28.30, "RMSE": 42.29},
    ]
)

FALLBACK_THRESHOLDS = pd.DataFrame(
    [
        {"threshold": 0, "total_pnl_eur": 100857.71, "n_trades": 5376, "win_rate_pct": 68.36, "avg_pnl_per_trade_eur": 18.76, "max_drawdown_eur": -934.91},
        {"threshold": 5, "total_pnl_eur": 99485.51, "n_trades": 4558, "win_rate_pct": 71.48, "avg_pnl_per_trade_eur": 21.83, "max_drawdown_eur": -793.74},
        {"threshold": 10, "total_pnl_eur": 94298.72, "n_trades": 3787, "win_rate_pct": 74.31, "avg_pnl_per_trade_eur": 24.90, "max_drawdown_eur": -793.74},
        {"threshold": 15, "total_pnl_eur": 84818.56, "n_trades": 3053, "win_rate_pct": 75.96, "avg_pnl_per_trade_eur": 27.78, "max_drawdown_eur": -793.74},
        {"threshold": 20, "total_pnl_eur": 75420.61, "n_trades": 2390, "win_rate_pct": 79.00, "avg_pnl_per_trade_eur": 31.56, "max_drawdown_eur": -793.74},
        {"threshold": 25, "total_pnl_eur": 64481.73, "n_trades": 1804, "win_rate_pct": 81.37, "avg_pnl_per_trade_eur": 35.74, "max_drawdown_eur": -750.25},
        {"threshold": 30, "total_pnl_eur": 53337.55, "n_trades": 1334, "win_rate_pct": 83.58, "avg_pnl_per_trade_eur": 39.98, "max_drawdown_eur": -728.28},
    ]
)

FALLBACK_RISK_SUMMARY = pd.DataFrame(
    [
        {
            "total_pnl_eur": 94298.72,
            "avg_daily_pnl_eur": 419.11,
            "std_daily_pnl_eur": 485.47,
            "best_day_eur": 2716.90,
            "worst_day_eur": -720.76,
            "win_days_pct": 84.44,
        }
    ]
)


@st.cache_data
def load_csv(filename: str, _fallback: pd.DataFrame) -> pd.DataFrame:
    path = REPORTS_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return _fallback.copy()


def format_eur(value: float) -> str:
    return f"EUR {value:,.0f}"


def format_number(value: float) -> str:
    return f"{value:,.2f}"


st.set_page_config(
    page_title="DK2 Electricity Forecasting",
    page_icon=None,
    layout="wide",
)

st.title("DK2 Electricity Price Forecasting")
st.caption("24-hour-ahead forecasting, walk-forward validation, battery arbitrage backtesting, and risk reporting.")

final_models = load_csv("final_model_comparison_DK2.csv", FALLBACK_FINAL_MODEL_COMPARISON)
feature_sets = load_csv("feature_set_comparison_DK2.csv", FALLBACK_FEATURE_SETS)
thresholds = load_csv("economic_backtest_thresholds_DK2.csv", FALLBACK_THRESHOLDS)
risk_summary = load_csv("risk_summary_DK2.csv", FALLBACK_RISK_SUMMARY)

walk_forward = final_models[
    final_models["model"].str.contains("Walk-forward", case=False, na=False)
].head(1)
baseline = final_models[
    final_models["model"].str.contains("baseline", case=False, na=False)
    & final_models["validation"].str.contains("walk-forward", case=False, na=False)
].head(1)

best_strategy = thresholds.loc[thresholds["threshold"].eq(10)].head(1)
if best_strategy.empty:
    best_strategy = thresholds.sort_values("total_pnl_eur", ascending=False).head(1)

risk_row = risk_summary.iloc[0]
model_row = walk_forward.iloc[0] if not walk_forward.empty else final_models.iloc[0]
baseline_row = baseline.iloc[0] if not baseline.empty else final_models.iloc[1]
strategy_row = best_strategy.iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Walk-forward MAE", format_number(model_row["MAE"]), f"{model_row['MAE'] - baseline_row['MAE']:.2f} vs baseline")
col2.metric("Walk-forward RMSE", format_number(model_row["RMSE"]))
col3.metric("Backtested PnL", format_eur(strategy_row["total_pnl_eur"]))
col4.metric("Win Days", f"{risk_row['win_days_pct']:.2f}%")

tab_models, tab_strategy, tab_risk = st.tabs(["Models", "Strategy", "Risk"])

with tab_models:
    left, right = st.columns([1.1, 1])

    with left:
        st.subheader("Model comparison")
        chart_data = final_models.sort_values("MAE").set_index("model")[["MAE"]]
        st.bar_chart(chart_data, height=360, width="stretch")

    with right:
        st.subheader("Feature sets")
        feature_chart = feature_sets.sort_values("MAE").set_index("feature_set")[["MAE"]]
        st.bar_chart(feature_chart, height=360, width="stretch")

    st.dataframe(final_models, width="stretch", hide_index=True)

with tab_strategy:
    left, right = st.columns([1, 1])

    with left:
        st.subheader("PnL by signal threshold")
        pnl_chart = thresholds.set_index("threshold")[["total_pnl_eur"]]
        st.line_chart(pnl_chart, height=360, width="stretch")

    with right:
        st.subheader("Trade quality")
        st.scatter_chart(
            thresholds,
            x="n_trades",
            y="win_rate_pct",
            size="avg_pnl_per_trade_eur",
            color="threshold",
            height=360,
            width="stretch",
        )

    st.dataframe(thresholds, width="stretch", hide_index=True)

with tab_risk:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average daily PnL", format_eur(risk_row["avg_daily_pnl_eur"]))
    col2.metric("Daily PnL volatility", format_eur(risk_row["std_daily_pnl_eur"]))
    col3.metric("Best day", format_eur(risk_row["best_day_eur"]))
    col4.metric("Worst day", format_eur(risk_row["worst_day_eur"]))

    st.subheader("Risk summary")
    st.dataframe(risk_summary, width="stretch", hide_index=True)
