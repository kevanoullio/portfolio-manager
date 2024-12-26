# Purpose: Database Schema module for creating and initializing the database schema.

# Standard Libraries

# Third-party Libraries
import pandas as pd

# Local Modules
from database_management.query.query_executor import QueryExecutor
# from import_modules.web_data_importer import WebDataImporter

# Configure logging
import logging


# DatabaseSchema class for creating and initializing the database schema
class DatabaseSchema:
    def __init__(self, query_executor: QueryExecutor, db_schema_filename: str) -> None:
        self.__query_executor = query_executor
        self.__db_schema_filename = db_schema_filename

    def initialize_database(self) -> None:
        self.__query_executor.initialize_database_schema(self.__db_schema_filename)
        self.__insert_default_asset_classes_and_subclasses()
        self.__insert_default_country_codes()
        self.__insert_default_currency_codes()
        self.__insert_default_exchanges()

    def __insert_default_asset_classes_and_subclasses(self) -> None:
        # Create a dataframe with the default asset classes
        asset_classes_and_subclasses = {
            "equity": ["common_stock", "preferred_share", "warrant", "unit", "depository_share", "other", "unknown"],
            "fund": ["etf", "mutual_fund", "investment_fund", "hedge_fund", "private_equity", "other", "unknown"],
            "fixed_income": ["government_bond", "corporate_bond", "municipal_bond", "government_note", "corporate_note", "municipal_note", "perpetual", "money_market_fund", "certificate_of_deposit", "loan", "other", "unknown"],
            "cash_or_cash_equivalent": ["savings_account", "checking_account", "money_market_account", "cash", "cash_equivalent", "other", "unknown"],
            "real_estate": ["real_estate_investment_trust", "real_estate_fund", "real_estate_property", "other", "unknown"],
            "commodity": ["industrial_metal", "precious_metal", "energy", "agriculture", "livestock", "other", "unknown"],
            "derivative": ["stock_option", "futures_contract", "other", "unknown"],
            "cryptocurrency": ["platform", "defi", "exchange_token", "oracle", "dao", "metaverse", "privacy", "utility", "nft", "gaming", "payment", "stablecoin", "other", "unknown"],
            "unknown": ["unknown"]
        }

        # Convert the asset classes into a pandas dataframe
        asset_classes = list(asset_classes_and_subclasses.keys())
        df_asset_classes = pd.DataFrame(asset_classes, columns=["name"])

        # Convert the asset subclasses into a pandas dataframe
        data = []
        for i, (asset_class, subclasses) in enumerate(asset_classes_and_subclasses.items(), start=1):
            for subclass in subclasses:
                data.append({"asset_class_id": i, "name": subclass})
        df_asset_subclasses = pd.DataFrame(data)

        # Insert the default asset classes into the database
        self.__query_executor.dataframe_to_existing_sql_table(df_asset_classes, "asset_class")
        # Insert the default asset subclasses into the database
        self.__query_executor.dataframe_to_existing_sql_table(df_asset_subclasses, "asset_subclass")

    def __insert_default_country_codes(self) -> None:
        # Set the URL for the Wikipedia page containing the country codes
        url = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
        tables = pd.read_html(url)

        # Print all tables to debug
        for i, table in enumerate(tables):
            logging.debug(f"Table {i}:")
            logging.debug(table.head())

        # The first table contains the country codes
        table_index = 0
        country_codes = tables[table_index]

        # The dataframe has a multi-level column index, so we need to flatten it
        country_codes.columns = country_codes.columns.get_level_values(1)

        # Rename the columns we want to keep
        # Last accessed Dec 22, 2024, these were the formatted column names:
        # "name": ["Country name (using title case)"], "iso_code": ["Alpha-2 code"]
        country_codes = country_codes.rename(columns={"ISO 3166[1] name[5]": "name", "A-3 [5]": "iso_code"})
        # Rebuild a new dataframe with only the columns we want to keep
        country_codes = country_codes[["name", "iso_code"]]

        # Filter out the rows where the name is the same as the iso_code
        country_codes = country_codes[country_codes["name"] != country_codes["iso_code"]]

        # Remove all the citation references from the name column
        country_codes["name"] = country_codes["name"].str.replace(r"\[.*\]", "", regex=True)

        # Add an "unknown" country code to the dataframe
        new_row = pd.DataFrame({"name": ["Unknown"], "iso_code": ["UNK"]})
        country_codes = pd.concat([country_codes, new_row], ignore_index=True)

        # Order the dataframe by the name column
        country_codes = country_codes.sort_values(by=["name"])

        # Insert the default country codes into the database
        self.__query_executor.dataframe_to_existing_sql_table(country_codes, "country")

    def __insert_default_currency_codes(self) -> None:
        # Set the URL for the Wikipedia page containing the currency codes
        url = "https://en.wikipedia.org/wiki/List_of_circulating_currencies"
        tables = pd.read_html(url)

        # Print all tables to debug
        for i, table in enumerate(tables):
            logging.debug(f"Table {i}:")
            logging.debug(table.head())

        # The second table contains the country codes
        table_index = 1
        currency_codes = tables[table_index]

        # Rename the columns we want to keep
        # Last accessed Dec 22, 2024, these were the formatted column names:
        # "name": ["Currency[2][3]"], "iso_code": ["ISO code[3]"], "symbol": ["Symbol[D] or Abbrev.[4]"]
        currency_codes = currency_codes.rename(columns={"Currency[2][3]": "name", "ISO code[3]": "iso_code", "Symbol[D] or Abbrev.[4]": "symbol"})

        # Rebuild a new dataframe with only the columns we want to keep
        currency_codes = currency_codes[["name", "iso_code", "symbol"]]
        logging.debug(f"currency_codes: {currency_codes}")

        # Print out all rows that are "none" in all columns
        logging.debug(currency_codes[(currency_codes["name"] == "(none)")])
        logging.debug(currency_codes[(currency_codes["iso_code"] == "(none)")])
        logging.debug(currency_codes[(currency_codes["symbol"] == "(none)")])

        # Remove any rows with "(none)" in the name column
        mask = currency_codes["name"] != "(none)"
        currency_codes = currency_codes[mask]
        # Remove any rows that have "(none)" for their iso_code
        mask = currency_codes["iso_code"] != "(none)"
        currency_codes = currency_codes[mask]
        # Remove any rows with "(none)" in the symbol column
        mask = currency_codes["symbol"] != "(none)"
        currency_codes = currency_codes[mask]

        # Remove any rows with null values for all columns
        currency_codes = currency_codes.dropna(subset=["name", "iso_code", "symbol"])

        # Remove any duplicate entries
        currency_codes = currency_codes.drop_duplicates(subset=["iso_code"])

        # Remove any citation references "[...]" from the name column
        currency_codes["name"] = currency_codes["name"].str.replace(r"\[.*\]$", "", regex=True)
        # Remove any " or ..." from the symbol column
        currency_codes["symbol"] = currency_codes["symbol"].str.replace(r" or .*$", "", regex=True)

        # Order the dataframe by the name column
        currency_codes = currency_codes.sort_values(by=["name"])

        # Add an "unknown" currency code to the dataframe
        new_row = pd.DataFrame({"name": ["Unknown"], "iso_code": ["UNK"], "symbol": ["UNK"]})
        currency_codes = pd.concat([currency_codes, new_row], ignore_index=True)

        # Insert the default currency codes into the database
        self.__query_executor.dataframe_to_existing_sql_table(currency_codes, "currency")

    def __insert_default_exchanges(self) -> None:
        # TODO - replace this with function that imports exchange data from csv file???

        country_id = {}
        # Search for the country_id of the exchange in the database
        country_id["USA"] = self.__query_executor.get_country_id_by_country_iso_code("USA")
        country_id["JPN"] = self.__query_executor.get_country_id_by_country_iso_code("JPN")
        country_id["CHN"] = self.__query_executor.get_country_id_by_country_iso_code("CHN")
        country_id["HKG"] = self.__query_executor.get_country_id_by_country_iso_code("HKG")
        country_id["FRA"] = self.__query_executor.get_country_id_by_country_iso_code("FRA")
        country_id["GBR"] = self.__query_executor.get_country_id_by_country_iso_code("GBR")
        country_id["IND"] = self.__query_executor.get_country_id_by_country_iso_code("IND")
        country_id["CAN"] = self.__query_executor.get_country_id_by_country_iso_code("CAN")
        country_id["CHE"] = self.__query_executor.get_country_id_by_country_iso_code("CHE")
        country_id["AUS"] = self.__query_executor.get_country_id_by_country_iso_code("AUS")
        country_id["KOR"] = self.__query_executor.get_country_id_by_country_iso_code("KOR")
        country_id["DEU"] = self.__query_executor.get_country_id_by_country_iso_code("DEU")
        country_id["ESP"] = self.__query_executor.get_country_id_by_country_iso_code("ESP")
        country_id["ITA"] = self.__query_executor.get_country_id_by_country_iso_code("ITA")
        country_id["BRA"] = self.__query_executor.get_country_id_by_country_iso_code("BRA")
        country_id["TWN"] = self.__query_executor.get_country_id_by_country_iso_code("TWN")
        country_id["SGP"] = self.__query_executor.get_country_id_by_country_iso_code("SGP")
        country_id["ZAF"] = self.__query_executor.get_country_id_by_country_iso_code("ZAF")
        country_id["UNK"] = self.__query_executor.get_country_id_by_country_iso_code("UNK")

        # Put the country_id and exchange name and acronym into a dataframe
        exchanges = [
            {"country_id": country_id["USA"], "name": "NASDAQ Stock Exchange", "acronym": "NASDAQ"},
            {"country_id": country_id["USA"], "name": "New York Stock Exchange", "acronym": "NYSE"},
            {"country_id": country_id["USA"], "name": "New York Stock Exchange American", "acronym": "NYSE MKT"},
            {"country_id": country_id["USA"], "name": "New York Stock Exchange Arca", "acronym": "NYSE ARCA"},
            {"country_id": country_id["USA"], "name": "BATS Global Markets", "acronym": "BATS"},
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
            {"country_id": country_id["CAN"], "name": "Cboe Canada", "acronym": "Cboe CA"},
            {"country_id": country_id["CHE"], "name": "SIX Swiss Exchange", "acronym": "SIX"},
            {"country_id": country_id["AUS"], "name": "Australian Securities Exchange", "acronym": "ASX"},
            {"country_id": country_id["KOR"], "name": "Korea Exchange", "acronym": "KRX"},
            {"country_id": country_id["DEU"], "name": "Deutsche Börse", "acronym": "DB"},
            {"country_id": country_id["ESP"], "name": "Bolsa de Madrid", "acronym": "BME"},
            {"country_id": country_id["ITA"], "name": "Borsa Italiana", "acronym": "BIT"},
            {"country_id": country_id["BRA"], "name": "B3", "acronym": "B3"},
            {"country_id": country_id["TWN"], "name": "Taiwan Stock Exchange", "acronym": "TWSE"},
            {"country_id": country_id["SGP"], "name": "Singapore Exchange", "acronym": "SGX"},
            {"country_id": country_id["ZAF"], "name": "Johannesburg Stock Exchange", "acronym": "JSE"},
            {"country_id": country_id["UNK"], "name": "Unknown", "acronym": "UNK"}
        ]

        # Convert the exchanges data into a pandas dataframe
        df_exchanges = pd.DataFrame(exchanges)
        logging.debug(f"df_exchanges: {df_exchanges}")

        # Insert the default exchanges into the database
        self.__query_executor.dataframe_to_existing_sql_table(df_exchanges, "exchange")


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
