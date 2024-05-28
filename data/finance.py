# Technical analysis
from type import Stock
from typing import Union
import yfinance as yf
import pandas as pd


def calculate_bollinger_bands(stock: Union[str, Stock]):
    """Get a stock either from Stock object or ticker. Returns Bollinger bands percentage"""
    data = {}

    if isinstance(stock, Stock):
        stock = stock.symbol

    yf_stock = yf.Ticker(stock)
    history = yf_stock.history(period="3mo", interval="1h")
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
