# Purpose: Database Schema module for creating and initializing the database schema.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries
import pandas as pd

# Local Modules
from database_management.connection import DatabaseConnectionError
from import_modules.import_market_data import ImportMarketData

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from database_management.database import DatabaseConnection

# Configure logging
import logging


# DatabaseSchema class for creating and initializing the database schema
class DatabaseSchema:
    def __init__(self, db_connection: DatabaseConnection, db_schema_filename: str) -> None:
        self._db_connection = db_connection
        self._db_schema_filename = db_schema_filename
        self._import_market_data = ImportMarketData(self._db_connection)
    
    def initialize_database(self) -> None:
        # TODO Check if initialization was successful, make sure the database file is deleted if it wasn't
        try:
            with self._db_connection as connection:
                with connection.cursor() as cursor:
                    # Read the schema file
                    with open(self._db_schema_filename, 'r') as database_schema_file:
                        schema_sql_script = database_schema_file.read()
                        # Execute the schema SQL statements
                        cursor.executescript(schema_sql_script)
                        logging.info("Database schema initialized using the schema.sql file.")
                        # Insert default values into the database
                        self._insert_default_asset_classes_and_subclasses()
                        self._insert_default_country_codes()
                        self._insert_default_currency_codes()
                        logging.info("Default asset classes, subclasses, country codes, and currency codes inserted into the database.")
        except DatabaseConnectionError as e:
            logging.error(str(e))
        else:
            # Handle the case where no exception was raised, but the initialization was not successful
            pass

    def _insert_default_asset_classes_and_subclasses(self) -> None:
        # Create a dataframe with the default asset classes
        asset_classes_and_subclasses = {
            "equity": ["common stock", "preferred stock", "convertible preferred stock", "other"],
            "fund": ["ETF", "mutual fund", "other"],
            "fixed income": ["government bond", "corporate bond", "municipal bond", "money market fund", "certificate of deposit", "other"],
            "cash or cash equivalent": ["savings account", "checking account", "money market account", "cash", "cash equivalent", "other"],
            "real estate": ["real estate investment trust", "real estate fund", "real estate property", "other"],
            "commodity": ["industrial metal", "precious metal", "energy", "agriculture", "livestock", "other"],
            "derivative": ["stock option", "futures contract", "other"],
            "cryptocurrency": ["platform", "DeFi", "exchange token", "oracle", "DAO", "metaverse", "privacy", "utility", "NFT", "gaming", "payment", "stablecoin", "other"]
        }

        # Convert the asset classes into a pandas dataframe
        asset_classes = list(asset_classes_and_subclasses.keys())
        df_asset_classes = pd.DataFrame(asset_classes, columns=["[name]"])

        # Convert the asset subclasses into a pandas dataframe
        data = []
        for i, (asset_class, subclasses) in enumerate(asset_classes_and_subclasses.items(), start=1):
            for subclass in subclasses:
                data.append({"id": i, "[name]": subclass})
        df_asset_subclasses = pd.DataFrame(data)

        # Insert the default asset classes into the database
        self._import_market_data.pandas_to_existing_sql_table(df_asset_classes, "asset_class")
        # Insert the default asset subclasses into the database
        self._import_market_data.pandas_to_existing_sql_table(df_asset_subclasses, "asset_subclass")
    
    def _insert_default_country_codes(self) -> None:
        # Get the country codes from Wikipedia and format them into a pandas dataframe
        url = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
        tables = pd.read_html(url)

        # The first table contains the country codes
        country_codes = tables[0]
        # The dataframe has a multi-level column index, so we need to flatten it
        country_codes.columns = country_codes.columns.get_level_values(1)

        # Rename the columns we want to keep
        country_codes = country_codes.rename(columns={"Country name[5]": "[name]", "Alpha-3 code[5]": "iso_code"})
        # Rebuild a new dataframe with only the columns we want to keep
        country_codes = country_codes[["[name]", "iso_code"]]

        # Filter out the rows where the name is the same as the iso_code
        country_codes = country_codes[country_codes["[name]"] != country_codes["iso_code"]]

        # Remove all the citation references from the [name] column
        country_codes["[name]"] = country_codes["[name]"].str.replace(r"\[.*\]", "")

        # Insert the default country codes into the database
        self._import_market_data.pandas_to_existing_sql_table(country_codes, "country")

    def _insert_default_currency_codes(self) -> None:
        # Get the currency codes from Wikipedia and format them into a pandas dataframe
        url = "https://en.wikipedia.org/wiki/ISO_4217"
        tables = pd.read_html(url)

        # The second table contains the country codes
        currency_codes = tables[1]
        # Rename the columns we want to keep
        currency_codes = currency_codes.rename(columns={"Currency": "[name]", "Code": "iso_code"})
        # Rebuild a new dataframe with only the columns we want to keep
        currency_codes = currency_codes[["[name]", "iso_code"]]

        # Filter out the rows that have "Unit " or "(funds code)" or (complementary currency)" in the currency column
        currency_codes = currency_codes[~currency_codes["[name]"].str.contains("Unit |(funds code)|(complementary currency)")]
        # Filter out these specific currencies: ["XXX", "XTS", "XSU", "XDR"]
        currency_codes = currency_codes[~currency_codes["iso_code"].isin(["XXX", "XTS", "XSU", "XDR"])]

        # Remove all the citation references from the [name] column
        currency_codes["[name]"] = currency_codes["[name]"].str.replace(r"\[.*\]", "")

        # Insert the default currency codes into the database
        self._import_market_data.pandas_to_existing_sql_table(currency_codes, "currency")




# Function for printing all the tables from a url (used for debugging)
def _print_all_tables(url: str) -> None:
    tables = pd.read_html(url)
    for idx, table in enumerate(tables):
        print(f"Table {idx+1}:")
        print(table)
        print("\n")

def _print_one_table(url: str, table_index: int) -> None:
    tables = pd.read_html(url)
    print(f"Table {table_index}:")
    print(tables[table_index])
    print("\n")

url = "https://eoddata.com/stocklist/TSX/A.htm"
_print_all_tables(url)
_print_one_table(url, 5)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
