# Purpose: Import Market Data module for importing market data, cleaning, and storing directly to the database.

# Standard Libraries
import sqlite3
from typing import TypedDict


# Third-party Libraries
import pandas as pd
import yfinance as yf

# Local Modules
from database_management.connection import DatabaseConnection
from import_modules.web_scraper import WebScraper

# Configure logging
import logging


# ExchangeListingsExtractor class for extracting exchange listings from various websites
class ExchangeListingsExtractor:
    def __init__(self, base_url: str, exchange_in_url: str | None=None, url_iterables: list[str] | None=None, url_ending: str | None=None) -> None:
        """Function to extract exchange listings from various websites.

        Args:
            base_url (str): Base URL for the website to read from.
            exchange_in_url (str): Exchange as it's listed in the URL.
            url_iterables (list[str]): List of iterables to iterate through (example A-Z).
            url_ending (str): Ending of the URL.

        Returns:
            None
        """
        self._base_url = base_url
        self._exchange_in_url = exchange_in_url
        self._url_iterables = url_iterables
        self._url_ending = url_ending
        self._web_scraper = WebScraper(user_agent=True)

    def _format_url(self, iterable_index: int | None=None) -> str:
        if self._url_iterables is None:
            return f"{self._base_url}/{self._exchange_in_url}{self._url_ending}"
        else:
            if iterable_index is None:
                raise ValueError("Iterable index must be specified when there are iterables.")
            return f"{self._base_url}/{self._exchange_in_url}/{self._url_iterables[iterable_index]}{self._url_ending}"
 
    def html_table_to_dataframe(self, table_index: int | None=None) -> pd.DataFrame | None:
        if table_index is None:
            table_index = 0

        # If there are no iterables, read data from the URL and return the DataFrame from the specified table index
        if self._url_iterables is None:
            html_text = self._web_scraper.get_html_content_as_text(self._format_url())
            if html_text is None:
                return None
            return pd.read_html(html_text)[table_index]
        
        # Iterate over the url iterables, read data from each URL, and store the DataFrames in a list
        dataframes_list = []
        for i, iterable in enumerate(self._url_iterables):
            html_text = self._web_scraper.get_html_content_as_text(self._format_url(i))
            if html_text is None:
                return None
            tables = pd.read_html(html_text)
            # Grab the 5th table and keep only the columns we want, "Code" and "Name"
            table = tables[table_index][["Code", "Name"]]
            dataframes_list.append(table)

        # Concatenate all DataFrames in the list
        result_df = pd.concat(dataframes_list, ignore_index=True)
        # Rename the columns
        result_df.columns = ["symbol", "company_name"]
        return result_df
    
    def csv_to_dataframe(self, csv_file: list[dict[str, str]]) -> pd.DataFrame | None:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)


class AssetInfoExtractor:
    def __init__(self, symbols: list[str]) -> None:
        self._symbols = symbols

    def get_asset_info(self, symbol: str) -> dict[str, str]:
        data = yf.Ticker(symbol)
        # Keep only the key/value pairs we want
        asset_info = {key: data.info[key] for key in ["quoteType", "sector", "industry", "country", "city", "currency", "exchange", "symbol", "longName", "longBusinessSummary", "website", "logo_url"]}
        return asset_info


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


class IndexData(TypedDict):
    name: str
    symbol: str
    website_url: str
    table_index: int
    symbol_column: str


class IndexHoldingsExtractor:
    def __init__(self, index_data: IndexData) -> None:
        self._index_data = index_data

    def get_holdings_from_index(self) -> pd.DataFrame | None:
        # Reate the HTML text from the specified URL
        html_text = WebScraper(user_agent=True).get_html_content_as_text(self._index_data["website_url"])
        if html_text is None:
            return None
        # Extract the tables from the HTML text
        html_tables = pd.read_html(html_text)
        # Access the specific table based on the table_index
        index_table = html_tables[self._index_data["table_index"]]
        # Extract the column indicated by "ticker_column" and convert to a list
        index_holdings = index_table[self._index_data["symbol_column"]].tolist()
        # Create a DataFrame from the list of tickers
        index_holdings_df = pd.DataFrame(index_holdings, columns=["symbol"])
        return index_holdings_df



def main():
    # TODO - grab all info for each stock from yfinance and store in the database

    wiki = "https://en.wikipedia.org/wiki/"

    sp500 = "List_of_S&P_500_companies"
    nasdaq100 = "NASDAQ-100"
    dow30 = "Dow_Jones_Industrial_Average"
    russell2000 = "Russell_2000_Index"
    tsx60 = "S&P/TSX_60"
    tsx_composite = "S&P/TSX_Composite_Index"

    index_wiki_url = {
        "S&P 500": wiki + sp500,
        "NASDAQ 100": wiki + nasdaq100,
        "Dow Jones Industrial Average": wiki + dow30,
        "Russell 2000": wiki + russell2000,
        "S&P/TSX 60": wiki + tsx60,
        "S&P/TSX Composite Index": wiki + tsx_composite
    }

    index_holdings = {
        "S&P 500": [],
        "NASDAQ 100": [],
        "Dow Jones Industrial Average": [],
        "Russell 2000": [],
        "S&P/TSX 60": [],
        "S&P/TSX Composite Index": []
    }

    
if __name__ == "__main__":
    print("This module is not meant to be executed directly...")
