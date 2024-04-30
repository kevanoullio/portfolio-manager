# Purpose: 

# Standard Libraries

# Third-party Libraries
import requests
import yfinance as yf

# Local Modules
from database_management.database import Database
from import_modules.web_scraper import WebScraper
from database_management.schema.asset_dataclass import YFinanceAssetInfo

# Configure logging
import logging


# YahooFinanceDataExtractor class for extracting data from Yahoo Finance using the yfinance library
# class YahooFinanceDataExtractor:
#     def __init__(self, database: Database) -> None:
#         self._database = database
#         self._asset_symbol: str | None = None
#         self._yfinance_asset_info: YFinanceAssetInfo | None = None

#     def _format_symbol_for_yfinance(self, original_symbol: str) -> str:
#         # Check if the symbol has ".___" in it, yfinance requires it to be "-___"
#         if ".A" in original_symbol:
#             formatted_symbol = original_symbol.replace(".", "-")
#         elif ".B" in original_symbol:
#             formatted_symbol = original_symbol.replace(".", "-")
#         elif ".UN" in original_symbol:
#             formatted_symbol = original_symbol.replace(".", "-")
#         elif ".X" in original_symbol:
#             formatted_symbol = original_symbol.replace(".", "-")
#         elif ".PR." in original_symbol:
#             formatted_symbol = original_symbol.replace(".PR.", "-P")
#         elif "$" in original_symbol:
#             formatted_symbol = original_symbol.replace("$", "-P")
#         else:
#             formatted_symbol = original_symbol
#         return formatted_symbol
    
#     def _get_asset_info_from_yfinance(self, asset_symbol: str) -> dict | None:
#         try:
#             ticker = yf.Ticker(self._format_symbol_for_yfinance(asset_symbol))
#             if ticker.info is None:
#                 logging.error(f"Asset symbol {asset_symbol} not found on Yahoo Finance.")
#                 raise ValueError(f"Asset symbol {asset_symbol} not found on Yahoo Finance.")
#             else:
#                 logging.debug(f"df_asset_info: {ticker.info}")
#                 return ticker.info
#         except requests.exceptions.HTTPError as err:
#             print(f"HTTP error occurred for symbol {asset_symbol}: {err}")
#             return None
#         except ValueError as err:
#             print(f"Value error occurred for symbol {asset_symbol}: {err}")
#             return None

#     def _store_raw_yfinance_data(self) -> None:
#         if self._asset_symbol is None:
#             logging.error("Asset symbol is None.")
#             return None
        
#         # Get the raw yahoo finance data
#         df_asset_info = self._get_asset_info_from_yfinance(self._asset_symbol)

#         # Store the desired raw yahoo finance data
#         if df_asset_info is None:
#             logging.error(f"Could not find any asset info for {self._asset_symbol} on Yahoo Finance.")
#             return None
#         self._yfinance_asset_info = YFinanceAssetInfo(
#             asset_class_name=str(df_asset_info.get("quoteType")),
#             sector_name=str(df_asset_info.get("sector")),
#             industry_name=str(df_asset_info.get("industry")),
#             country_name=str(df_asset_info.get("country")),
#             city_name=str(df_asset_info.get("city")),
#             financial_currency_iso_code=str(df_asset_info.get("financialCurrency")),
#             company_name=str(df_asset_info.get("shortName")),
#             business_summary=str(df_asset_info.get("longBusinessSummary")),
#             website=str(df_asset_info.get("website")),
#             logo_url=str(df_asset_info.get("logo_url"))
#         )

#     def extract_asset_info_from_yfinance(self, asset_symbol: str) -> None:        
#         # Store the asset symbol
#         self._asset_symbol = asset_symbol

#         # Store the desired raw yahoo finance data
#         self._store_raw_yfinance_data()

#     def extract_asset_info_from_yfinance_website(self, asset_symbol: str, exchange_in_url: str) -> None:
#         # Store the asset symbol
#         self._asset_symbol = asset_symbol

#         # Create a WebScraper object
#         web_scraper = WebScraper(user_agent=True)
#         # Format the url
#         url = "https://finance.yahoo.com/quote/" + self._asset_symbol + "." + exchange_in_url + "/profile?p=" + self._asset_symbol + "." + exchange_in_url
#         # Get the html from the url
#         text_content = web_scraper.get_html_content_as_text(url)
#         # Scrape the text for the asset information

