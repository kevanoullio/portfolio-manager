# Purpose: Asset Info Extractor module for extracting asset information from various sources.

# Standard Libraries

# Third-party Libraries
import pandas as pd

# Local Modules
from database_management.database import Database
from database_management.schema.schema import AssetInfoWithNames, AssetInfoWithIDs
# from import_modules.web_scraper import WebScraper
# from import_modules.csv_file_manager import CSVFileManager
# from import_modules.txt_file_manager import TXTFileManager

# Configure logging
import logging


class AssetInfoExtractor:
    def __init__(self, database: Database) -> None:
        self._database = database
        # self._web_scraper = WebScraper(user_agent=True)
        self._asset_info_with_names: AssetInfoWithNames | None = None
        self._asset_info_with_ids: AssetInfoWithIDs | None = None
        self._df_asset_info: pd.DataFrame | None = None

    def get_asset_class_id(self, asset_class_name: str) -> int | None:
        return self._database.query_executor.get_asset_class_id_by_asset_class_name(asset_class_name)
    
    def get_asset_subclass_id(self, asset_subclass_name: str) -> int | None:
        return self._database.query_executor.get_asset_subclass_id_by_asset_subclass_name(asset_subclass_name)
    
    def get_sector_id_or_insert(self, sector_name: str) -> int | None:
        sector_id = self._database.query_executor.get_sector_id_by_sector_name(sector_name)
        if sector_id is None:
            self._database.query_executor.insert_sector(sector_name)
        sector_id = self._database.query_executor.get_sector_id_by_sector_name(sector_name)
        return sector_id
    
    def get_industry_id_or_insert(self, industry_name: str) -> int | None:
        industry_id = self._database.query_executor.get_industry_id_by_industry_name(industry_name)
        if industry_id is None:
            self._database.query_executor.insert_industry(industry_name)
        industry_id = self._database.query_executor.get_industry_id_by_industry_name(industry_name)
        return industry_id
    
    def get_country_id(self, country_iso_code: str) -> int | None:
        return self._database.query_executor.get_country_id_by_country_iso_code(country_iso_code)
    
    def get_city_id_or_insert(self, city_name: str, country_name: str) -> int | None:
        city_id = self._database.query_executor.get_city_id_by_city_name(city_name)
        if city_id is None:
            self._database.query_executor.insert_city(city_name, country_name)
        city_id = self._database.query_executor.get_city_id_by_city_name(city_name)
        return city_id
    
    def get_currency_id(self, currency_iso_code: str) -> int | None:
        return self._database.query_executor.get_currency_id_by_currency_iso_code(currency_iso_code)

    def get_exchange_id(self, exchange_acronym: str) -> int | None:
        return self._database.query_executor.get_exchange_id_by_exchange_acronym(exchange_acronym)
    
    def asset_info_with_names_to_asset_info_with_ids(self) -> None:
        # Check if the asset info with names has been extracted
        if self._asset_info_with_names is None:
            raise ValueError("Asset Info with names must be extracted before converting to asset info with IDs.")
        
        asset_class_name = self._asset_info_with_names.asset_class_name
        asset_class_id = self.get_asset_class_id(asset_class_name)
        if asset_class_name is None or asset_class_id is None:
            raise ValueError("Asset Class Name must be provided.")
        asset_subclass_name = self._asset_info_with_names.asset_subclass_name
        asset_subclass_id = self.get_asset_subclass_id(asset_subclass_name)
        if asset_subclass_name is None or asset_subclass_id is None:
            raise ValueError("Asset Subclass Name must be provided.")
        sector_name = self._asset_info_with_names.sector_name
        sector_id = self.get_sector_id_or_insert(sector_name)
        if sector_name is None or sector_id is None:
            raise ValueError("Sector Name must be provided.")
        industry_name = self._asset_info_with_names.industry_name
        industry_id = self.get_industry_id_or_insert(industry_name)
        if industry_name is None or industry_id is None:
            raise ValueError("Industry Name must be provided.")
        country_name = self._asset_info_with_names.country_name
        country_id = self.get_country_id(country_name)
        if country_name is None or country_id is None:
            raise ValueError("Country Name must be provided.")
        city_name = self._asset_info_with_names.city_name
        city_id = self.get_city_id_or_insert(city_name, country_name)
        if city_name is None or city_id is None:
            raise ValueError("City Name must be provided.")
        currency_iso_code = self._asset_info_with_names.currency_iso_code
        currency_id = self.get_currency_id(currency_iso_code)
        if currency_iso_code is None or currency_id is None:
            raise ValueError("Currency ISO Code must be provided.")
        exchange_acronym = self._asset_info_with_names.exchange_acronym
        exchange_id = self.get_exchange_id(exchange_acronym)
        if exchange_acronym is None or exchange_id is None:
            raise ValueError("Exchange Acronym must be provided.")
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
            currency_id,
            exchange_id,
            symbol,
            company_name,
            business_summary,
            website,
            logo_url
        )

    def asset_info_with_ids_to_dataframe(self) -> None:
        # Check if the asset info has been extracted
        if self._asset_info_with_ids is None:
            raise ValueError("Asset Info must be extracted and formatted based on IDs before putting into a data frame.")
        # Convert the asset info to a dict
        asset_info_dict = self._asset_info_with_ids.to_dict()
        # Create a data frame from the asset info
        self._df_asset_info = pd.DataFrame.from_dict(asset_info_dict)

    def insert_asset_info_to_database(self) -> None:
        # Check if the asset info has been extracted
        if self._df_asset_info is None:
            raise ValueError("Asset Info must be extracted and put into a data frame before inserting into the database.")
        # Insert the asset info into the database
        self._database.query_executor.dataframe_to_existing_sql_table(self._df_asset_info, "asset_info")


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
