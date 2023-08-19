# Purpose: Asset Info Extractor module for extracting asset information from various sources.

# Standard Libraries

# Third-party Libraries
import pandas as pd

# Local Modules
from database_management.database import Database
from database_management.schema.asset_dataclass import ExchangeListingsInfo, YFinanceAssetInfo, AssetInfoWithNames, AssetInfoWithIDs
from import_modules.import_market_data.exchange_listings_extractor import ExchangeListingsExtractor
from import_modules.import_market_data.yfinance_data_extractor import YahooFinanceDataExtractor

# Configure logging
import logging


# AssetInfoExtractor class for extracting asset information from various sources
class AssetInfoExtractor:
    def __init__(self, database: Database) -> None:
        self._database = database
        self._exchange_acronym: str | None = None
        self._yfinance_data_extractor = YahooFinanceDataExtractor(self._database)
        self._yfinance_asset_info: YFinanceAssetInfo | None = None
        self._asset_info_with_names: AssetInfoWithNames | None = None
        self._asset_info_with_ids: AssetInfoWithIDs | None = None
        self._df_asset_info: pd.DataFrame | None = None

    def _replace_delisted_asset_info(self) -> None:
        # Get the exchange_id for Cboe Canada
        cboe_ca_exchange_id = asset_info_extractor.get_exchange_id_by_exchange_acronym("Cboe CA")

        if df_data["asset_account"][0] != "Crypto":
            if df_data["currency"][0] == "CAD":
                if df_asset_info["exchange_listing_id"] == cboe_ca_exchange_id:
                    yf_asset_info = asset_info_extractor.get_asset_info_from_yf_website("NE", formatted_symbol)
                else:
                    if formatted_symbol == "SJR-B":
                        temp_symbol = "RCI-B"
                        yf_asset_info = asset_info_extractor.get_asset_info_from_yf(temp_symbol + ".TO")
                        if yf_asset_info is None:
                            raise Exception(f"yf_asset_info is None for symbol: '{temp_symbol}.TO'")
                        yf_asset_info["symbol"] = "SJR-B.TO bought out by RCI-B.TO"
                        yf_asset_info["company_name"] = "Shaw Communications bought out by Rogers Communications"
                    else:
                        yf_asset_info = asset_info_extractor.n(formatted_symbol + ".TO")
                        if yf_asset_info is None:
                            raise Exception(f"yf_asset_info is None for symbol: '{formatted_symbol}.TO'")
            else:
                yf_asset_info = asset_info_extractor.get_asset_info_from_yf(formatted_symbol    )

    def _extract_asset_info_from_yfinance(self, asset_symbol: str) -> None:
        if self._exchange_acronym is None:
            raise ValueError("Exchange Acronym must be extracted before Asset Info With Names.")
        # Extract the asset info with names
        if self._exchange_acronym == "Cboe CA":
            self._yfinance_data_extractor.extract_asset_info_from_yfinance_website("NE", asset_symbol)
        else:
            self._yfinance_data_extractor.extract_asset_info_from_yfinance(asset_symbol)
        # Get the asset info with names
        yf_asset_info = self._yfinance_data_extractor.get_yfinance_asset_info()
        if yf_asset_info is None:
            logging.warning(f"Could not retrieve asset information for {asset_symbol} from Yahoo Finance.")
            return None
        self._yfinance_asset_info = yf_asset_info


    # def _cleanup_asset_info(self) -> None:
    #     if self._asset_symbol is None:
    #         logging.error(f"Asset Symbol needs to be provided before it can be formatted.")
    #         return None
    #     if self._yf_asset_info is None:
    #         logging.error(f"Asset Info needs to be extracted from Yahoo Finance before it can be formatted.")
    #         return None
    #     else:
    #         # Format the asset class name
    #         asset_class_name = self._yf_asset_info.asset_class_name
    #         available_asset_classes = self._database.query_executor.get_all_asset_class_names()
    #         if available_asset_classes is None:
    #             logging.error(f"Could not find any asset classes in the database.")
    #             return None
    #         if asset_class_name.lower() in available_asset_classes:
    #             asset_class_name = asset_class_name.lower()
    #         elif asset_class_name.upper() in available_asset_classes:
    #             asset_class_name = asset_class_name.upper()
    #         else:
    #             fund_asset_subclass_names = self._database.query_executor.get_asset_subclass_names_by_asset_class_name("fund")
    #             if fund_asset_subclass_names is None:
    #                 logging.error(f"Could not find any asset subclasses for asset class 'fund' in the database.")
    #                 return None
    #             if asset_class_name.lower() in fund_asset_subclass_names or asset_class_name.upper() in fund_asset_subclass_names:
    #                 asset_class_name = "fund"

    #         # # Get the available asset subclasses from the database
    #         # available_asset_subclasses = self._database.query_executor.get_all_asset_subclass_names()
    #         # if available_asset_subclasses is None:
    #         #     logging.error(f"Could not find any asset subclasses in the database.")
    #         #     return None
    #         # # Get exchange_id from the database
    #         # exchange_id = self._database.query_executor.get_exchange_id_by_exchange_acronym(exchange_acronym)
    #         # if exchange_id is None:
    #         #     logging.error(f"Could not find exchange_id for {exchange_acronym} in the database.")
    #         #     return None
    #         # # Get the company_name from the database
    #         # company_name = self._database.query_executor.get_company_name_by_exchange_id_and_symbol(exchange_id, self._asset_symbol)
    #         # if company_name is None:
    #         #     logging.error(f"Could not find company_name for {self._asset_symbol} on {exchange_acronym} in the database.")
    #         #     return None
    #         # # Synonyms for Common Stock
    #         # common_stock_synonyms = ["common stock", "common stocks", "common", "stock", "stocks", 
    #         #                          "common share", "common shares", "share", "shares",
    #         #                          "class a", "class b", "class c", "class d"]
    #         # asset_subclass_name = None
    #         # for name in available_asset_subclasses:
    #         #     if name == common_stock_synonyms[0]:
    #         #         for synonym in common_stock_synonyms:
    #         #             if synonym in company_name.lower():
    #         #                 asset_subclass_name = name
    #         #                 break
    #         #     elif name in company_name.lower():
    #         #         asset_subclass_name = name.lower()
    #         #         break
    #         #     elif name in company_name.upper():
    #         #         asset_subclass_name = name.upper()
    #         #         break
    #         # if asset_subclass_name is None:
    #         #     asset_subclass_name = asset_class_name
    #         #     logging.error(f"Could not find asset subclass for {self._yf_asset_info.} on Yahoo Finance, using asset class as placeholder.")
            
    #         sector_name = 
    #         industry_name = str(df_asset_info.get("industry")).lower()

    #         # Format country_name to match the database entries
    #         country_name = str(df_asset_info.get("country")).title()
    #         if country_name == "United States":
    #             country_name = "United States of America (the)"
    #         elif country_name == "United Kingdom":
    #             country_name = "United Kingdom of Great Britain and Northern Ireland (the)"
    #         elif country_name == "None":
    #             if str(df_asset_info.get("currency")).upper() == "USD":
    #                 country_name = "United States of America (the)"
    #             elif str(df_asset_info.get("currency")).upper() == "CAD":
    #                 country_name = "Canada"
    #             elif str(df_asset_info.get("currency")).upper() == "GBP":
    #                 country_name = "United Kingdom of Great Britain and Northern Ireland (the)"

    #         # Use "N/A" if city is not available
    #         city_name = str(df_asset_info.get("city")).title()
    #         if city_name == "None":
    #             city_name = "N/A"
            
    #         # Financial currency is the currency used for financial statements
    #         financial_currency_iso_code = str(df_asset_info.get("financialCurrency")).upper()
    #         if financial_currency_iso_code == "NONE":
    #             financial_currency_iso_code = str(df_asset_info.get("currency")).upper()
            
    #         exchange_currency_iso_code = str(df_asset_info.get("currency")).upper()
    #         company_name = str(df_asset_info.get("shortName")).title() # or "longName"
    #         business_summary = str(df_asset_info.get("longBusinessSummary"))
    #         website = str(df_asset_info.get("website"))
    #         logo_url = str(df_asset_info.get("logo_url"))
    #     # else:
    #     #     return None


    # def _merge_exchange_listings_info_and_yfinance_info(self, df_exchange_listings_info: pd.DataFrame) -> AssetInfoWithNames | None:
    #     self._yf_asset_info
    #     # Return the asset info
    #     asset_info_names = AssetInfoWithNames(
    #         asset_class_name,
    #         asset_subclass_name,
    #         sector_name,
    #         industry_name,
    #         country_name,
    #         city_name,
    #         financial_currency_iso_code,
    #         exchange_currency_iso_code,
    #         exchange_acronym,
    #         asset_symbol,
    #         company_name,
    #         business_summary,
    #         website,
    #         logo_url
    #     )
    #     logging.debug(f"Filtered asset_info_names: {asset_info_names}")
    #     return asset_info_names

    def _get_asset_class_id(self, asset_class_name: str) -> int | None:
        return self._database.query_executor.get_asset_class_id_by_asset_class_name(asset_class_name)
    
    def _get_asset_subclass_id(self, asset_subclass_name: str) -> int | None:
        return self._database.query_executor.get_asset_subclass_id_by_asset_subclass_name(asset_subclass_name)
    
    def _get_sector_id_or_insert(self, asset_class_id: int, sector_name: str) -> int | None:
        sector_id = self._database.query_executor.get_sector_id_by_sector_name(sector_name)
        if sector_id is None:
            self._database.query_executor.insert_sector(asset_class_id, sector_name)
        sector_id = self._database.query_executor.get_sector_id_by_sector_name(sector_name)
        return sector_id
    
    def _get_industry_id_or_insert(self, sector_id: int, industry_name: str) -> int | None:
        industry_id = self._database.query_executor.get_industry_id_by_industry_name(industry_name)
        if industry_id is None:
            self._database.query_executor.insert_industry(sector_id, industry_name)
        industry_id = self._database.query_executor.get_industry_id_by_industry_name(industry_name)
        return industry_id
    
    def _get_country_id(self, country_name: str) -> int | None:
        return self._database.query_executor.get_country_id_by_country_name(country_name)
    
    def _get_city_id_or_insert(self, city_name: str, country_name: str) -> int | None:
        city_id = self._database.query_executor.get_city_id_by_city_name(city_name)
        if city_id is None:
            self._database.query_executor.insert_city(city_name, country_name)
        city_id = self._database.query_executor.get_city_id_by_city_name(city_name)
        return city_id
    
    def _get_currency_id(self, currency_iso_code: str) -> int | None:
        return self._database.query_executor.get_currency_id_by_currency_iso_code(currency_iso_code)

    def _get_exchange_id(self, exchange_acronym: str) -> int | None:
        return self._database.query_executor.get_exchange_id_by_exchange_acronym(exchange_acronym)

    def _convert_asset_info_with_names_to_ids(self) -> None:
        # Check if the asset info with names has been extracted
        if self._asset_info_with_names is None:
            raise ValueError("Asset Info with names must be extracted before converting to asset info with IDs.")
        
        # Asset Class
        asset_class_name = self._asset_info_with_names.asset_class_name
        if asset_class_name is None:
            raise ValueError("Asset Class Name must be provided.")
        asset_class_id = self._get_asset_class_id(asset_class_name)
        if asset_class_id is None:
            raise ValueError("Asset Class ID is None.")
        # Asset Subclass
        asset_subclass_name = self._asset_info_with_names.asset_subclass_name
        if asset_subclass_name is None:
            raise ValueError("Asset Subclass Name must be provided.")
        asset_subclass_id = self._get_asset_subclass_id(asset_subclass_name)
        if asset_subclass_id is None:
            raise ValueError("Asset Subclass ID is None.")
        # Sector
        sector_name = self._asset_info_with_names.sector_name
        if sector_name is None:
            raise ValueError("Sector Name must be provided.")
        sector_id = self._get_sector_id_or_insert(asset_class_id, sector_name)
        if sector_id is None:
            raise ValueError("Sector ID is None.")
        # Industry
        industry_name = self._asset_info_with_names.industry_name
        if industry_name is None:
            raise ValueError("Industry Name must be provided.")
        industry_id = self._get_industry_id_or_insert(sector_id, industry_name)
        if industry_id is None:
            raise ValueError("Industry ID is None.")
        # Country
        country_name = self._asset_info_with_names.country_name
        if country_name is None:
            raise ValueError("Country Name must be provided.")
        country_id = self._get_country_id(country_name)
        if country_id is None:
            logging.debug(f"Country Name: '{country_name}' returned None.")
            raise ValueError("Country ID is None.")
        # City
        city_name = self._asset_info_with_names.city_name
        if city_name is None:
            raise ValueError("City Name must be provided.")
        city_id = self._get_city_id_or_insert(city_name, country_name)
        if city_id is None:
            raise ValueError("City ID is None.")
        # Financial Currency
        financial_currency_iso_code = self._asset_info_with_names.financial_currency_iso_code
        if financial_currency_iso_code is None:
            raise ValueError("Financial Currency ISO Code must be provided.")
        financial_currency_id = self._get_currency_id(financial_currency_iso_code)
        if financial_currency_id is None:
            raise ValueError("Financial Currency ID is None.")
        # Exchange Currency
        exchange_currency_iso_code = self._asset_info_with_names.exchange_currency_iso_code
        if exchange_currency_iso_code is None:
            raise ValueError("Exchange Currency ISO Code must be provided.")
        exchange_currency_id = self._get_currency_id(exchange_currency_iso_code)
        if exchange_currency_id is None:
            raise ValueError("Exchange Currency ID is None.")
        # Exchange Acronym
        exchange_acronym = self._asset_info_with_names.exchange_acronym
        if exchange_acronym is None:
            raise ValueError("Exchange Acronym must be provided.")
        exchange_id = self._get_exchange_id(exchange_acronym)
        if exchange_id is None:
            raise ValueError("Exchange ID is None.")
        # All remaining fields
        symbol = self._asset_info_with_names.symbol
        company_name = self._asset_info_with_names.company_name
        business_summary = self._asset_info_with_names.business_summary
        website = self._asset_info_with_names.website
        logo_url = self._asset_info_with_names.logo_url
        
        self._asset_info_with_ids = AssetInfoWithIDs(
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

    def _insert_asset_info_to_database(self) -> None:
        # Check if the asset info has been extracted
        if self._asset_info_with_ids is None:
            raise ValueError("Asset Info must be extracted and put into a data frame before inserting into the database.")
        # Insert the asset info into the database
        self._database.query_executor.insert_asset_info_with_ids(self._asset_info_with_ids)


    def initialize_asset_info(self, df_exchange_listings_info: pd.DataFrame, exchange_acronym: str) -> None:
        self._exchange_acronym = exchange_acronym
        for index, row in df_exchange_listings_info.iterrows():
            # Get asset info with names
            self._extract_asset_info_from_yfinance(row["symbol"])
            # Convert asset info with names to asset info with IDs
            self._convert_asset_info_with_names_to_ids()
            # Insert asset info into the database
            self._insert_asset_info_to_database()
        print(f"Asset Info for {exchange_acronym} has been initialized.")
        logging.info(f"Asset Info for {exchange_acronym} has been initialized.")


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
