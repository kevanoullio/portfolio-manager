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
        self.__database = database
        self.__base_url: str | None = None
        self.__exchange_in_url: str | None = None
        self.__url_iterables: list[str] | None = None
        self.__url_ending: str | None = None
        self.__web_scraper = WebScraper(user_agent=True)
        self.__df_exchange_listings_info: pd.DataFrame | None = None
        self.__exchange_id: int | None = None
        self.__asset_class_subclass_names: dict[str, list[str]] | None = None
        self.__asset_class_lookup: dict | None = None

    def __format_url(self, iterable_index: int | None = None) -> str:
        if self.__url_iterables is None:
            return f"{self.__base_url}{self.__exchange_in_url}{self.__url_ending}"
        else:
            if iterable_index is None:
                raise ValueError("Iterable index must be specified when there are iterables.")
            return f"{self.__base_url}{self.__exchange_in_url}/{self.__url_iterables[iterable_index]}{self.__url_ending}"
 
    def __html_table_to_dataframe(self, table_index: int | None = None) -> None:
        if table_index is None:
            table_index = 0

        # If there are no iterables, read data from the URL and return the DataFrame from the specified table index
        if self.__url_iterables is None:
            html_text = self.__web_scraper.get_html_content_as_text(self.__format_url())
            if html_text is None:
                self.__df_exchange_listing = None
            else:
                self.__df_exchange_listing = pd.read_html(html_text)[table_index]
        else:
            # Iterate over the url iterables, read data from each URL, and store the DataFrames in a list
            dataframes_list = []
            for i, iterable in enumerate(self.__url_iterables):
                html_text = self.__web_scraper.get_html_content_as_text(self.__format_url(i))
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
            self.__df_exchange_listing = result_df
    
    def __csv_link_to_dataframe(self, first_column_in_header: str, sort_by_column: str | None = None) -> None:
        # Create a CSVFileManager object
        csv_file = CSVFileManager()
        # Set the first column in the header
        csv_file.set_first_column_in_header(first_column_in_header)
        if self.__base_url is None:
            raise ValueError("Base URL must be specified.")
        
        # Read the CSV file from the specified URL
        csv_file.read_csv_from_url(self.__format_url())

        if csv_file.get_data() is None:
            return None       

        if sort_by_column is not None:
            # Sort the data by the sort_by_column
            csv_file.sort_data_by_column(sort_by_column)

        # Convert the CSVFileManager object to a DataFrame
        self.__df_exchange_listings_info = csv_file.to_dataframe()
    
    def __txt_link_to_dataframe(self, first_column_in_header: str, delimiter: str) -> None: #, sort_by_column: str | None = None) -> None:
        # Create a TXTFileManager object
        txt_file = TXTFileManager()
        # Set the first column in the header
        txt_file.set_first_column_in_header(first_column_in_header)
        # Set the delimiter
        txt_file.set_delimiter(delimiter)
        if self.__base_url is None:
            raise ValueError("Base URL must be specified.")
        
        # Read the TXT file from the specified URL
        txt_file.read_txt_from_url(self.__format_url())

        if txt_file.get_data() is None:
            return None

        # Convert the TXTFileManager object to a DataFrame
        self.__df_exchange_listings_info = txt_file.to_dataframe()

    def __filter_dataframe_columns(self, desired_columns: list[str]) -> None:
        if self.__df_exchange_listings_info is None:
            raise ValueError("DataFrame must be initialized before filtering.")
        # Only keep the desired columns if specified
        try:
            self.__df_exchange_listings_info = self.__df_exchange_listings_info[desired_columns]
        except KeyError as err:
            print(f"KeyError: {err}")


    def __rename_dataframe_columns(self, columns_to_be_renamed: list[str], new_column_names: list[str]) -> None:
        if self.__df_exchange_listings_info is None:
            raise ValueError("DataFrame must be initialized before renaming.")
        # Rename the desired columns
        self.__df_exchange_listings_info.rename(columns=dict(zip(columns_to_be_renamed, new_column_names)), inplace=True)

    def __add_dataframe_column(self, column_name: str, column_data) -> None:
        if self.__df_exchange_listings_info is None:
            raise ValueError("DataFrame must be initialized before adding columns.")
        # Add the column to the DataFrame
        self.__df_exchange_listings_info[column_name] = column_data

    def __filter_dataframe_by_exchange(self, exchange_column_name: str, exchange: str) -> None:
        if self.__df_exchange_listings_info is None:
            raise ValueError("DataFrame must be initialized before filtering.")
        # Create a boolean mask based on the condition
        mask = self.__df_exchange_listings_info[exchange_column_name] == exchange
        # Filter the DataFrame using the boolean mask
        self.__df_exchange_listings_info = self.__df_exchange_listings_info[mask]

    def __get_exchange_id_or_insert(self, country_iso_code: str, exchange_name: str, exchange_acronym: str) -> int | None:
        # Get the exchange_id from the database
        exchange_id = self.__database.query_executor.get_exchange_id_by_exchange_acronym(exchange_acronym)
        # If the exchange doesn't exist in the database, insert it
        if exchange_id is None:
            # Get the country_id from the database
            country_id = self.__database.query_executor.get_country_id_by_country_iso_code(country_iso_code)
            if country_id is None:
                raise ValueError(f"Country ISO Code '{country_iso_code}' does not exist in the database.")
            self.__database.query_executor.insert_exchange(country_id, exchange_name, exchange_acronym)
            exchange_id = self.__database.query_executor.get_exchange_id_by_exchange_acronym(exchange_acronym)
            # Check if the exchange_id was successfully inserted
            if exchange_id is None:
                raise ValueError(f"Exchange acronym '{exchange_acronym}' does not exist in the database.")
        self.__exchange_id = exchange_id
    
    def __fetch_asset_classes_and_subclasses(self) -> None:
        # Initialize the asset class lookup dictionary
        self.__asset_class_lookup = {}

        # Get all asset class names from the database
        asset_class_names = self.__database.query_executor.get_all_asset_class_names()

        if asset_class_names is None:
            logging.error("Asset class names could not be retrieved from the database.")
            raise ValueError("Asset class names could not be retrieved from the database.")

        # # Remove all "_" from the asset class names
        # asset_class_names = [asset_class_name.replace("_", " ") for asset_class_name in asset_class_names]

        # Fill the asset class lookup dictionary with asset class names as keys and subclasses as a list of values
        for asset_class in asset_class_names:
            # Add the asset class name to the dictionary
            self.__asset_class_lookup[asset_class] = []

            # Get all asset subclass names for the asset class
            asset_subclass_names = self.__database.query_executor.get_asset_subclass_names_by_asset_class_name(asset_class)

            if asset_subclass_names is None:
                logging.error(f"Asset subclass names could not be retrieved for asset class '{asset_class}' from the database.")
                raise ValueError(f"Asset subclass names could not be retrieved for asset class '{asset_class}' from the database.")
            
            # # Remove all "_" from the asset subclass names
            # asset_subclass_names = [asset_subclass_name.replace("_", " ") for asset_subclass_name in asset_subclass_names]

            # Add the asset subclass names to the dictionary
            self.__asset_class_lookup[asset_class] = asset_subclass_names


    def __build_asset_class_and_subclass_lookup(self) -> None:
        """
        This method builds a dictionary to store asset class names, subclasses, and their synonyms.

        Updates the internal `_asset_class_lookup` attribute.

        `_asset_class_lookup` dict structure:
            A dictionary where the key is the asset class name and the value is another dictionary.
            The inner dictionary has two keys:
                - 'subclasses': a list of asset subclasses for the class
                - 'synonyms': a list of synonyms for both the class and subclasses (combined)

        Raises:
            ValueError: If asset class names or subclass names cannot be retrieved from the database.
        """
        # Predefined synonym dictionaries for each subclass
        subclass_synonyms = {
            "equity": {
                "common_stock": ["common stock", "common", "stock", "common share","share",
                                "class a", "class b", "class c", "class d"],
                "preferred_share": ["preferred share", "pref shs", "preference share"],
                "depository_share": ["depository", "depository share", "depository receipt", "depository unit"] 
            },
            "fund": {
                "etf": ["etf", "exchange traded fund"]
            },
            "fixed_income": {
                "bond": ["bond", "debt"],
                "note": ["note", "paper", "bill"],
                "government": ["government", "govt", "gov", "federal", "provincial", "province",
                               "united states", " usa ", "u.s.a.", " us ", "u.s.", "american", "treasury", "treasuries",
                               "canada", "canadian", "ontario", "quebec", "alberta", "british columbia", "manitoba", "saskatchewan",
                               "newfoundland", "labrador", "nova scotia", "new brunswick", "prince edward island", "northwest territories", "nunavut", "yukon"],
                "municipal": ["municipal", "city", "town", "county", "municipality"],
                "corporate": ["corporate", "company", "business", "enterprise", "corporation", "firm", "organization", "association", "holding"]
            },
        }

        if self.__asset_class_subclass_names is None:
            logging.error("Asset class and subclass names could not be retrieved from the database.")
            raise ValueError("Asset class and subclass names could not be retrieved from the database.")
        
        if self.__asset_class_lookup is None:
            logging.error("Asset class lookup dictionary not yet built. Please call _fetch_asset_classes_and_subclasses first.")
            raise ValueError("Asset class lookup dictionary not yet built. Please call _fetch_asset_classes_and_subclasses first.")

        for asset_class, asset_subclass in self.__asset_class_subclass_names:
            # Combine synonyms from class name, subclasses, and predefined subclass synonyms
            synonyms = [asset_class.lower().replace('_', ' ')] + [subclass.lower().replace('_', ' ') for subclass in asset_subclass]
            for subclass in asset_subclass:
                synonyms.extend(subclass_synonyms.get(asset_class, {}).get(subclass, []))

            self.__asset_class_lookup[asset_class] = {
                "subclasses": asset_subclass,
                "synonyms": synonyms
            }

    def __match_asset_class_and_subclass(self, security_name):
        """
        This method matches a security name to an asset class and subclass.

        Args:
            security_name: The name of the security to match.

        Returns:
            The matched asset class and subclass, or (None, None) if no match is found.
        """
        if self.__asset_class_lookup is None:
            logging.error("Asset class lookup dictionary not yet built. Please call _build_asset_class_and_subclass_lookup first.")
            raise ValueError("Asset class lookup dictionary not yet built. Please call _build_asset_class_and_subclass_lookup first.")
        
        for asset_class, info in self.__asset_class_lookup.items():
            if any(word in info["synonyms"] for word in security_name.split()):
                for subclass in info["subclasses"]:
                    if any(word in subclass for word in security_name.split()):
                        return asset_class, subclass
                return asset_class, None
        return None, None

    def __add_asset_class_and_subclass_names_to_dataframe(self) -> None:
        """
        This method attempts to match security descriptions in the exchange listings DataFrame to asset classes and subclasses using the internal lookup dictionary.

        Modifies the DataFrame in-place to add new columns "asset_class_name" and "asset_subclass_name".

        Raises:
            ValueError: If exchange listings have not been extracted or the asset class lookup dictionary is not built.
        """

        if self.__df_exchange_listings_info is None:
            raise ValueError("Exchange listings must be extracted before adding asset class and subclass names.")

        if self.__asset_class_lookup is None:
            raise ValueError("Asset class lookup dictionary not yet built. Please call _build_asset_class_and_subclass_lookup first.")

        # Add new columns for asset class and subclass names to the DataFrame
        self.__df_exchange_listings_info["asset_class_name"] = None
        self.__df_exchange_listings_info["asset_subclass_name"] = None

        for index, row in self.__df_exchange_listings_info.iterrows():
            security_name_lower = row["security_name"].lower()
            matched_class, matched_subclass = self.__match_asset_class_and_subclass(security_name_lower)

            # Update columns with matched class and subclass (or None if no match)
            self.__df_exchange_listings_info.at[index, "asset_class_name"] = matched_class
            self.__df_exchange_listings_info.at[index, "asset_subclass_name"] = matched_subclass

            # Handle cases where no match is found (consider logging or assigning defaults)
            if matched_class is None:
                logging.error(f"Could not determine asset class for '{row['symbol']}'.")
            if matched_subclass is None:
                logging.error(f"Could not determine asset subclass for '{row['symbol']}'.")

    # def __add_asset_class_and_subclass_names_to_dataframe(self) -> None:
    #     self.__retrieve_asset_class_names()

    #     if self.__asset_class_names is None:
    #         logging.debug("Asset class names could not be retrieved from the database.")
    #         raise ValueError("Asset class names could not be retrieved from the database.")
        
    #     # Create a dictionary of asset class names and their corresponding asset subclass names
    #     asset_classes_and_subclasses = {}
    #     for asset_class_name in self.__asset_class_names:
    #         asset_classes_and_subclasses[asset_class_name] = self.__database.query_executor.get_asset_subclass_names_by_asset_class_name(asset_class_name)
    #     logging.debug(f"asset_classes_and_subclasses:\n{asset_classes_and_subclasses}")

    #     # Synonyms for Common Stock
    #     common_stock_synonyms = ["common stock", "common", "stock", "common share","share",
    #                             "class a", "class b", "class c", "class d"]
        
    #     # Synonyms for Preferred Shares
    #     preferred_shares_synonyms = ["preferred share", "pref shs", "preference share"]
        
    #     # Synonyms for Government notes and bonds
    #     government_synonyms = ["government", "govt", "gov", "federal", "provincial", "province",
    #                            "united states", " usa ", "u.s.a.", " us ", "u.s.", "american", "treasury", "treasuries",
    #                            "canada", "canadian", "ontario", "quebec", "alberta", "british columbia", "manitoba", "saskatchewan",
    #                            "newfoundland", "labrador", "nova scotia", "new brunswick", "prince edward island", "northwest territories", "nunavut", "yukon"]

    #     # Check if the exchange listings have been extracted
    #     if self.__df_exchange_listings_info is None:
    #         raise ValueError("Exchange listings must be extracted before adding asset class and subclass names.")

    #     # Create a new column "asset_class_name" and "asset_subclass_name" to store determined class/subclass
    #     self.__df_exchange_listings_info["asset_class_name"] = None
    #     self.__df_exchange_listings_info["asset_subclass_name"] = None
        
    #     for index, row in self.__df_exchange_listings_info.iterrows():
    #         logging.debug(f"row:\n{row}")
    #         security_name_lower = row["security_name"].lower()
    #         logging.debug(f"security_name_lower: {security_name_lower}")
    #         # security_name_upper = row["security_name"].upper()
    #         asset_class_name = None
    #         asset_subclass_name = None

    #         # Flag to indicate if a match is found
    #         found = False
            
    #         # Check if any of the other asset classes are present in the security name
    #         for asset_class, asset_subclasses in asset_classes_and_subclasses.items():
    #             logging.debug(f"asset_class: {asset_class}, asset_subclasses: {asset_subclasses}")

    #             # Check if the security is an etf
    #             if " etf" in security_name_lower:
    #                 asset_class_name = "fund"
    #                 asset_subclass_name = "etf"
    #                 found = True
    #                 break

    #             # Check if the security is a depository share
    #             if "depository" in security_name_lower:
    #                 asset_class_name = "equity"
    #                 asset_subclass_name = "depository_share"
    #                 found = True
    #                 break

    #             # Check if the security is a preferred share
    #             for synonym in preferred_shares_synonyms:
    #                 if synonym in security_name_lower:
    #                     asset_class_name = "equity"
    #                     asset_subclass_name = "preferred_share"
    #                     found = True
    #                     break

    #             # Check if the security is a note
    #             if "note" in security_name_lower:
    #                 asset_class_name = "fixed_income"
    #                 for synonym in government_synonyms:
    #                     if synonym in security_name_lower:
    #                         asset_subclass_name = "government_note"
    #                         found = True
    #                         break
    #                 if "municipal" in security_name_lower:
    #                     asset_subclass_name = "municipal_note"
    #                     found = True
    #                     break
    #                 asset_subclass_name = "corporate_note"
    #                 found = True
    #                 break

    #             # Check if the security is a bond
    #             if "bond" in security_name_lower:
    #                 asset_class_name = "fixed_income"
    #                 for synonym in government_synonyms:
    #                     if synonym in security_name_lower:
    #                         asset_subclass_name = "government_bond"
    #                         found = True
    #                         break
    #                 if "municipal" in security_name_lower:
    #                     asset_subclass_name = "municipal_bond"
    #                     found = True
    #                     break
    #                 asset_subclass_name = "corporate_bond"
    #                 found = True
    #                 break
                
    #             # Check if the security is a common stock
    #             if asset_subclasses == "common_stock":
    #                 for synonym in common_stock_synonyms:
    #                     if synonym in security_name_lower:
    #                         asset_class_name = asset_class
    #                         asset_subclass_name = asset_subclasses[0]
    #                         found = True
    #                         break

    #             # Check if any of the asset subclasses is present in the security name
    #             if asset_subclass_name is not None:
    #                 for subclass in asset_subclasses:
    #                     if subclass in security_name_lower:
    #                         logging.debug(f"subclass '{subclass}' is in the security name.")
    #                         # Set the asset subclass name to the first subclass found in the security name
    #                         asset_class_name = asset_class
    #                         asset_subclass_name = subclass
    #                         found = True
    #                         break
    #                     logging.debug(f"subclass '{subclass}' is not in the security name.")

    #             if found:
    #                 break

    #         logging.debug(f"asset_class_name: {asset_class_name}, asset_subclass_name: {asset_subclass_name}")
            
    #         # If no asset class or subclass, assign a default
    #         if asset_class_name is None:
    #             asset_class_name = "unknown"
    #             logging.error(f"Could not determine asset class for '{row['symbol']}', using unknown as placeholder.")
    #         if asset_subclass_name is None:
    #             asset_subclass_name = "unknown"
    #             logging.error(f"Could not determine asset subclass for '{row['symbol']}', using unknown as placeholder.")
            
    #         # Update the 'asset_subclass' column with the determined asset class and subclass names
    #         self.__df_exchange_listings_info.at[index, "asset_class_name"] = asset_class_name
    #         self.__df_exchange_listings_info.at[index, "asset_subclass_name"] = asset_subclass_name
    #         logging.debug(f"current df_exchange_listing entry:\n{self.__df_exchange_listings_info.loc[index]}") # type: ignore

    def __extract_nasdaq_trader_exchange_listings(self, exchange_in_url: str, exchange_filter: str | None = None) -> None:
        """
        Extracts the exchange listings from the nasdaqtrader.com website here:
        http://ftp.nasdaqtrader.com/Trader.aspx?id=symbollookup

        NASDAQ listed companies: http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt
        Other listed companies: http://ftp.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt
        """
        # Assign nasdaqtrader.com specific variables
        self.__base_url = "http://ftp.nasdaqtrader.com/dynamic/SymDir/"
        self.__exchange_in_url = exchange_in_url
        self.__url_ending = "listed.txt"

        # Extract the exchange listings from the website
        if exchange_in_url == "nasdaq":
            first_column_in_header = "Symbol"
        elif exchange_in_url == "other":
            first_column_in_header = "ACT Symbol"
        else:
            raise ValueError(f"Exchange '{exchange_in_url}' is not supported.")

        # Extract the exchange listings from the website to a DataFrame
        self.__txt_link_to_dataframe(first_column_in_header, "|")
        # If other listings, filter by exchange
        if exchange_filter:
            self.__filter_dataframe_by_exchange("Exchange", exchange_filter)
        
        # Check if the exchange listings were successfully retrieved
        if self.__df_exchange_listings_info is None:
            raise ValueError(f"Exchange listings for '{exchange_in_url}' could not be retrieved from the website.")

    def __add_static_columns_to_nasdaq_trader_dataframe(self) -> None:
        # Add the exchange_id column
        self.__add_dataframe_column("exchange_id", self.__exchange_id)
        # Add the currency_id column
        usd_currency_id = self.__database.query_executor.get_currency_id_by_currency_iso_code("USD")
        self.__add_dataframe_column("exchange_currency_id", usd_currency_id)

    def __cleanup_nasdaq_trader_exchange_listings(self) -> None:
        # Check if the exchange listings have been extracted
        if self.__df_exchange_listings_info is None:
            raise ValueError("Exchange listings must be extracted before cleaning up.")
        
        # Remove test listings
        self.__df_exchange_listings_info = self.__df_exchange_listings_info[~self.__df_exchange_listings_info["Security Name"].str.contains("NASDAQ TEST")]
        self.__df_exchange_listings_info = self.__df_exchange_listings_info[~self.__df_exchange_listings_info["Security Name"].str.contains("Nasdaq Symbology Test")]
        if self.__exchange_in_url == "other":
            # Remove all rows where the Test Issue column is "Y"
            self.__df_exchange_listings_info = self.__df_exchange_listings_info[self.__df_exchange_listings_info["Test Issue"] != "Y"]

        # Remove "File Creation Time" entry at the end of the DataFrame
        self.__df_exchange_listings_info = self.__df_exchange_listings_info[~self.__df_exchange_listings_info[self.__df_exchange_listings_info.columns[0]].str.contains("File Creation Time")]

        # Filter the desired columns
        desired_columns = ["exchange_currency_id", "exchange_id", self.__df_exchange_listings_info.columns[0], "Security Name"]
        self.__filter_dataframe_columns(desired_columns)
        # Rename all of the remaining columns to match the database
        self.__rename_dataframe_columns(desired_columns, ["exchange_currency_id", "exchange_id", "symbol", "security_name"])

        # Remove rows with missing values
        self.__df_exchange_listings_info.dropna()
        # Remove rows with duplicate values based on the symbol (first) column
        self.__df_exchange_listings_info.drop_duplicates(subset=[self.__df_exchange_listings_info.columns[0]])

    def initialize_nasdaq_trader_market_data(self, country_iso_code: str, exchange_name: str, exchange_acronym: str, exchange_in_url: str, exchange_filter: str | None) -> None:
        # Get the exchange_id from the database, or insert it if it doesn't exist
        self.__get_exchange_id_or_insert(country_iso_code, exchange_name, exchange_acronym)
        # Get the exchange listings from the website
        self.__extract_nasdaq_trader_exchange_listings(exchange_in_url, exchange_filter)
        # Add the remaining columns to the DataFrame
        self.__add_static_columns_to_nasdaq_trader_dataframe()
        # Cleanup the exchange listings
        self.__cleanup_nasdaq_trader_exchange_listings()
        # Fetch asset classes and subclasses from the database
        if self.__asset_class_subclass_names is None:
            self.__fetch_asset_classes_and_subclasses()
        # Build the asset class and subclass lookup dictionary
        if self.__asset_class_lookup is None:
            self.__build_asset_class_and_subclass_lookup()
        # Add the asset class and subclass name to the DataFrame
        self.__add_asset_class_and_subclass_names_to_dataframe()
        print(f"{exchange_name} listings information successfully collected.")
        logging.info(f"{exchange_name} listings information successfully collected.")

    def __extract_cboe_canada_exchange_listings(self, exchange_acronym: str, exchange_filter: str) -> None:
        """
        Extracts the exchange listings from the Cboe Canada website here:
        https://cdn.cboe.com/ca/equities/mnow/symbol_listings.csv
        """
        # Assign cdn.cboe.com specific variables
        self.__base_url = "https://cdn.cboe.com/ca/equities/mnow/"
        self.__exchange_in_url = "symbol_listings"
        self.__url_ending = ".csv"

        # Extract the exchange listings from the website
        self.__csv_link_to_dataframe(first_column_in_header="company_name", sort_by_column="symbol")
        if self.__df_exchange_listings_info is None:
            raise ValueError(f"Exchange listings for '{exchange_acronym}' could not be retrieved from the website.")
        logging.debug(f"df_exchange_listings after filtering:\n{self.__df_exchange_listings_info}")

        # Filter by exchange
        self.__filter_dataframe_by_exchange("mic", exchange_filter)

        # Add the exchange_id column
        self.__df_exchange_listings_info["exchange_id"] = self.__exchange_id
        # Convert the currency column to exchange_currency_id
        self.__df_exchange_listings_info["exchange_currency_id"] = self.__df_exchange_listings_info["currency"].apply(self.__database.query_executor.get_currency_id_by_currency_iso_code)
        # Remove the currency column
        self.__df_exchange_listings_info.drop(columns=["currency"], inplace=True)

    def __cleanup_cboe_canada_exchange_listings(self) -> None:
        # Check if the exchange listings have been extracted
        if self.__df_exchange_listings_info is None:
            raise ValueError("Exchange listings must be extracted before cleaning up.")

        # Remove test listings
        self.__df_exchange_listings_info = self.__df_exchange_listings_info[~self.__df_exchange_listings_info["cusip"].str.contains("TEST")]

        # Remove rows without a company name
        self.__df_exchange_listings_info = self.__df_exchange_listings_info[self.__df_exchange_listings_info["company_name"] != ""]
        # Remove the test symbol entry
        self.__df_exchange_listings_info = self.__df_exchange_listings_info[self.__df_exchange_listings_info["symbol"] != "ZYZ.C"]

        # Define the regular expression pattern to match " AT [...]" with any four-letter acronym
        pattern = r"\sAT\s[A-Z]{4}\b$"
        # Remove the pattern from the "company_name" column using regular expressions
        self.__df_exchange_listings_info["company_name"] = self.__df_exchange_listings_info["company_name"].str.replace(pattern, "", regex=True)

        # Replace all symbols with ".DB" at the end with ".TO"
        self.__df_exchange_listings_info["symbol"] = self.__df_exchange_listings_info["symbol"].str.replace(r"\.DB$", ".TO", regex=True)

        # Filter the desired columns
        desired_columns = ["asset_class", "exchange_currency_id", "exchange_id", "symbol", "company_name"]
        self.__filter_dataframe_columns(desired_columns)
        # Rename all of the remaining columns to match the database
        self.__rename_dataframe_columns(desired_columns, ["asset_class_name", "exchange_currency_id", "exchange_id", "symbol", "security_name"])

        # Remove rows with missing values
        self.__df_exchange_listings_info.dropna()
        # Remove rows with duplicate values based on the symbol (first) column
        self.__df_exchange_listings_info.drop_duplicates(subset=[self.__df_exchange_listings_info.columns[0]])

    def initialize_cboe_canada_market_data(self, country_iso_code: str, exchange_name: str, exchange_acronym: str, exchange_filter: str) -> None:
        # Get the exchange_id from the database, or insert it if it doesn't exist
        self.__get_exchange_id_or_insert(country_iso_code, exchange_name, exchange_acronym)
        # Get the exchange listings from the website
        self.__extract_cboe_canada_exchange_listings(exchange_acronym, exchange_filter)
        # Cleanup the exchange listings
        self.__cleanup_cboe_canada_exchange_listings()
        # Fetch asset classes and subclasses from the database
        if self.__asset_class_subclass_names is None:
            self.__fetch_asset_classes_and_subclasses()
        # Build the asset class and subclass lookup dictionary
        if self.__asset_class_lookup is None:
            self.__build_asset_class_and_subclass_lookup()
        # Add the asset class and subclass name to the DataFrame
        self.__add_asset_class_and_subclass_names_to_dataframe()
        print(f"{exchange_name} listings information successfully collected.")
        logging.info(f"{exchange_name} listings information successfully collected.")

    def get_exchange_listings_info_dataframe(self) -> pd.DataFrame | None:
        return self.__df_exchange_listings_info


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
