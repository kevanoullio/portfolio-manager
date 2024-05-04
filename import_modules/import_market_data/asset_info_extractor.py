# Purpose: Asset Info Extractor module for extracting asset information from various sources.

# Standard Libraries

# Third-party Libraries
import pandas as pd

# Local Modules
from database_management.database import Database
from database_management.schema.asset_dataclass import ExchangeListingsInfo, YFinanceAssetInfo, AssetInfoWithNames, AssetInfoWithIDs
# from import_modules.import_market_data.exchange_listings_extractor import ExchangeListingsExtractor
from import_modules.import_market_data.yfinance_data_extractor import YahooFinanceDataExtractor

# Configure logging
import logging


# AssetInfoExtractor class for extracting asset information from various sources
class AssetInfoExtractor:
    def __init__(self, database: Database) -> None:
        self.__database = database
        self.__exchange_acronym: str | None = None
        self.__exchange_listings_info: ExchangeListingsInfo | None = None
        self.__yfinance_data_extractor = YahooFinanceDataExtractor()
        self.__yfinance_asset_info: YFinanceAssetInfo | None = None
        self.__asset_info_with_names: AssetInfoWithNames | None = None
        self.__asset_info_with_ids: AssetInfoWithIDs | None = None
        # self.__df_asset_info: pd.DataFrame | None = None

    def __replace_delisted_asset_info(self, asset_symbol: str) -> dict[str, str] | None:
        replacement_asset_info = {}
        if asset_symbol == "SJR-B":
            replacement_asset_info["symbol"] = "RCI-B"
            replacement_asset_info["security_name"] = "SJR-B.TO bought out by RCI-B.TO"
            replacement_asset_info["business_summary"] = "Shaw Communications bought out by Rogers Communications as of March 15, 2021"
        else:
            replacement_asset_info = None
        return replacement_asset_info

    def __extract_asset_info_from_yfinance(self, exchange_acronym: str, asset_symbol: str) -> None:
        if self.__exchange_acronym is None:
            raise ValueError("Exchange Acronym must be extracted before Asset Info With Names.")
        
        # Extract the asset info with names
        yf_asset_info = self.__yfinance_data_extractor.extract_asset_info_from_yfinance(exchange_acronym, asset_symbol)
        if yf_asset_info is None:
            logging.warning(f"Could not retrieve asset information for {asset_symbol} from Yahoo Finance.")
            return None
        self.__yfinance_asset_info = yf_asset_info

    def __cleanup_asset_info_with_names(self) -> None:
        if self.__asset_info_with_names is None:
            logging.error(f"asset_info_with_names needs to be extracted before it can be cleaned up.")
            return None
        else:
            # Format the asset class name
            asset_class_name = self.__asset_info_with_names.asset_class_name
            available_asset_classes = self.__database.query_executor.get_all_asset_class_names()
            if available_asset_classes is None:
                logging.error(f"Could not find any asset classes in the database.")
                return None
            
            if asset_class_name is None:
                logging.error(f"Asset Class Name must be provided.")
                return None
            else:
                if asset_class_name.lower() in available_asset_classes:
                    asset_class_name = asset_class_name.lower()
                elif asset_class_name.upper() in available_asset_classes:
                    asset_class_name = asset_class_name.upper()
                else:
                    fund_asset_subclass_names = self.__database.query_executor.get_asset_subclass_names_by_asset_class_name("fund")
                    if fund_asset_subclass_names is None:
                        logging.error(f"Could not find any asset subclasses for asset class 'fund' in the database.")
                        return None
                    if asset_class_name.lower() in fund_asset_subclass_names or asset_class_name.upper() in fund_asset_subclass_names:
                        asset_class_name = "fund"

            # Get the available asset subclasses from the database
            available_asset_subclasses = self.__database.query_executor.get_all_asset_subclass_names()
            if available_asset_subclasses is None:
                logging.error(f"Could not find any asset subclasses in the database.")
                return None
            
            # Get exchange_id from the database
            if self.__exchange_acronym is None:
                logging.error(f"Exchange Acronym must be extracted before asset info can be cleaned up.")
                return None
            else:
                exchange_id = self.__database.query_executor.get_exchange_id_by_exchange_acronym(self.__exchange_acronym)
                if exchange_id is None:
                    logging.error(f"Could not find exchange_id for {self.__exchange_acronym} in the database.")
                    return None
            
            if self.__yfinance_asset_info is None:
                logging.error(f"yfinance_asset_info needs to be extracted before it can be cleaned up.")
                return None
            else:
                # Synonyms for Common Stock
                common_stock_synonyms = ["common stock", "common stocks", "common", "stock", "stocks", 
                                        "common share", "common shares", "share", "shares",
                                        "class a", "class b", "class c", "class d"]
                asset_subclass_name = None
                for name in available_asset_subclasses:
                    if name == common_stock_synonyms[0]:
                        for synonym in common_stock_synonyms:
                            if synonym in self.__yfinance_asset_info.company_name.lower():
                                asset_subclass_name = name
                                break
                    elif name in self.__yfinance_asset_info.company_name.lower():
                        asset_subclass_name = name.lower()
                        break
                    elif name in self.__yfinance_asset_info.company_name.upper():
                        asset_subclass_name = name.upper()
                        break
                if asset_subclass_name is None:
                    asset_subclass_name = asset_class_name
                    logging.error(f"Could not find asset subclass for {self.__yfinance_asset_info.company_name} on Yahoo Finance, using asset class name as placeholder.")
            
            # self.__asset_info_with_names.sector_name.title()
            # self.__asset_info_with_names.industry_name.title()

            # Format country_name to match the database entries
            if self.__asset_info_with_names.country_name.title() == "United States":
                self.__asset_info_with_names.country_name = "United States of America (the)"
            elif self.__asset_info_with_names.country_name.title() == "United Kingdom"\
                or self.__asset_info_with_names.country_name.title() == "Great Britain":
                self.__asset_info_with_names.country_name = "United Kingdom of Great Britain and Northern Ireland (the)"
            elif self.__asset_info_with_names.country_name.title() == "None":
                if self.__asset_info_with_names is None:
                    logging.error(f"_asset_info_with_names needs to be extracted before country_name can be cleaned up.")
                    return None
                if self.__asset_info_with_names.financial_currency_iso_code.upper() == "USD":
                    self.__asset_info_with_names.country_name = "United States of America (the)"
                elif self.__asset_info_with_names.financial_currency_iso_code.upper() == "CAD":
                    self.__asset_info_with_names.country_name = "Canada"
                elif self.__asset_info_with_names.financial_currency_iso_code.upper() == "GBP":
                    self.__asset_info_with_names.country_name = "United Kingdom of Great Britain and Northern Ireland (the)"

            # Use "N/A" if city is not applicable
            if self.__asset_info_with_names.city_name.title() == "None":
                self.__asset_info_with_names.city_name = "N/A"
            
            # Financial currency is the currency used for financial statements
            if self.__asset_info_with_names.financial_currency_iso_code.upper() == "NONE":
                currency_iso_code = self.__database.query_executor.get_currency_iso_code_by_currency_id(self.__asset_info_with_names.exchange_currency_id)
                if currency_iso_code is None:
                    logging.error(f"Could not find currency_iso_code for {self.__asset_info_with_names.exchange_currency_id} in the database.")
                    return None
                self.__asset_info_with_names.financial_currency_iso_code = currency_iso_code

    def __merge_exchange_listings_info_and_yfinance_asset_info(self) -> None:
        # Check if either asset info datatypes are None
        if self.__exchange_listings_info is None:
            raise ValueError("exchange_listings_info must be exctracted before merging.")
        if self.__yfinance_asset_info is None:
            raise ValueError("yfinance_asset_info must be exctracted before merging.")

        # Merge exchange_lisings_info and yfinance_asset_info
        self.__asset_info_with_names = AssetInfoWithNames(
            self.__exchange_listings_info.asset_class_name,
            self.__exchange_listings_info.asset_subclass_name,
            self.__yfinance_asset_info.sector_name,
            self.__yfinance_asset_info.industry_name,
            self.__yfinance_asset_info.country_name,
            self.__yfinance_asset_info.city_name,
            self.__yfinance_asset_info.financial_currency_iso_code,
            self.__exchange_listings_info.exchange_currency_id,
            self.__exchange_listings_info.exchange_id,
            self.__exchange_listings_info.symbol,
            self.__exchange_listings_info.security_name,
            self.__yfinance_asset_info.business_summary,
            self.__yfinance_asset_info.website,
            self.__yfinance_asset_info.logo_url
        )
        logging.debug(f"Filtered asset_info_with_names: {self.__asset_info_with_names}")

    def __get_asset_class_id(self, asset_class_name: str) -> int | None:
        asset_id = self.__database.query_executor.get_asset_class_id_by_asset_class_name(asset_class_name)
        if asset_id is None:
            asset_id = self.__database.query_executor.get_asset_class_id_by_asset_class_name("unknown")
        return asset_id

    def __get_asset_subclass_id(self, asset_subclass_name: str) -> int | None:
        subclass_id = self.__database.query_executor.get_asset_subclass_id_by_asset_subclass_name(asset_subclass_name)
        if subclass_id is None:
            subclass_id = self.__database.query_executor.get_asset_subclass_id_by_asset_subclass_name("unknown")
        return subclass_id
    
    def __get_sector_id_or_insert(self, asset_class_id: int, sector_name: str) -> int | None:
        # Check if sector_name is "None"
        if sector_name == "None":
            sector_name = "unknown"
            sector_id = self.__database.query_executor.get_sector_id_by_sector_name(sector_name)
            # Insert "unknown" sector if it doesn't exist
            if sector_id is None:
                self.__database.query_executor.insert_sector(asset_class_id, sector_name)
        # Get sector_id
        sector_id = self.__database.query_executor.get_sector_id_by_sector_name(sector_name)
        # If sector is still None, then it's a new sector, insert it
        if sector_id is None:
            self.__database.query_executor.insert_sector(asset_class_id, sector_name)
        sector_id = self.__database.query_executor.get_sector_id_by_sector_name(sector_name)
        return sector_id
    
    def __get_industry_id_or_insert(self, sector_id: int, industry_name: str) -> int | None:
        # Check if industry_name is "None"
        if industry_name == "None":
            industry_name = "unknown"
            industry_id = self.__database.query_executor.get_industry_id_by_industry_name(industry_name)
            # Insert "unknown" industry if it doesn't exist
            if industry_id is None:
                self.__database.query_executor.insert_industry(sector_id, industry_name)
        # Get industry_id
        industry_id = self.__database.query_executor.get_industry_id_by_industry_name(industry_name)
        # If industry is still None, then it's a new industry, insert it
        if industry_id is None:
            self.__database.query_executor.insert_industry(sector_id, industry_name)
        industry_id = self.__database.query_executor.get_industry_id_by_industry_name(industry_name)
        return industry_id
    
    def __get_country_id(self, country_name: str) -> int | None:
        if country_name == "None":
            country_name = "unknown"
        country_id = self.__database.query_executor.get_country_id_by_country_name(country_name)
        if country_id is None:
            logging.error(f"Could not find country_id for {country_name} in the database.")
            raise ValueError(f"Could not find country_id for {country_name} in the database.")
        return country_id
    
    def __get_city_id_or_insert(self, city_name: str, country_name: str) -> int | None:
        if city_name == "None":
            city_name = "unknown"
        city_id = self.__database.query_executor.get_city_id_by_city_name(city_name)
        if city_id is None:
            self.__database.query_executor.insert_city(city_name, country_name)
        city_id = self.__database.query_executor.get_city_id_by_city_name(city_name)
        return city_id
    
    def __get_currency_id(self, currency_iso_code: str) -> int | None:
        if currency_iso_code == "None":
            currency_iso_code = "unknown"
        currency_id = self.__database.query_executor.get_currency_id_by_currency_iso_code(currency_iso_code)
        if currency_id is None:
            logging.error(f"Could not find currency_id for {currency_iso_code} in the database.")
            raise ValueError(f"Could not find currency_id for {currency_iso_code} in the database.")
        return currency_id

    def __get_exchange_id(self, exchange_acronym: str) -> int | None:
        if exchange_acronym == "None":
            exchange_acronym = "unknown"
        exchange_id = self.__database.query_executor.get_exchange_id_by_exchange_acronym(exchange_acronym)
        if exchange_id is None:
            logging.error(f"Could not find exchange_id for {exchange_acronym} in the database.")
            raise ValueError(f"Could not find exchange_id for {exchange_acronym} in the database.")
        return exchange_id

    def __convert_asset_info_with_names_to_ids(self) -> None:
        # Check if the asset info with names has been extracted
        if self.__asset_info_with_names is None:
            logging.error("Asset Info with names must be extracted before converting to asset info with IDs.")
            raise ValueError("Asset Info with names must be extracted before converting to asset info with IDs.")
        
        # Asset Class
        asset_class_name = self.__asset_info_with_names.asset_class_name
        if asset_class_name is None:
            logging.error("Asset Class Name must be provided.")
            raise ValueError("Asset Class Name must be provided.")
        asset_class_id = self.__get_asset_class_id(asset_class_name)
        if asset_class_id is None:
            logging.error("Asset Class ID is None.")
            raise ValueError("Asset Class ID is None.")
        # Asset Subclass
        asset_subclass_name = self.__asset_info_with_names.asset_subclass_name
        if asset_subclass_name is None:
            logging.error("Asset Subclass Name must be provided.")
            raise ValueError("Asset Subclass Name must be provided.")
        asset_subclass_id = self.__get_asset_subclass_id(asset_subclass_name)
        if asset_subclass_id is None:
            logging.error("Asset Subclass ID is None.")
            raise ValueError("Asset Subclass ID is None.")
        # Sector
        sector_name = self.__asset_info_with_names.sector_name
        if sector_name is None:
            logging.error("Sector Name must be provided.")
            raise ValueError("Sector Name must be provided.")
        sector_id = self.__get_sector_id_or_insert(asset_class_id, sector_name)
        if sector_id is None:
            logging.error("Sector ID is None.")
            raise ValueError("Sector ID is None.")
        # Industry
        industry_name = self.__asset_info_with_names.industry_name
        if industry_name is None:
            logging.error("Industry Name must be provided.")
            raise ValueError("Industry Name must be provided.")
        industry_id = self.__get_industry_id_or_insert(sector_id, industry_name)
        if industry_id is None:
            logging.error("Industry ID is None.")
            raise ValueError("Industry ID is None.")
        # Country
        country_name = self.__asset_info_with_names.country_name
        if country_name is None:
            logging.error("Country Name must be provided.")
            raise ValueError("Country Name must be provided.")
        country_id = self.__get_country_id(country_name)
        if country_id is None:
            logging.error("Country ID is None.")
            raise ValueError("Country ID is None.")
        # City
        city_name = self.__asset_info_with_names.city_name
        if city_name is None:
            logging.error("City Name must be provided.")
            raise ValueError("City Name must be provided.")
        city_id = self.__get_city_id_or_insert(city_name, country_name)
        if city_id is None:
            logging.error("City ID is None.")
            raise ValueError("City ID is None.")
        # Financial Currency
        financial_currency_iso_code = self.__asset_info_with_names.financial_currency_iso_code
        if financial_currency_iso_code is None:
            logging.error("Financial Currency ISO Code must be provided.")
            raise ValueError("Financial Currency ISO Code must be provided.")
        financial_currency_id = self.__get_currency_id(financial_currency_iso_code)
        if financial_currency_id is None:
            logging.error("Financial Currency ID is None.")
            raise ValueError("Financial Currency ID is None.")
        # Exchange Currency
        exchange_currency_id = self.__asset_info_with_names.exchange_currency_id
        if exchange_currency_id is None:
            logging.error("Exchange Currency ID is None.")
            raise ValueError("Exchange Currency ID is None.")
        # Exchange Acronym
        exchange_id = self.__asset_info_with_names.exchange_id
        if exchange_id is None:
            logging.error("Exchange ID is None.")
            raise ValueError("Exchange ID is None.")
        # All remaining fields
        symbol = self.__asset_info_with_names.symbol
        company_name = self.__asset_info_with_names.security_name
        business_summary = self.__asset_info_with_names.business_summary
        website = self.__asset_info_with_names.website
        logo_url = self.__asset_info_with_names.logo_url
        
        self.__asset_info_with_ids = AssetInfoWithIDs(
            asset_class_id,
            asset_subclass_id,
            sector_id,
            industry_id,
            country_id,
            city_id,
            financial_currency_id,
            exchange_currency_id,
            exchange_id,
            symbol,
            company_name,
            business_summary,
            website,
            logo_url
        )

    def __insert_asset_info_to_database(self) -> None:
        # Check if the asset info has been extracted
        if self.__asset_info_with_ids is None:
            logging.error("Asset Info must be extracted and put into a data frame before inserting into the database.")
            raise ValueError("Asset Info must be extracted and put into a data frame before inserting into the database.")
        # Insert the asset info into the database
        self.__database.query_executor.insert_asset_info_with_ids(self.__asset_info_with_ids)

    def initialize_asset_info(self, df_exchange_listings_info: pd.DataFrame, exchange_acronym: str) -> None:
        logging.debug(f"df_exchange_listings_info: {df_exchange_listings_info}")
        self.__exchange_acronym = exchange_acronym
        for index, row in df_exchange_listings_info.iterrows():
            # Replace delisted asset info if applicable (only applies for known delisted assets)
            replacement_symbol = self.__replace_delisted_asset_info(row["symbol"])
            if replacement_symbol is not None:
                # Populate the exchange_listings_info datatype using the current row
                self.__exchange_listings_info = ExchangeListingsInfo(
                    row["asset_class_name"],
                    row["asset_subclass_name"],
                    row["exchange_currency_id"],
                    row["exchange_id"],
                    replacement_symbol["symbol"],
                    replacement_symbol["security_name"]
                )
                # Get asset info with names
                self.__extract_asset_info_from_yfinance(exchange_acronym, replacement_symbol["symbol"])
                if self.__asset_info_with_names is None:
                    raise ValueError("Asset Info with names is None.")
                self.__asset_info_with_names.symbol = row["symbol"]
                self.__asset_info_with_names.security_name = replacement_symbol["security_name"]
                self.__asset_info_with_names.business_summary = replacement_symbol["business_summary"]
            else:
                # Populate the exchange_listings_info datatype using the current row
                self.__exchange_listings_info = ExchangeListingsInfo(
                    row["asset_class_name"],
                    row["asset_subclass_name"],
                    row["exchange_currency_id"],
                    row["exchange_id"],
                    row["symbol"],
                    row["security_name"]
                )
                # Get asset info with names
                self.__extract_asset_info_from_yfinance(exchange_acronym, self.__exchange_listings_info.symbol)

            # Merge exchange listings info and yfinance asset info
            if self.__yfinance_asset_info is None:
                logging.warning(f"Could not retrieve asset information for {self.__exchange_listings_info.symbol} from Yahoo Finance.")
                continue
            else:
                self.__merge_exchange_listings_info_and_yfinance_asset_info()
                # Cleanup asset info with names
                self.__cleanup_asset_info_with_names()
                try:
                    # Convert asset info with names to asset info with IDs
                    self.__convert_asset_info_with_names_to_ids()
                except ValueError as err:
                    logging.error(f"ValueError occurred: {err}")
                else:
                    # Insert asset info into the database
                    self.__insert_asset_info_to_database()
        if self.__yfinance_asset_info is not None:
            print(f"Asset Info for {exchange_acronym} has been initialized.")
            logging.info(f"Asset Info for {exchange_acronym} has been initialized.")
        else:
            print(f"Asset Info for {exchange_acronym} could not be initialized.")
            logging.info(f"Asset Info for {exchange_acronym} could not be initialized.")


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
