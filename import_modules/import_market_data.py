# Purpose: Import Market Data module for importing market data, cleaning, and storing directly to the database.

# Standard Libraries
import sqlite3
from typing import TypedDict


# Third-party Libraries
import pandas as pd
import yfinance as yf

# Local Modules
from database_management.database import Database
from import_modules.web_scraper import WebScraper
from import_modules.csv_file_manager import CSVFileManager

# Configure logging
import logging


# ExchangeListingsExtractor class for extracting exchange listings from various websites
class ExchangeListingsExtractor:
    def __init__(self, database: Database) -> None:
        """Function to extract exchange listings from various websites.

        Args:
            database (Database): Database object for managing the database.

        Returns:
            None
        """
        self._database = database
        self._base_url: str | None = None
        self._exchange_in_url: str | None = None
        self._url_iterables: list[str] | None = None
        self._url_ending: str | None = None
        self._web_scraper = WebScraper(user_agent=True)
        self._exchange_listings: pd.DataFrame | None = None
        self._exchange_id: int | None = None
    
    def get_dataframe(self) -> pd.DataFrame | None:
        return self._exchange_listings

    def _format_url(self, iterable_index: int | None = None) -> str:
        if self._url_iterables is None:
            return f"{self._base_url}/{self._exchange_in_url}{self._url_ending}"
        else:
            if iterable_index is None:
                raise ValueError("Iterable index must be specified when there are iterables.")
            return f"{self._base_url}/{self._exchange_in_url}/{self._url_iterables[iterable_index]}{self._url_ending}"
 
    def _html_table_to_dataframe(self, table_index: int | None = None) -> None:
        if table_index is None:
            table_index = 0

        # If there are no iterables, read data from the URL and return the DataFrame from the specified table index
        if self._url_iterables is None:
            html_text = self._web_scraper.get_html_content_as_text(self._format_url())
            if html_text is None:
                self._exchange_listings = None
            else:
                self._exchange_listings = pd.read_html(html_text)[table_index]
        else:
            # Iterate over the url iterables, read data from each URL, and store the DataFrames in a list
            dataframes_list = []
            for i, iterable in enumerate(self._url_iterables):
                html_text = self._web_scraper.get_html_content_as_text(self._format_url(i))
                if html_text is None:
                    return None
                tables = pd.read_html(html_text)

                # Grab the nth table
                table = tables[table_index]
                
                # Append the DataFrame to the list
                dataframes_list.append(table)

            # Concatenate all DataFrames in the list
            result_df = pd.concat(dataframes_list, ignore_index=True)
            
            # Store the result DataFrame
            self._exchange_listings = result_df
    
    def _csv_link_to_dataframe(self, first_column_in_header: str, sort_by_column: str | None = None) -> None:
        # Read the CSV file from the specified URL
        csv_file = CSVFileManager()
        csv_file.set_first_column_in_header(first_column_in_header)
        if self._base_url is None:
            raise ValueError("Base URL must be specified.")
        csv_file.read_csv_from_url(self._base_url)

        if csv_file.get_data() is None:
            return None       

        if sort_by_column is not None:
            # Sort the data by the sort_by_column
            csv_file.sort_data_by_column(sort_by_column)

        # Convert the CSVFileManager object to a DataFrame
        self._exchange_listings = csv_file.to_dataframe()

    def _filter_and_rename_dataframe_columns(self, desired_columns: list[str], rename_desired_columns: list[str] | None = None) -> None:
        if self._exchange_listings is None:
            raise ValueError("DataFrame must be initialized before filtering.")
        # Only keep the desired columns if specified
        self._exchange_listings = self._exchange_listings[desired_columns]
        # Rename the desired columns if specified
        if rename_desired_columns is not None:
            self._exchange_listings.columns = rename_desired_columns

    def _filter_dataframe_by_exchange(self, exchange: str) -> None:
        if self._exchange_listings is None:
            raise ValueError("DataFrame must be initialized before filtering.")
        # Create a boolean mask based on the condition
        mask = self._exchange_listings["mic"] == exchange
        # Filter the DataFrame using the boolean mask
        self._exchange_listings = self._exchange_listings[mask]

    def get_exchange_id_by_exchange_acronym_or_insert(self, country_iso_code: str, exchange_name: str, exchange_acronym: str) -> int | None:
        # Get the exchange_id from the database
        exchange_id = self._database.query_executor.get_exchange_id_by_exchange_acronym(exchange_acronym)
        # If the exchange doesn't exist in the database, insert it
        if exchange_id is None:
            # Get the country_id from the database
            country_id = self._database.query_executor.get_country_id_by_country_iso_code(country_iso_code)
            if country_id is None:
                raise ValueError(f"Country ISO Code '{country_iso_code}' does not exist in the database.")
            self._database.query_executor.insert_exchange(country_id, exchange_name, exchange_acronym)
            exchange_id = self._database.query_executor.get_exchange_id_by_exchange_acronym(exchange_acronym)
        # Check if the exchange_id was successfully retrieved or inserted
        if exchange_id is None:
            raise ValueError(f"Exchange acronym '{exchange_acronym}' does not exist in the database.")
        self._exchange_id = exchange_id

    def initialize_eoddata_exchange_listings(self, exchange_acronym: str) -> None:
        # Assign eoddata.com specific variables
        self._base_url = "https://eoddata.com/stocklist/"
        self._exchange_in_url = exchange_acronym
        self._url_iterables = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self._url_ending = ".htm"
        
        # Extract the exchange listings from the website
        self._html_table_to_dataframe(table_index=4)
        self._filter_and_rename_dataframe_columns(["Code", "Name"], ["symbol", "company_name"])
        if self._exchange_listings is None:
            raise ValueError(f"Exchange listings for '{exchange_acronym}' could not be retrieved from the website.")
        
        # Add the exchange_id column
        self._exchange_listings["exchange_id"] = self._exchange_id
        # Remove rows with missing values
        self._exchange_listings.dropna()
        # Remove rows with duplicate values
        self._exchange_listings.drop_duplicates(subset=["exchange_id", "symbol"])

        # Insert the exchange listings into the database
        self._database.query_executor.dataframe_to_existing_sql_table(self._exchange_listings, "exchange_listing")

    def initialize_cboe_canada_exchange_listings(self, exchange_acronym: str, mic_filter: str) -> None:
        # Assign cdn.cboe.com specific variables
        self._base_url = "https://cdn.cboe.com/ca/equities/mnow/symbol_listings.csv"

        # Extract the exchange listings from the website
        self._csv_link_to_dataframe(first_column_in_header="company_name", sort_by_column="symbol")
        self._filter_dataframe_by_exchange(mic_filter)
        self._filter_and_rename_dataframe_columns(["symbol", "company_name"])
        if self._exchange_listings is None:
            raise ValueError(f"Exchange listings for '{exchange_acronym}' could not be retrieved from the website.")
        logging.debug(f"df_exchange_listings after filtering:\n{self._exchange_listings}")
        
        # Add the exchange_id column
        self._exchange_listings["exchange_id"] = self._exchange_id

        # Remove rows with missing values
        self._exchange_listings.dropna()
        # Remove rows with duplicate values
        self._exchange_listings.drop_duplicates(subset=["exchange_id", "symbol"])
        # Remove rows without a company name
        self._exchange_listings = self._exchange_listings[self._exchange_listings["company_name"] != ""]
        # Remove the test symbol entry
        self._exchange_listings = self._exchange_listings[self._exchange_listings["symbol"] != "ZYZ.C"]

        # Define the regular expression pattern to match " AT [...]" with any four-letter acronym
        pattern = r"\sAT\s[A-Z]{4}\b$"
        # Remove the pattern from the "company_name" column using regular expressions
        self._exchange_listings["company_name"] = self._exchange_listings["company_name"].str.replace(pattern, "", regex=True)
        
        # Insert the exchange listings into the database
        self._database.query_executor.dataframe_to_existing_sql_table(self._exchange_listings, "exchange_listing")


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
