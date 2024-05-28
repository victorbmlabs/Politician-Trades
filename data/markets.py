import yfinance as yf
from type import Stock
import json


def get_current_stock_price(ticker: str) -> float:
    stock = yf.Ticker(ticker)
    return stock.info["currentPrice"]


def get_stock_by_ticker(ticker: str) -> Stock:
    stock = yf.Ticker(ticker)
    return Stock.from_dict(stock.info)
