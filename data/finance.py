# Technical analysis
from type import Stock
from typing import Union
import yfinance as yf
import pandas as pd


def calculate_bollinger_bands(stock: Stock):
    """Get a stock either from Stock object or ticker. Returns Bollinger bands percentage"""
    data = {}
    history = stock.get_history()

    if history.empty:
        return

    data["SMA"] = history["Close"].rolling(window=20).mean()  # Calculate 20 day sma
    data["SD"] = (
        history["Close"].rolling(window=20).std()
    )  # Calculate 20 period standard devision
    data["UB"] = data["SMA"] + 2 * data["SD"]  # Calculate upper band
    data["LB"] = data["SMA"] - 2 * data["SD"]  # Calculate lower band

    latest_close = history["Close"].iloc[-1]
    latest_lb = data["LB"].iloc[-1]
    latest_ub = data["UB"].iloc[-1]

    if not pd.isna(latest_lb) and not pd.isna(latest_ub):
        bb_percent = (latest_close - latest_lb) / (latest_ub - latest_lb) * 100
    else:
        bb_percent = None

    return bb_percent


def calculate_rsi(stock: Stock, period=14):
    """Calculate the RSI. 70 or above indicates over bought, 30 or below oversold."""
    history = stock.get_history(period="3mo", interval="1d")

    if history.empty:
        return None

    history["Price Change"] = history["Close"].diff()  # Calculate price changes

    history["Gain"] = history["Price Change"].apply(lambda x: x if x > 0 else 0)
    history["Loss"] = history["Price Change"].apply(lambda x: -x if x < 0 else 0)

    history["Avg Gain"] = history["Gain"].rolling(window=period, min_periods=1).mean()
    history["Avg Loss"] = history["Loss"].rolling(window=period, min_periods=1).mean()

    # Calculate the Relative Strength (RS)
    history["RS"] = history["Avg Gain"] / history["Avg Loss"]

    # Calculate the RSI
    history["RSI"] = 100 - (100 / (1 + history["RS"]))

    return history.tail(1)["RSI"]
