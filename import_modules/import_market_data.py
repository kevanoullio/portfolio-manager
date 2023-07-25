# Purpose: Import Market Data module for importing market data, cleaning, and storing directly to the database.

# Standard Libraries
import sqlite3
from typing import TypedDict


# Third-party Libraries
import pandas as pd
import yfinance as yf

# Local Modules
from database_management.connection import DatabaseConnection, DatabaseConnectionError

# Configure logging
import logging


# ImportMarketData class for importing market data as a Pandas DataFrame and storing it directly to the database
class ImportMarketData:
    def __init__(self, db_connection: DatabaseConnection) -> None:
        self._db_connection = db_connection

    def pandas_to_existing_sql_table(self, dataframe: pd.DataFrame, table_name: str) -> None:
        # Check if the dataframe is not None
        if dataframe is not None:
            # Access the underlying database connection object
            conn = self._db_connection.connection
            # Check if the connection is None or not
            if conn is not None:
                try:
                    # Insert all rows from the dataframe into the existing database table
                    dataframe.to_sql(table_name, conn, index=False, if_exists="append")
                    logging.info(f"Dataframe inserted into the {table_name} table.")
                except sqlite3.IntegrityError as e:
                    logging.error(f"Dataframe could not be inserted into the {table_name} table. {e}")
            else:
                raise DatabaseConnectionError(self._db_connection, "Database connection is None.")
        else:
            logging.error("Dataframe is None.")


class ExchangeListingsExtractor:
    def __init__(self, base_url: str, exchange_in_url: str, url_iterables: list[str] | None=None) -> None:
        """Function to extract exchange listings from various websites.

        Args:
            base_url (str): Base URL for the website to read from.
            exchange (str): Exchange as it's listed in the URL.
            iterables (list[str]): List of iterables to iterate through (example A-Z).

        Returns:
            None
        """
        self._base_url = base_url
        self._exchange_in_url = exchange_in_url
        self._url_iterables = url_iterables

    def _format_eod_url(self, iterable_index: int | None=None) -> str:
        if self._url_iterables is None:
            return f"{self._base_url}/{self._exchange_in_url}.htm"
        else:
            if iterable_index is None:
                raise ValueError("Iterable index must be specified when there are iterables.")
            return f"{self._base_url}/{self._exchange_in_url}/{self._url_iterables[iterable_index]}.htm"
 
    def eoddata_to_dataframe(self) -> pd.DataFrame:
        # If there are no iterables, read data from the URL and return the DataFrame from the 5th table
        if self._url_iterables is None:
            return pd.read_html(self._format_eod_url())[4]
        
        # Iterate over the url iterables, read data from each URL, and store the DataFrames in a list
        dataframes_list = []
        for i, iterable in enumerate(self._url_iterables):
            tables = pd.read_html(self._format_eod_url(i))
            # Grab the 5th table and keep only the columns we want, "Code" and "Name"
            table = tables[4][["Code", "Name"]]
            dataframes_list.append(table)

        # Concatenate all DataFrames in the list
        result_df = pd.concat(dataframes_list, ignore_index=True)
        # Rename the columns
        result_df.columns = ["symbol", "company name"]
        return result_df

    def print_all_tables(self) -> None:
        """Prints all tables from the list of tables.

        Args:
            None

        Returns:
            None
        """
        tables = self.eoddata_to_dataframe()
        for idx, table in enumerate(tables):
            print(f"Table {idx+1}:")
            print(table)
            print("\n")

    def print_dataframe(self) -> None:
        """Prints the dataframe.

        Args:
            None
        
        Returns:
            None
        """
        df = self.eoddata_to_dataframe()
        print(f"Dataframe:")
        print(df)
        print("\n")


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


def save_to_db(table: str, data: pd.DataFrame) -> None:
    conn = sqlite3.connect("historical_data.db")
    cursor = conn.cursor()

    for row in data:
        cursor.execute("INSERT INTO asset_price_history ([date], open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)", row)
        conn.commit()

    conn.close()


class IndexData(TypedDict):
    name: str
    symbol: str
    website_url: str
    table_index: int
    symbol_column: str


class IndexHoldingsExtractor:
    def __init__(self, index_data: IndexData) -> None:
        self._index_data = index_data

    def get_holdings_from_index(self) -> pd.DataFrame:
        # Read the HTML tables from the specified URL
        html_tables = pd.read_html(self._index_data["website_url"])
        # Access the specific table based on the table_index
        index_table = html_tables[self._index_data["table_index"]]
        # Extract the column indicated by "ticker_column" and convert to a list
        index_holdings = index_table[self._index_data["symbol_column"]].tolist()
        
        # Create a DataFrame from the list of tickers
        index_holdings_df = pd.DataFrame(index_holdings, columns=["symbol"])
        return index_holdings_df




def main():
    tsx = ExchangeListingsExtractor("https://eoddata.com/stocklist/", "TSX/", list("A")) # list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    df_tsx = tsx.eoddata_to_dataframe()
    print(df_tsx)

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

    

