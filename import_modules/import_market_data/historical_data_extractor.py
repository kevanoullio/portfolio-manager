# Purpose: Import Market Data module for importing market data, cleaning, and storing directly to the database.

# Standard Libraries

# Third-party Libraries
import pandas as pd
import yfinance as yf

# Local Modules
from import_modules.web_scraper import WebScraper

# Configure logging
import logging


# HistoricalDataExtractor class for extracting historical data
class HistoricalDataExtractor:
    def __init__(self, symbols: list[str]) -> None:
        self._symbols = symbols

    def get_historical_price_data(self, symbol: str) -> pd.DataFrame:
        data = yf.download(symbol, period="max", interval="1d", actions=True)
        # Reset index to get Date as a column instead of an index
        data.reset_index(inplace=True)
        return data[["Date", "Ticker", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]

    def get_historical_dividend_data(self, symbol: str) -> pd.DataFrame:
        data = yf.download(symbol, period="max", interval="1d", actions=True)
        # Reset index to get Date as a column instead of an index
        data.reset_index(inplace=True)
        return data[["Date", "Ticker", "Dividend"]]

    def get_historical_split_data(self, symbol: str) -> pd.DataFrame:
        data = yf.download(symbol, period="max", interval="1d", actions=True)
        # Reset index to get Date as a column instead of an index
        data.reset_index(inplace=True)
        return data[["Date", "Ticker", "Stock Split"]]

    
if __name__ == "__main__":
    print("This module is not meant to be executed directly...")