#         # logging.info(f"text_content: {text_content}")
        
#         # Store the desired raw yahoo finance data
#         self._store_raw_yfinance_data()

#     def get_yfinance_asset_info(self) -> YFinanceAssetInfo | None:
#         return self._yfinance_asset_info


class YahooFinanceDataExtractor:
    def __init__(self, database: Database) -> None:
        self._database = database
        self._asset_symbol: str | None = None
        self._yfinance_asset_info: YFinanceAssetInfo | None = None

    def _format_symbol_for_yfinance(self, original_symbol: str) -> str:
        # Check if the symbol has ".___" in it, yfinance requires it to be "-___"
        if ".A" in original_symbol:
            formatted_symbol = original_symbol.replace(".", "-")
        elif ".B" in original_symbol:
            formatted_symbol = original_symbol.replace(".", "-")
        elif ".UN" in original_symbol:
            formatted_symbol = original_symbol.replace(".", "-")
        elif ".X" in original_symbol:
            formatted_symbol = original_symbol.replace(".", "-")
        elif ".PR." in original_symbol:
            formatted_symbol = original_symbol.replace(".PR.", "-P")
        elif "$" in original_symbol:
            formatted_symbol = original_symbol.replace("$", "-P")
        else:
            formatted_symbol = original_symbol
        return formatted_symbol
    
    def _get_asset_info_from_yfinance(self, asset_symbol: str) -> dict | None:
        try:
            ticker = yf.Ticker(self._format_symbol_for_yfinance(asset_symbol))
            if ticker.info is None:
                logging.error(f"Asset symbol {asset_symbol} not found on Yahoo Finance.")
                raise ValueError(f"Asset symbol {asset_symbol} not found on Yahoo Finance.")
            else:
                logging.debug(f"df_asset_info: {ticker.info}")
                return ticker.info
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred for symbol {asset_symbol}: {err}")
            return None
        except ValueError as err:
            print(f"Value error occurred for symbol {asset_symbol}: {err}")
            return None

    def _store_raw_yfinance_data(self, df_asset_info: dict) -> None:
        # Store the yahoo finance data in a YFinanceAssetInfo object
        self._yfinance_asset_info = YFinanceAssetInfo(
            asset_class_name=str(df_asset_info.get("quoteType")),
            sector_name=str(df_asset_info.get("sector")),
            industry_name=str(df_asset_info.get("industry")),
            country_name=str(df_asset_info.get("country")),
            city_name=str(df_asset_info.get("city")),
            financial_currency_iso_code=str(df_asset_info.get("financialCurrency")),
            company_name=str(df_asset_info.get("shortName")),
            business_summary=str(df_asset_info.get("longBusinessSummary")),
            website=str(df_asset_info.get("website")),
            logo_url=str(df_asset_info.get("logo_url"))
        )

    # def extract_asset_info_from_yfinance_website(self, asset_symbol: str, exchange_in_url: str) -> None:
    #     # Store the asset symbol
    #     self._asset_symbol = asset_symbol

    #     # Create a WebScraper object
    #     web_scraper = WebScraper(user_agent=True)
    #     # Format the url
    #     url = "https://finance.yahoo.com/quote/" + self._asset_symbol + "." + exchange_in_url + "/profile?p=" + self._asset_symbol + "." + exchange_in_url
    #     # Get the html from the url
    #     text_content = web_scraper.get_html_content_as_text(url)
    #     # Scrape the text for the asset information

    #     # logging.info(f"text_content: {text_content}")
        
    #     # Store the desired raw yahoo finance data
    #     self._store_raw_yfinance_data()

    def extract_asset_info_from_yfinance(self, asset_symbol: str) -> None:  
        # Get the raw yahoo finance data
        df_asset_info = self._get_asset_info_from_yfinance(asset_symbol)

        # Check if the asset info is None
        if df_asset_info is None:
            logging.error(f"Could not find any asset info for {asset_symbol} on Yahoo Finance.")
            return None
              
        # Store the raw yahoo finance data
        self._store_raw_yfinance_data(df_asset_info)

    def get_yfinance_asset_info(self) -> YFinanceAssetInfo | None:
        return self._yfinance_asset_info

if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
