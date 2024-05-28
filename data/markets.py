import yfinance as yf
from type import Stock, StockData
import json


def get_current_stock_price(ticker: str) -> float:
    stock = yf.Ticker(ticker)
    return stock.info["currentPrice"]


def get_stock_by_ticker(ticker: str) -> Stock:
    stock = yf.Ticker(ticker)
    return Stock(ticker=stock, data=StockData.from_dict(stock.info))
