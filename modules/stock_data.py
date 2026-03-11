import yfinance as yf
import pandas as pd


def get_stock_data(ticker, period="1y"):
    """
    Fetch historical stock data
    """

    stock = yf.Ticker(ticker)

    data = stock.history(period=period)

    return data


def get_current_price(ticker):
    """
    Fetch latest stock price
    """

    stock = yf.Ticker(ticker)

    price = stock.history(period="1d")["Close"].iloc[-1]

    return price


def get_stock_info(ticker):
    """
    Fetch basic company information
    """

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "company": info.get("longName"),
        "sector": info.get("sector"),
        "market_cap": info.get("marketCap")
    }