# Purpose: 

# Standard Libraries

# Third-party Libraries
import requests
import yfinance as yf
import re

# Local Modules
# from database_management.database import Database
# from import_modules.web_scraper import WebScraper
from database_management.schema.asset_dataclass import YFinanceAssetInfo

# Configure logging
import logging


class YahooFinanceDataExtractor:
    def __init__(self) -> None:
        pass
    # def __init__(self, database: Database) -> None:
        # self.__database = database
        # self.__asset_symbol: str | None = None
        # self.__yfinance_asset_info: YFinanceAssetInfo | None = None
    
    def __format_symbol(self, original_symbol: str, char_to_replace: str, replacement_char: str) -> str:
        pattern = r'\{}([A-Z]+)'.format(char_to_replace)
        formatted_symbol = re.sub(pattern, replacement_char, original_symbol)
        return formatted_symbol

    def __format_symbol_for_yfinance(self, exchange_acronym: str, original_symbol: str) -> str:
        if exchange_acronym == "NASDAQ":
            formatted_symbol = original_symbol
        
        # Check if the symbol has ".__" in it, yfinance requires it to be "-"
        if exchange_acronym == "NYSE":
            if '.' in original_symbol:
                if ".W" in original_symbol:
                    formatted_symbol = self.__format_symbol(original_symbol, ".W", "-WT")
                else:
                    formatted_symbol = self.__format_symbol(original_symbol, '.', '-')
            elif '$' in original_symbol:
                formatted_symbol = self.__format_symbol(original_symbol, '$', "-P")
            else:
                formatted_symbol = original_symbol

        elif exchange_acronym == "NYSE MKT":
            if '.' in original_symbol:
                if ".U" in original_symbol:
                    formatted_symbol = self.__format_symbol(original_symbol, ".U", "-UN")
                if ".W" in original_symbol:
                    formatted_symbol = self.__format_symbol(original_symbol, ".W", "-WT")
                else:
                    formatted_symbol = self.__format_symbol(original_symbol, '.', '-')
            # elif '$' in original_symbol:
            #     formatted_symbol = self.__format_symbol(original_symbol, '$', "-P")
            else:
                formatted_symbol = original_symbol

        elif exchange_acronym == "NYSE ARCA":
            formatted_symbol = original_symbol

        elif exchange_acronym == "BATS":
            formatted_symbol = original_symbol

        # Check if the symbol has ".__" in it, yfinance requires it to be "-__"
        elif exchange_acronym == "TSX":
            if '.' in original_symbol:
                if ".PR." in original_symbol:
                    formatted_symbol = original_symbol.replace(".PR.", "-P")
                elif ".RT." in original_symbol:
                    formatted_symbol = original_symbol.replace(".RT.", "-RT")
                elif ".WT." in original_symbol:
                    formatted_symbol = original_symbol.replace(".WT.", "-WT")
                else:
                    formatted_symbol = self.__format_symbol(original_symbol, '.', '-')
            else:
                formatted_symbol = original_symbol
            # Add the ".TO" suffix to the symbol
            formatted_symbol += ".TO"

        elif exchange_acronym == "TSXV":
            if '.' in original_symbol:
                formatted_symbol = self.__format_symbol(original_symbol, '.', '-')
            else:
                formatted_symbol = original_symbol
            # Add the ".V" suffix to the symbol
            formatted_symbol += ".V"

        elif exchange_acronym == "CSE":
            if '.' in original_symbol:
                formatted_symbol = self.__format_symbol(original_symbol, '.', '-')
            else:
                formatted_symbol = original_symbol
            # Add the ".CN" suffix to the symbol
            formatted_symbol += ".CN"

        elif exchange_acronym == "Cboe CA":
            if '.' in original_symbol:
                formatted_symbol = self.__format_symbol(original_symbol, '.', '-')
            else:
                formatted_symbol = original_symbol
            # Add the ".NE" suffix to the symbol
            formatted_symbol += ".NE"

        return formatted_symbol
    
    def __get_asset_info_from_yfinance(self, exchange_acronym: str, asset_symbol: str) -> dict | None:
        try:
            ticker = yf.Ticker(self.__format_symbol_for_yfinance(exchange_acronym, asset_symbol))
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

    def extract_asset_info_from_yfinance(self, exchange_acronym, asset_symbol: str) -> YFinanceAssetInfo | None:  
        # Get the raw yahoo finance data
        df_asset_info = self.__get_asset_info_from_yfinance(exchange_acronym, asset_symbol)

        # Check if the asset info is None
        if df_asset_info is None:
            logging.error(f"Could not find any asset info for {asset_symbol} on Yahoo Finance.")
            return None

        # Return the raw yfinance asset info
        return YFinanceAssetInfo(
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


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
