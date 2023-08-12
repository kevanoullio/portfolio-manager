# Purpose: Exchange Listings Extractor module for extracting exchange listings data from various websites.

# Standard Libraries

# Third-party Libraries
import pandas as pd

# Local Modules
from database_management.database import Database
from import_modules.web_scraper import WebScraper
from import_modules.file_management.csv_file_manager import CSVFileManager
from import_modules.file_management.txt_file_manager import TXTFileManager

# Configure logging
import logging


# ExchangeListingsExtractor class for extracting exchange listings data from various websites
class ExchangeListingsExtractor:
    def __init__(self, database: Database) -> None:
        """Class with methods to extract exchange listings data from various websites.

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
        self._df_exchange_listing: pd.DataFrame | None = None
        self._exchange_id: int | None = None

    def _format_url(self, iterable_index: int | None = None) -> str:
        if self._url_iterables is None:
            return f"{self._base_url}{self._exchange_in_url}{self._url_ending}"
        else:
            if iterable_index is None:
                raise ValueError("Iterable index must be specified when there are iterables.")
            return f"{self._base_url}{self._exchange_in_url}/{self._url_iterables[iterable_index]}{self._url_ending}"
 
    def _html_table_to_dataframe(self, table_index: int | None = None) -> None:
        if table_index is None:
            table_index = 0

        # If there are no iterables, read data from the URL and return the DataFrame from the specified table index
        if self._url_iterables is None:
            html_text = self._web_scraper.get_html_content_as_text(self._format_url())
            if html_text is None:
                self._df_exchange_listing = None
            else:
                self._df_exchange_listing = pd.read_html(html_text)[table_index]
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
            self._df_exchange_listing = result_df
    
    def _csv_link_to_dataframe(self, first_column_in_header: str, sort_by_column: str | None = None) -> None:
        # Create a CSVFileManager object
        csv_file = CSVFileManager()
        # Set the first column in the header
        csv_file.set_first_column_in_header(first_column_in_header)
        if self._base_url is None:
            raise ValueError("Base URL must be specified.")
        
        # Read the CSV file from the specified URL
        csv_file.read_csv_from_url(self._format_url())

        if csv_file.get_data() is None:
            return None       

        if sort_by_column is not None:
            # Sort the data by the sort_by_column
            csv_file.sort_data_by_column(sort_by_column)

        # Convert the CSVFileManager object to a DataFrame
        self._df_exchange_listing = csv_file.to_dataframe()
    
    def _txt_link_to_dataframe(self, first_column_in_header: str, delimiter: str) -> None: #, sort_by_column: str | None = None) -> None:
        # Create a TXTFileManager object
        txt_file = TXTFileManager()
        # Set the first column in the header
        txt_file.set_first_column_in_header(first_column_in_header)
        # Set the delimiter
        txt_file.set_delimiter(delimiter)
        if self._base_url is None:
            raise ValueError("Base URL must be specified.")
        
        # Read the TXT file from the specified URL
        txt_file.read_txt_from_url(self._format_url())

        if txt_file.get_data() is None:
            return None

        # Convert the TXTFileManager object to a DataFrame
        self._df_exchange_listing = txt_file.to_dataframe()

    def _filter_dataframe_columns(self, desired_columns: list[str]) -> None:
        if self._df_exchange_listing is None:
            raise ValueError("DataFrame must be initialized before filtering.")
        # Only keep the desired columns if specified
        self._df_exchange_listing = self._df_exchange_listing[desired_columns]

    def _rename_dataframe_columns(self, columns_to_be_renamed: list[str], new_column_names: list[str]) -> None:
        if self._df_exchange_listing is None:
            raise ValueError("DataFrame must be initialized before renaming.")
        # Rename the desired columns
        self._df_exchange_listing.rename(columns=dict(zip(columns_to_be_renamed, new_column_names)), inplace=True)

    def _add_dataframe_column(self, column_name: str, column_data) -> None:
        if self._df_exchange_listing is None:
            raise ValueError("DataFrame must be initialized before adding columns.")
        # Add the column to the DataFrame
        self._df_exchange_listing[column_name] = column_data

    def _filter_dataframe_by_exchange(self, exchange_column_name: str, exchange: str) -> None:
        if self._df_exchange_listing is None:
            raise ValueError("DataFrame must be initialized before filtering.")
        # Create a boolean mask based on the condition
        mask = self._df_exchange_listing[exchange_column_name] == exchange
        # Filter the DataFrame using the boolean mask
        self._df_exchange_listing = self._df_exchange_listing[mask]

    def _get_exchange_id_or_insert(self, country_iso_code: str, exchange_name: str, exchange_acronym: str) -> int | None:
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

    def _extract_nasdaq_trader_exchange_listings(self, exchange_in_url: str, exchange_filter: str | None = None) -> None:
        """
        Extracts the exchange listings from the nasdaqtrader.com website here:
        http://ftp.nasdaqtrader.com/Trader.aspx?id=symbollookup

        NASDAQ listed companies: http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt
        Other listed companies: http://ftp.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt
        """
        # Assign nasdaqtrader.com specific variables
        self._base_url = "http://ftp.nasdaqtrader.com/dynamic/SymDir/"
        self._exchange_in_url = exchange_in_url
        self._url_ending = "listed.txt"

        # Extract the exchange listings from the website
        if exchange_in_url == "nasdaq":
            first_column_in_header = "Symbol"
        elif exchange_in_url == "other":
            first_column_in_header = "ACT Symbol"
        else:
            raise ValueError(f"Exchange '{exchange_in_url}' is not supported.")

        # Extract the exchange listings from the website to a DataFrame
        self._txt_link_to_dataframe(first_column_in_header, "|")
        # If other listings, filter by exchange
        if exchange_filter is not None:
            self._filter_dataframe_by_exchange("Exchange", exchange_filter)
        
        # Check if the exchange listings were successfully retrieved
        if self._df_exchange_listing is None:
            raise ValueError(f"Exchange listings for '{exchange_in_url}' could not be retrieved from the website.")
        
        # Add the exchange_id column
        self._add_dataframe_column("exchange_id", self._exchange_id)
        # Add the currency_id column
        usd_currency_id = self._database.query_executor.get_currency_id_by_currency_iso_code("USD")
        self._add_dataframe_column("currency_id", usd_currency_id)
    
    def _cleanup_nasdaq_trader_exchange_listings(self) -> None:
        # Check if the exchange listings have been extracted
        if self._df_exchange_listing is None:
            raise ValueError("Exchange listings must be extracted before cleaning up.")
        
        # Remove test listings
        self._df_exchange_listing = self._df_exchange_listing[~self._df_exchange_listing["Security Name"].str.contains("NASDAQ TEST")]
        self._df_exchange_listing = self._df_exchange_listing[~self._df_exchange_listing["Security Name"].str.contains("Nasdaq Symbology Test")]
        if self._exchange_in_url == "other":
            # Remove all rows where the Test Issue column is "Y"
            self._df_exchange_listing = self._df_exchange_listing[self._df_exchange_listing["Test Issue"] != "Y"]

        # Remove "File Creation Time" entry at the end of the DataFrame
        self._df_exchange_listing = self._df_exchange_listing[~self._df_exchange_listing[self._df_exchange_listing.columns[0]].str.contains("File Creation Time")]

        # Filter the desired columns
        desired_columns = ["exchange_id", "currency_id", self._df_exchange_listing.columns[0], "Security Name"]
        self._filter_dataframe_columns(desired_columns)
        # Rename all of the remaining columns to match the database
        self._rename_dataframe_columns(desired_columns, ["exchange_id", "currency_id", "symbol", "company_name"])

        # Remove rows with missing values
        self._df_exchange_listing.dropna()
        # Remove rows with duplicate values based on the symbol (first) column
        self._df_exchange_listing.drop_duplicates(subset=[self._df_exchange_listing.columns[0]])

    def initialize_nasdaq_trader_market_data(self, country_iso_code: str, exchange_name: str, exchange_acronym: str, exchange_in_url: str, exchange_filter: str | None) -> None:
        # Get the exchange_id from the database, or insert it if it doesn't exist
        self._get_exchange_id_or_insert(country_iso_code, exchange_name, exchange_acronym)
        # Get the exchange listings from the website
        self._extract_nasdaq_trader_exchange_listings(exchange_in_url, exchange_filter)
        # Cleanup the exchange listings
        self._cleanup_nasdaq_trader_exchange_listings()
        # Insert the exchange listings into the database
        self._insert_exchange_listings_into_database()
        print(f"{exchange_name} listings initialized successfully")
        logging.info(f"{exchange_name} listings initialized successfully")


    def _extract_cboe_canada_exchange_listings(self, exchange_acronym: str, exchange_filter: str) -> None:
        """
        Extracts the exchange listings from the Cboe Canada website here:
        https://cdn.cboe.com/ca/equities/mnow/symbol_listings.csv
        """
        # Assign cdn.cboe.com specific variables
        self._base_url = "https://cdn.cboe.com/ca/equities/mnow/"
        self._exchange_in_url = "symbol_listings"
        self._url_ending = ".csv"

        # Extract the exchange listings from the website
        self._csv_link_to_dataframe(first_column_in_header="company_name", sort_by_column="symbol")
        if self._df_exchange_listing is None:
            raise ValueError(f"Exchange listings for '{exchange_acronym}' could not be retrieved from the website.")
        logging.debug(f"df_exchange_listings after filtering:\n{self._df_exchange_listing}")

        # Filter by exchange
        self._filter_dataframe_by_exchange("mic", exchange_filter)

        # Add the exchange_id column
        self._df_exchange_listing["exchange_id"] = self._exchange_id
        # Convert the currency column to currency_id
        self._df_exchange_listing["currency_id"] = self._df_exchange_listing["currency"].apply(self._database.query_executor.get_currency_id_by_currency_iso_code)
        # Remove the currency column
        self._df_exchange_listing.drop(columns=["currency"], inplace=True)

    def _cleanup_cboe_canada_exchange_listings(self) -> None:
        # Check if the exchange listings have been extracted
        if self._df_exchange_listing is None:
            raise ValueError("Exchange listings must be extracted before cleaning up.")

        # Remove test listings
        self._df_exchange_listing = self._df_exchange_listing[~self._df_exchange_listing["cusip"].str.contains("TEST")]

        # Remove rows without a company name
        self._df_exchange_listing = self._df_exchange_listing[self._df_exchange_listing["company_name"] != ""]
        # Remove the test symbol entry
        self._df_exchange_listing = self._df_exchange_listing[self._df_exchange_listing["symbol"] != "ZYZ.C"]

        # Define the regular expression pattern to match " AT [...]" with any four-letter acronym
        pattern = r"\sAT\s[A-Z]{4}\b$"
        # Remove the pattern from the "company_name" column using regular expressions
        self._df_exchange_listing["company_name"] = self._df_exchange_listing["company_name"].str.replace(pattern, "", regex=True)

        # Filter the desired columns
        desired_columns = ["exchange_id", "currency_id", "symbol", "company_name"]
        self._filter_dataframe_columns(desired_columns)

        # Remove rows with missing values
        self._df_exchange_listing.dropna()
        # Remove rows with duplicate values based on the symbol (first) column
        self._df_exchange_listing.drop_duplicates(subset=[self._df_exchange_listing.columns[0]])

    def initialize_cboe_canada_market_data(self, country_iso_code: str, exchange_name: str, exchange_acronym: str, exchange_filter: str) -> None:
        # Get the exchange_id from the database, or insert it if it doesn't exist
        self._get_exchange_id_or_insert(country_iso_code, exchange_name, exchange_acronym)
        # Get the exchange listings from the website
        self._extract_cboe_canada_exchange_listings(exchange_acronym, exchange_filter)
        # Cleanup the exchange listings
        self._cleanup_cboe_canada_exchange_listings()
        # Insert the exchange listings into the database
        self._insert_exchange_listings_into_database()
        print(f"{exchange_name} listings initialized successfully")
        logging.info(f"{exchange_name} listings initialized successfully")

    def _insert_exchange_listings_into_database(self) -> None:
        # Check if the exchange listings have been extracted
        if self._df_exchange_listing is None:
            raise ValueError("Exchange Listings data must be extracted and put into a data frame before inserting into the database.")
        # Insert the exchange listings into the database
        self._database.query_executor.dataframe_to_existing_sql_table(self._df_exchange_listing, "exchange_listing")

    def get_exchange_listing_dataframe(self) -> pd.DataFrame | None:
        return self._df_exchange_listing


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
