# Purpose: Database Schema module for creating and initializing the database schema.

# Standard Libraries

# Third-party Libraries
import pandas as pd

# Local Modules
from database_management.query.query_executor import QueryExecutor

# Configure logging
import logging


# DatabaseSchema class for creating and initializing the database schema
class DatabaseSchema:
    def __init__(self, query_executor: QueryExecutor, db_schema_filename: str) -> None:
        self._query_executor = query_executor
        self._db_schema_filename = db_schema_filename
    
    def initialize_database(self) -> None:
        self._query_executor.initialize_database_schema(self._db_schema_filename)
        self._insert_default_asset_classes_and_subclasses()
        self._insert_default_country_codes()
        self._insert_default_currency_codes()
        self._insert_default_exchanges()

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
        df_asset_classes = pd.DataFrame(asset_classes, columns=["name"])

        # Convert the asset subclasses into a pandas dataframe
        data = []
        for i, (asset_class, subclasses) in enumerate(asset_classes_and_subclasses.items(), start=1):
            for subclass in subclasses:
                data.append({"id": i, "name": subclass})
        df_asset_subclasses = pd.DataFrame(data)

        # Insert the default asset classes into the database
        self._query_executor.dataframe_to_existing_sql_table(df_asset_classes, "asset_class")
        # Insert the default asset subclasses into the database
        self._query_executor.dataframe_to_existing_sql_table(df_asset_subclasses, "asset_subclass")
    
    def _insert_default_country_codes(self) -> None:
        # Get the country codes from Wikipedia and format them into a pandas dataframe
        url = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
        tables = pd.read_html(url)

        # The first table contains the country codes
        country_codes = tables[0]
        # The dataframe has a multi-level column index, so we need to flatten it
        country_codes.columns = country_codes.columns.get_level_values(1)

        # Rename the columns we want to keep
        country_codes = country_codes.rename(columns={"Country name[5]": "name", "Alpha-3 code[5]": "iso_code"})
        # Rebuild a new dataframe with only the columns we want to keep
        country_codes = country_codes[["name", "iso_code"]]

        # Filter out the rows where the name is the same as the iso_code
        country_codes = country_codes[country_codes["name"] != country_codes["iso_code"]]

        # Remove all the citation references from the name column
        country_codes["name"] = country_codes["name"].str.replace(r"\[.*\]", "", regex=True)

        # Insert the default country codes into the database
        self._query_executor.dataframe_to_existing_sql_table(country_codes, "country")

    def _insert_default_currency_codes(self) -> None:
        # Get the currency codes from Wikipedia and format them into a pandas dataframe
        url = "https://en.wikipedia.org/wiki/ISO_4217"
        # TODO - replace with (add symbol) https://en.wikipedia.org/wiki/List_of_circulating_currencies
        tables = pd.read_html(url)

        # The second table contains the country codes
        currency_codes = tables[1]
        # Rename the columns we want to keep
        currency_codes = currency_codes.rename(columns={"Currency": "name", "Code": "iso_code"})
        # Rebuild a new dataframe with only the columns we want to keep
        currency_codes = currency_codes[["name", "iso_code"]]

        # Filter out the rows that have "Unit " or "(funds code)" or (complementary currency)" in the currency column
        mask = ~currency_codes["name"].str.extract(r"(Unit |funds code|complementary currency)").notna().any(axis=1)

        # mask = ~currency_codes["name"].str.contains(r"Unit |(funds code)|(complementary currency)", regex=True)
        currency_codes = currency_codes[mask]
        # Filter out these specific currencies: ["XXX", "XTS", "XSU", "XDR"]
        mask = ~currency_codes["iso_code"].isin(["XXX", "XTS", "XSU", "XDR"])
        currency_codes = currency_codes[mask]

        # Remove all the citation references from the name column
        currency_codes["name"] = currency_codes["name"].str.replace(r"\[.*\]", "", regex=True)

        # Insert the default currency codes into the database
        self._query_executor.dataframe_to_existing_sql_table(currency_codes, "currency")

    def _get_country_id_by_iso_code(self, country_iso_code: str) -> int | None:
        # Search for the country_id based on the country's 3-letter iso_code
        country_id = self._query_executor.execute_query("SELECT id FROM country WHERE iso_code = ?", (country_iso_code,))
        # Check if the country_id was found
        return country_id[0][0] if country_id else None

    def _insert_default_exchanges(self) -> None:
        # TODO - replace this with function that imports exchange data from csv file

        country_id = {}
        # Search for the country_id of the exchange in the database
        country_id["USA"] = self._query_executor.get_country_id_by_country_iso_code("USA")
        country_id["JPN"] = self._query_executor.get_country_id_by_country_iso_code("JPN")
        country_id["CHN"] = self._query_executor.get_country_id_by_country_iso_code("CHN")
        country_id["HKG"] = self._query_executor.get_country_id_by_country_iso_code("HKG")
        country_id["FRA"] = self._query_executor.get_country_id_by_country_iso_code("FRA")
        country_id["GBR"] = self._query_executor.get_country_id_by_country_iso_code("GBR")
        country_id["IND"] = self._query_executor.get_country_id_by_country_iso_code("IND")
        country_id["CAN"] = self._query_executor.get_country_id_by_country_iso_code("CAN")
        country_id["CHE"] = self._query_executor.get_country_id_by_country_iso_code("CHE")
        country_id["AUS"] = self._query_executor.get_country_id_by_country_iso_code("AUS")
        country_id["KOR"] = self._query_executor.get_country_id_by_country_iso_code("KOR")
        country_id["DEU"] = self._query_executor.get_country_id_by_country_iso_code("DEU")
        country_id["ESP"] = self._query_executor.get_country_id_by_country_iso_code("ESP")
        country_id["ITA"] = self._query_executor.get_country_id_by_country_iso_code("ITA")
        country_id["BRA"] = self._query_executor.get_country_id_by_country_iso_code("BRA")
        country_id["TAI"] = self._query_executor.get_country_id_by_country_iso_code("TAI")
        country_id["SGP"] = self._query_executor.get_country_id_by_country_iso_code("SGP")
        country_id["ZAF"] = self._query_executor.get_country_id_by_country_iso_code("ZAF")

        # Put the country_id and exchange name and acronym into a dataframe
        exchanges = [
            {"country_id": country_id["USA"], "name": "NASDAQ Stock Exchange", "acronym": "NASDAQ"},
            {"country_id": country_id["USA"], "name": "New York Stock Exchange", "acronym": "NYSE"},
            {"country_id": country_id["USA"], "name": "American Stock Exchange", "acronym": "AMEX"},
            {"country_id": country_id["USA"], "name": "Chicago Mercantile Exchange", "acronym": "CME"},
            {"country_id": country_id["USA"], "name": "Chicago Board Options Exchange", "acronym": "CBOE"},
            {"country_id": country_id["JPN"], "name": "Tokyo Stock Exchange", "acronym": "TSE"},
            {"country_id": country_id["CHN"], "name": "Shanghai Stock Exchange", "acronym": "SSE"},
            {"country_id": country_id["HKG"], "name": "Hong Kong Stock Exchange", "acronym": "HKEX"},
            {"country_id": country_id["FRA"], "name": "Euronext Paris", "acronym": "ENX"},
            {"country_id": country_id["GBR"], "name": "London Stock Exchange", "acronym": "LSE"},
            {"country_id": country_id["CHN"], "name": "Shenzhen Stock Exchange", "acronym": "SZSE"},
            {"country_id": country_id["IND"], "name": "National Stock Exchange of India", "acronym": "NSE"},
            {"country_id": country_id["IND"], "name": "Bombay Stock Exchange", "acronym": "BSE"},
            {"country_id": country_id["CAN"], "name": "Toronto Stock Exchange", "acronym": "TSX"},
            {"country_id": country_id["CAN"], "name": "Toronto Venture Exchange", "acronym": "TSXV"},
            {"country_id": country_id["CAN"], "name": "Canadian Securities Exchange", "acronym": "CSE"},
            {"country_id": country_id["CAN"], "name": "Cboe Canada", "acronym": "Cboe Canada"},
            {"country_id": country_id["CHE"], "name": "SIX Swiss Exchange", "acronym": "SIX"},
            {"country_id": country_id["AUS"], "name": "Australian Securities Exchange", "acronym": "ASX"},
            {"country_id": country_id["KOR"], "name": "Korea Exchange", "acronym": "KRX"},
            {"country_id": country_id["DEU"], "name": "Deutsche Börse", "acronym": "DB"},
            {"country_id": country_id["ESP"], "name": "Bolsa de Madrid", "acronym": "BME"},
            {"country_id": country_id["ITA"], "name": "Borsa Italiana", "acronym": "BIT"},
            {"country_id": country_id["BRA"], "name": "B3", "acronym": "B3"},
            {"country_id": country_id["TAI"], "name": "Taiwan Stock Exchange", "acronym": "TWSE"},
            {"country_id": country_id["SGP"], "name": "Singapore Exchange", "acronym": "SGX"},
            {"country_id": country_id["ZAF"], "name": "Johannesburg Stock Exchange", "acronym": "JSE"}
        ]

        # Convert the exchanges data into a pandas dataframe
        df_exchanges = pd.DataFrame(exchanges)

        # Insert the default exchanges into the database
        self._query_executor.dataframe_to_existing_sql_table(df_exchanges, "exchange")


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


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
