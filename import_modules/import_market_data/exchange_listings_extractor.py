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


# Website links:
# http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt
# http://ftp.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt
# https://cdn.cboe.com/ca/equities/mnow/symbol_listings.csv

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
        self._df_exchange_listings_info: pd.DataFrame | None = None
        self._exchange_id: int | None = None
        self._asset_class_names: list[str] | None = None
        self._asset_class_lookup: dict | None = None

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
        self._df_exchange_listings_info = csv_file.to_dataframe()
    
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
        self._df_exchange_listings_info = txt_file.to_dataframe()

    def _filter_dataframe_columns(self, desired_columns: list[str]) -> None:
        if self._df_exchange_listings_info is None:
            raise ValueError("DataFrame must be initialized before filtering.")
        # Only keep the desired columns if specified
        try:
            self._df_exchange_listings_info = self._df_exchange_listings_info[desired_columns]
        except KeyError as err:
            print(f"KeyError: {err}")


    def _rename_dataframe_columns(self, columns_to_be_renamed: list[str], new_column_names: list[str]) -> None:
        if self._df_exchange_listings_info is None:
            raise ValueError("DataFrame must be initialized before renaming.")
        # Rename the desired columns
        self._df_exchange_listings_info.rename(columns=dict(zip(columns_to_be_renamed, new_column_names)), inplace=True)

    def _add_dataframe_column(self, column_name: str, column_data) -> None:
        if self._df_exchange_listings_info is None:
            raise ValueError("DataFrame must be initialized before adding columns.")
        # Add the column to the DataFrame
        self._df_exchange_listings_info[column_name] = column_data

    def _filter_dataframe_by_exchange(self, exchange_column_name: str, exchange: str) -> None:
        if self._df_exchange_listings_info is None:
            raise ValueError("DataFrame must be initialized before filtering.")
        # Create a boolean mask based on the condition
        mask = self._df_exchange_listings_info[exchange_column_name] == exchange
        # Filter the DataFrame using the boolean mask
        self._df_exchange_listings_info = self._df_exchange_listings_info[mask]

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
            # Check if the exchange_id was successfully inserted
            if exchange_id is None:
                raise ValueError(f"Exchange acronym '{exchange_acronym}' does not exist in the database.")
        self._exchange_id = exchange_id
    
    # def _build_asset_class_and_subclass_lookup(self) -> None:
    #     """
    #     This method builds a dictionary to store asset class names, subclasses, and their synonyms.

    #     Updates the internal `_asset_class_lookup` attribute.

    #     `_asset_class_lookup` dict structure:
    #         A dictionary where the key is the asset class name and the value is another dictionary.
    #         The inner dictionary has two keys:
    #             - 'subclasses': a list of asset subclasses for the class
    #             - 'synonyms': a list of synonyms for both the class and subclasses (combined)

    #     Raises:
    #         ValueError: If asset class names or subclass names cannot be retrieved from the database.
    #     """

    #     # Initialize the asset class lookup dictionary
    #     self._asset_class_lookup = {}

    #     # Get all asset class names and subclasses from the database
    #     asset_class_names = self._database.query_executor.get_all_asset_class_names()

    #     if asset_class_names is None:
    #         logging.error("Asset class names could not be retrieved from the database.")
    #         raise ValueError("Asset class names could not be retrieved from the database.")

    #     # Synonyms for equity subclasses
    #     common_stock_synonyms = ["common stock", "common", "stock", "common share","share",
    #                             "class a", "class b", "class c", "class d"]

    #     preferred_share_synonyms = ["preferred share", "pref shs", "preference share"]

    #     depository_share_synonyms = ["depository", "depository share", "depository receipt", "depository unit"] 

    #     # Synonyms for fund subclasses
    #     etf_synonyms = ["etf", "exchange traded fund"]

    #     # Synonyms for fixed income subclasses
    #     government_synonyms = ["government", "govt", "gov", "federal", "provincial", "province",
    #                            "united states", " usa ", "u.s.a.", " us ", "u.s.", "american", "treasury", "treasuries",
    #                            "canada", "canadian", "ontario", "quebec", "alberta", "british columbia", "manitoba", "saskatchewan",
    #                            "newfoundland", "labrador", "nova scotia", "new brunswick", "prince edward island", "northwest territories", "nunavut", "yukon"]
        
    #     municiple_synonyms = ["municipal", "city", "town", "county", "municipality"]
        
    #     corporate_synonyms = ["corporate", "company", "business", "enterprise", "corporation", "firm", "organization", "association"]
        
    #     bond_synonyms = ["bond", "debt"]

    #     note_synonyms = ["note", "paper", "bill"]

    #     # Predefined synonym dictionaries for each subclass
    #     subclass_synonyms = {
    #         "equity": {
    #             "common_stock": common_stock_synonyms,
    #             "preferred_share": preferred_share_synonyms,
    #             "depository_share": depository_share_synonyms
    #         },
    #         "fund": {
    #             "etf": etf_synonyms
    #         },
    #         "fixed_income": {
    #             "government_bond": government_synonyms + bond_synonyms,
    #             "municipal_bond": municiple_synonyms + bond_synonyms,
    #             "corporate_bond": corporate_synonyms + bond_synonyms,
    #             "government_note": government_synonyms + note_synonyms,
    #             "municipal_note": municiple_synonyms + note_synonyms,
    #             "corporate_note": corporate_synonyms + note_synonyms
    #         },

    #     }

    #     for asset_class_name in asset_class_names:
    #         asset_subclasses = self._database.query_executor.get_asset_subclass_names_by_asset_class_name(asset_class_name)

    #         if asset_subclasses is None:
    #             logging.error(f"Asset subclass names could not be retrieved for asset class '{asset_class_name}' from the database.")
    #             raise ValueError(f"Asset subclass names could not be retrieved for asset class '{asset_class_name}' from the database.")

    #         # Combine synonyms from class name, subclasses, and predefined subclass synonyms
    #         synonyms = [asset_class_name.lower().replace('_', ' ')] + [subclass.lower().replace('_', ' ') for subclass in asset_subclasses]
    #         for subclass in asset_subclasses:
    #             synonyms.extend(subclass_synonyms.get(asset_class_name, {}).get(subclass, []))

    #         self._asset_class_lookup[asset_class_name] = {
    #             "subclasses": asset_subclasses,
    #             "synonyms": synonyms
    #         }

    # def _match_asset_class_and_subclass(self, security_name):
    #     """
    #     This method matches a security name to an asset class and subclass.

    #     Args:
    #         security_name: The name of the security to match.

    #     Returns:
    #         The matched asset class and subclass, or (None, None) if no match is found.
    #     """
    #     if self._asset_class_lookup is None:
    #         logging.error("Asset class lookup dictionary not yet built. Please call _build_asset_class_and_subclass_lookup first.")
    #         raise ValueError("Asset class lookup dictionary not yet built. Please call _build_asset_class_and_subclass_lookup first.")
        
    #     for asset_class, info in self._asset_class_lookup.items():
    #         if any(word in info["synonyms"] for word in security_name.split()):
    #             for subclass in info["subclasses"]:
    #                 if any(word in subclass for word in security_name.split()):
    #                     return asset_class, subclass
    #             return asset_class, None
    #     return None, None


    # def _add_asset_class_and_subclass_names_to_dataframe(self) -> None:
    #     """
    #     This method attempts to match security descriptions in the exchange listings DataFrame to asset classes and subclasses using the internal lookup dictionary.

    #     Modifies the DataFrame in-place to add new columns "asset_class_name" and "asset_subclass_name".

    #     Raises:
    #         ValueError: If exchange listings have not been extracted or the asset class lookup dictionary is not built.
    #     """

    #     if self._df_exchange_listings_info is None:
    #         raise ValueError("Exchange listings must be extracted before adding asset class and subclass names.")

    #     if self._asset_class_lookup is None:
    #         raise ValueError("Asset class lookup dictionary not yet built. Please call _build_asset_class_and_subclass_lookup first.")

    #     # Add new columns for asset class and subclass names to the DataFrame
    #     self._df_exchange_listings_info["asset_class_name"] = None
    #     self._df_exchange_listings_info["asset_subclass_name"] = None

    #     for index, row in self._df_exchange_listings_info.iterrows():
    #         security_name_lower = row["security_name"].lower()
    #         matched_class, matched_subclass = self._match_asset_class_and_subclass(security_name_lower)

    #         # Update columns with matched class and subclass (or None if no match)
    #         self._df_exchange_listings_info.at[index, "asset_class_name"] = matched_class
    #         self._df_exchange_listings_info.at[index, "asset_subclass_name"] = matched_subclass

    #         # Handle cases where no match is found (consider logging or assigning defaults)
    #         if matched_class is None:
    #             logging.error(f"Could not determine asset class for '{row['symbol']}'.")
    #         if matched_subclass is None:
    #             logging.error(f"Could not determine asset subclass for '{row['symbol']}'.")
    
    def _retrieve_asset_class_names(self) -> None:
        # Get all asset class names from the database
        self._asset_class_names = self._database.query_executor.get_all_asset_class_names()
        logging.debug(f"asset_class_names:\n{self._asset_class_names}")
        if self._asset_class_names is None:
            raise ValueError("Asset class names could not be retrieved from the database.")
        
        # Remove all "_" from the asset class names
        self._asset_class_names = [asset_class_name.replace("_", " ") for asset_class_name in self._asset_class_names]

    def _add_asset_class_and_subclass_names_to_dataframe(self) -> None:
        self._retrieve_asset_class_names()

        if self._asset_class_names is None:
            logging.debug("Asset class names could not be retrieved from the database.")
            raise ValueError("Asset class names could not be retrieved from the database.")
        
        # Create a dictionary of asset class names and their corresponding asset subclass names
        asset_classes_and_subclasses = {}
        for asset_class_name in self._asset_class_names:
            asset_classes_and_subclasses[asset_class_name] = self._database.query_executor.get_asset_subclass_names_by_asset_class_name(asset_class_name)
        logging.debug(f"asset_classes_and_subclasses:\n{asset_classes_and_subclasses}")

        # Synonyms for Common Stock
        common_stock_synonyms = ["common stock", "common", "stock", "common share","share",
                                "class a", "class b", "class c", "class d"]
        
        # Synonyms for Preferred Shares
        preferred_shares_synonyms = ["preferred share", "pref shs", "preference share"]
        
        # Synonyms for Government notes and bonds
        government_synonyms = ["government", "govt", "gov", "federal", "provincial", "province",
                               "united states", " usa ", "u.s.a.", " us ", "u.s.", "american", "treasury", "treasuries",
                               "canada", "canadian", "ontario", "quebec", "alberta", "british columbia", "manitoba", "saskatchewan",
                               "newfoundland", "labrador", "nova scotia", "new brunswick", "prince edward island", "northwest territories", "nunavut", "yukon"]

        # Check if the exchange listings have been extracted
        if self._df_exchange_listings_info is None:
            raise ValueError("Exchange listings must be extracted before adding asset class and subclass names.")

        # Create a new column "asset_class_name" and "asset_subclass_name" to store determined class/subclass
        self._df_exchange_listings_info["asset_class_name"] = None
        self._df_exchange_listings_info["asset_subclass_name"] = None
        
        for index, row in self._df_exchange_listings_info.iterrows():
            logging.debug(f"row:\n{row}")
            security_name_lower = row["security_name"].lower()
            logging.debug(f"security_name_lower: {security_name_lower}")
            # security_name_upper = row["security_name"].upper()
            asset_class_name = None
            asset_subclass_name = None

            # Flag to indicate if a match is found
            found = False
            
            # Check if any of the other asset classes are present in the security name
            for asset_class, asset_subclasses in asset_classes_and_subclasses.items():
                logging.debug(f"asset_class: {asset_class}, asset_subclasses: {asset_subclasses}")

                # Check if the security is a depository share
                if "depository" in security_name_lower:
                    asset_class_name = "equity"
                    asset_subclass_name = "depository_share"
                    found = True
                    break

                # Check if the security is a preferred share
                for synonym in preferred_shares_synonyms:
                    if synonym in security_name_lower:
                        asset_class_name = "equity"
                        asset_subclass_name = "preferred_share"
                        found = True
                        break

                # Check if the security is a note
                if "note" in security_name_lower:
                    asset_class_name = "fixed_income"
                    for synonym in government_synonyms:
                        if synonym in security_name_lower:
                            asset_subclass_name = "government_note"
                            found = True
                            break
                    if "municipal" in security_name_lower:
                        asset_subclass_name = "municipal_note"
                        found = True
                        break
                    asset_subclass_name = "corporate_note"
                    found = True
                    break

                # Check if the security is a bond
                if "bond" in security_name_lower:
                    asset_class_name = "fixed_income"
                    for synonym in government_synonyms:
                        if synonym in security_name_lower:
                            asset_subclass_name = "government_bond"
                            found = True
                            break
                    if "municipal" in security_name_lower:
                        asset_subclass_name = "municipal_bond"
                        found = True
                        break
                    asset_subclass_name = "corporate_bond"
                    found = True
                    break

                # Check if the security is an etf
                if " etf" in security_name_lower:
                    asset_class_name = "fund"
                    asset_subclass_name = "etf"
                    found = True
                    break
                
                # Check if the security is a common stock
                if asset_subclasses == "common_stock":
                    for synonym in common_stock_synonyms:
                        if synonym in security_name_lower:
                            asset_class_name = asset_class
                            asset_subclass_name = asset_subclasses[0]
                            found = True
                            break

                # Check if any of the asset subclasses is present in the security name
                if asset_subclass_name is not None:
                    for subclass in asset_subclasses:
                        if subclass in security_name_lower:
                            logging.debug(f"subclass '{subclass}' is in the security name.")
                            # Set the asset subclass name to the first subclass found in the security name
                            asset_class_name = asset_class
                            asset_subclass_name = subclass
                            found = True
                            break
                        logging.debug(f"subclass '{subclass}' is not in the security name.")

                if found:
                    break

            logging.debug(f"asset_class_name: {asset_class_name}, asset_subclass_name: {asset_subclass_name}")
            
            # If no asset class or subclass, assign a default
            if asset_class_name is None:
                asset_class_name = "unknown"
                logging.error(f"Could not determine asset class for '{row['symbol']}', using unknown as placeholder.")
            if asset_subclass_name is None:
                asset_subclass_name = "unknown"
                logging.error(f"Could not determine asset subclass for '{row['symbol']}', using unknown as placeholder.")
            
            # Update the 'asset_subclass' column with the determined asset class and subclass names
            self._df_exchange_listings_info.at[index, "asset_class_name"] = asset_class_name
            self._df_exchange_listings_info.at[index, "asset_subclass_name"] = asset_subclass_name
            logging.debug(f"current df_exchange_listing entry:\n{self._df_exchange_listings_info.loc[index]}") # type: ignore

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
        if exchange_filter:
            self._filter_dataframe_by_exchange("Exchange", exchange_filter)
        
        # Check if the exchange listings were successfully retrieved
        if self._df_exchange_listings_info is None:
            raise ValueError(f"Exchange listings for '{exchange_in_url}' could not be retrieved from the website.")

    def _add_static_columns_to_nasdaq_trader_dataframe(self) -> None:
        # Add the exchange_id column
        self._add_dataframe_column("exchange_id", self._exchange_id)
        # Add the currency_id column
        usd_currency_id = self._database.query_executor.get_currency_id_by_currency_iso_code("USD")
        self._add_dataframe_column("exchange_currency_id", usd_currency_id)

    def _cleanup_nasdaq_trader_exchange_listings(self) -> None:
        # Check if the exchange listings have been extracted
        if self._df_exchange_listings_info is None:
            raise ValueError("Exchange listings must be extracted before cleaning up.")
        
        # Remove test listings
        self._df_exchange_listings_info = self._df_exchange_listings_info[~self._df_exchange_listings_info["Security Name"].str.contains("NASDAQ TEST")]
        self._df_exchange_listings_info = self._df_exchange_listings_info[~self._df_exchange_listings_info["Security Name"].str.contains("Nasdaq Symbology Test")]
        if self._exchange_in_url == "other":
            # Remove all rows where the Test Issue column is "Y"
            self._df_exchange_listings_info = self._df_exchange_listings_info[self._df_exchange_listings_info["Test Issue"] != "Y"]

        # Remove "File Creation Time" entry at the end of the DataFrame
        self._df_exchange_listings_info = self._df_exchange_listings_info[~self._df_exchange_listings_info[self._df_exchange_listings_info.columns[0]].str.contains("File Creation Time")]

        # Filter the desired columns
        desired_columns = ["exchange_currency_id", "exchange_id", self._df_exchange_listings_info.columns[0], "Security Name"]
        self._filter_dataframe_columns(desired_columns)
        # Rename all of the remaining columns to match the database
        self._rename_dataframe_columns(desired_columns, ["exchange_currency_id", "exchange_id", "symbol", "security_name"])

        # Remove rows with missing values
        self._df_exchange_listings_info.dropna()
        # Remove rows with duplicate values based on the symbol (first) column
        self._df_exchange_listings_info.drop_duplicates(subset=[self._df_exchange_listings_info.columns[0]])

    def initialize_nasdaq_trader_market_data(self, country_iso_code: str, exchange_name: str, exchange_acronym: str, exchange_in_url: str, exchange_filter: str | None) -> None:
        # Get the exchange_id from the database, or insert it if it doesn't exist
        self._get_exchange_id_or_insert(country_iso_code, exchange_name, exchange_acronym)
        # Get the exchange listings from the website
        self._extract_nasdaq_trader_exchange_listings(exchange_in_url, exchange_filter)
        # Add the remaining columns to the DataFrame
        self._add_static_columns_to_nasdaq_trader_dataframe()
        # Cleanup the exchange listings
        self._cleanup_nasdaq_trader_exchange_listings()
        # # Build the asset class and subclass lookup dictionary
        # if self._asset_class_lookup is None:
        #     self._build_asset_class_and_subclass_lookup()
        # Add the asset class and subclass name to the DataFrame
        self._add_asset_class_and_subclass_names_to_dataframe()
        print(f"{exchange_name} listings information successfully collected.")
        logging.info(f"{exchange_name} listings information successfully collected.")


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
        if self._df_exchange_listings_info is None:
            raise ValueError(f"Exchange listings for '{exchange_acronym}' could not be retrieved from the website.")
        logging.debug(f"df_exchange_listings after filtering:\n{self._df_exchange_listings_info}")

        # Filter by exchange
        self._filter_dataframe_by_exchange("mic", exchange_filter)

        # Add the exchange_id column
        self._df_exchange_listings_info["exchange_id"] = self._exchange_id
        # Convert the currency column to exchange_currency_id
        self._df_exchange_listings_info["exchange_currency_id"] = self._df_exchange_listings_info["currency"].apply(self._database.query_executor.get_currency_id_by_currency_iso_code)
        # Remove the currency column
        self._df_exchange_listings_info.drop(columns=["currency"], inplace=True)

    def _cleanup_cboe_canada_exchange_listings(self) -> None:
        # Check if the exchange listings have been extracted
        if self._df_exchange_listings_info is None:
            raise ValueError("Exchange listings must be extracted before cleaning up.")

        # Remove test listings
        self._df_exchange_listings_info = self._df_exchange_listings_info[~self._df_exchange_listings_info["cusip"].str.contains("TEST")]

        # Remove rows without a company name
        self._df_exchange_listings_info = self._df_exchange_listings_info[self._df_exchange_listings_info["company_name"] != ""]
        # Remove the test symbol entry
        self._df_exchange_listings_info = self._df_exchange_listings_info[self._df_exchange_listings_info["symbol"] != "ZYZ.C"]

        # Define the regular expression pattern to match " AT [...]" with any four-letter acronym
        pattern = r"\sAT\s[A-Z]{4}\b$"
        # Remove the pattern from the "company_name" column using regular expressions
        self._df_exchange_listings_info["company_name"] = self._df_exchange_listings_info["company_name"].str.replace(pattern, "", regex=True)

        # Replace all symbols with ".DB" at the end with ".TO"
        self._df_exchange_listings_info["symbol"] = self._df_exchange_listings_info["symbol"].str.replace(r"\.DB$", ".TO", regex=True)

        # Filter the desired columns
        desired_columns = ["asset_class", "exchange_currency_id", "exchange_id", "symbol", "company_name"]
        self._filter_dataframe_columns(desired_columns)
        # Rename all of the remaining columns to match the database
        self._rename_dataframe_columns(desired_columns, ["asset_class_name", "exchange_currency_id", "exchange_id", "symbol", "security_name"])

        # Remove rows with missing values
        self._df_exchange_listings_info.dropna()
        # Remove rows with duplicate values based on the symbol (first) column
        self._df_exchange_listings_info.drop_duplicates(subset=[self._df_exchange_listings_info.columns[0]])

    def initialize_cboe_canada_market_data(self, country_iso_code: str, exchange_name: str, exchange_acronym: str, exchange_filter: str) -> None:
        # Get the exchange_id from the database, or insert it if it doesn't exist
        self._get_exchange_id_or_insert(country_iso_code, exchange_name, exchange_acronym)
        # Get the exchange listings from the website
        self._extract_cboe_canada_exchange_listings(exchange_acronym, exchange_filter)
        # Cleanup the exchange listings
        self._cleanup_cboe_canada_exchange_listings()
        # # Build the asset class and subclass lookup dictionary
        # if self._asset_class_lookup is None:
        #     self._build_asset_class_and_subclass_lookup()
        # Add the asset class and subclass name to the DataFrame
        self._add_asset_class_and_subclass_names_to_dataframe()
        print(f"{exchange_name} listings information successfully collected.")
        logging.info(f"{exchange_name} listings information successfully collected.")

    def get_exchange_listings_info_dataframe(self) -> pd.DataFrame | None:
        return self._df_exchange_listings_info


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
