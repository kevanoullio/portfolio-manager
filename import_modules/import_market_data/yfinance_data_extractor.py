# Purpose: 

# Standard Libraries

# Third-party Libraries
import yfinance as yf

# Local Modules
from import_modules.web_scraper import WebScraper

# Configure logging
import logging


# YahooFinanceDataExtractor class for extracting data from Yahoo Finance using the yfinance library
class YahooFinanceDataExtractor:
    def __init__(self) -> None:
        self._asset_info_names_dict = {
                    "sector_name": "",
                    "industry_name": "",
                    "country_name": "",
                    "city_name": "",
                    "currency_iso_code": "",
                    "exchange_acronym": "",
                    "symbol": "",
                    "company_name": "",
                    "business_summary": "",
                    "website": "",
                    "logo_url": ""
                }

    def get_asset_info_names_dict(self) -> dict[str, str]:
        return self._asset_info_names_dict

    def _format_symbol_for_yf(self, original_symbol: str) -> str:
        # Check if the symbol has ".___" in it, yfinance requires it to be "-___"
        if ".A" in original_symbol:
            formatted_symbol = original_symbol.replace(".", "-")
        elif ".B" in original_symbol:
            formatted_symbol = original_symbol.replace(".", "-")
        elif ".UN" in original_symbol:
            formatted_symbol = original_symbol.replace(".", "-")
        elif ".X" in original_symbol:
            formatted_symbol = original_symbol.replace(".", "-")
        else:
            formatted_symbol = original_symbol
        return formatted_symbol

    def get_asset_info_from_yf(self, asset_symbol: str) -> dict[str, str] | None:
            df_asset_info = yf.Ticker(self._format_symbol_for_yf(asset_symbol)).info
            if df_asset_info:
                asset_info_names_dict = {
                    "asset_class_name": df_asset_info.get("quoteType"),
                    "asset_subclass_name": df_asset_info.get("quoteType"),
                    "sector_name": df_asset_info.get("sector"),
                    "industry_name": df_asset_info.get("industry"),
                    "country_name": df_asset_info.get("country"),
                    "city_name": df_asset_info.get("city"),
                    "currency_iso_code": df_asset_info.get("currency"),
                    "exchange_acronym": df_asset_info.get("exchange"),
                    "symbol": asset_symbol,
                    "company_name": df_asset_info.get("shortName"), # or "longName"
                    "business_summary": df_asset_info.get("longBusinessSummary"),
                    "website": df_asset_info.get("website"),
                    "logo_url": df_asset_info.get("logo_url")
                }
                for item in asset_info_names_dict:
                    if asset_info_names_dict[item] is None:
                        asset_info_names_dict[item] = ""
                return asset_info_names_dict
            else:
                return None

    def get_asset_info_from_yf_website(self, exchange_in_url: str, asset_symbol: str) -> dict[str, str] | None:
            # Create a WebScraper object
            web_scraper = WebScraper(user_agent=True)
            # Format the url
            url = "https://finance.yahoo.com/quote/" + asset_symbol + "." + exchange_in_url + "/profile?p=" + asset_symbol + "." + exchange_in_url
            # Get the html from the url
            text_content = web_scraper.get_html_content_as_text(url)
            # Scrape the text for the asset information

            logging.info(f"text_content: {text_content}")

            self._asset_info_names_dict = {
                # "asset_class_name": df_asset_info.get("quoteType"),
                # "asset_subclass_name": df_asset_info.get("quoteType"),
                "sector_name": df_asset_info.get("sector"),
                "industry_name": df_asset_info.get("industry"),
                "country_name": df_asset_info.get("country"),
                "city_name": df_asset_info.get("city"),
                "currency_iso_code": df_asset_info.get("currency"),
                "exchange_acronym": df_asset_info.get("exchange"),
                "symbol": asset_symbol,
                "company_name": df_asset_info.get("shortName"), # or "longName"
                "business_summary": df_asset_info.get("longBusinessSummary"),
                "website": df_asset_info.get("website"),
                "logo_url": df_asset_info.get("logo_url")
                }

    # def fill_in_asset_info(self, df_data: pd.DataFrame, df_asset_info: pd.DataFrame) -> None:
    #     # Get the exchange_id for Cboe Canada
    #     cboe_ca_exchange_id = asset_info_extractor.get_exchange_id_by_exchange_acronym("Cboe CA")

    #     if df_data["asset_account"][0] != "Crypto":
    #         if df_data["currency"][0] == "CAD":
    #             if df_asset_info["exchange_listing_id"] == cboe_ca_exchange_id:
    #                 yf_asset_info = asset_info_extractor.get_asset_info_from_yf_website("NE", formatted_symbol)
    #             else:
    #                 if formatted_symbol == "SJR-B":
    #                     temp_symbol = "RCI-B"
    #                     yf_asset_info = asset_info_extractor.get_asset_info_from_yf(temp_symbol + ".TO")
    #                     if yf_asset_info is None:
    #                         raise Exception(f"yf_asset_info is None for symbol: '{temp_symbol}.TO'")
    #                     yf_asset_info["symbol"] = "SJR-B.TO bought out by RCI-B.TO"
    #                     yf_asset_info["company_name"] = "Shaw Communications bought out by Rogers Communications"
    #                 else:
    #                     yf_asset_info = asset_info_extractor.n(formatted_symbol + ".TO")
    #                     if yf_asset_info is None:
    #                         raise Exception(f"yf_asset_info is None for symbol: '{formatted_symbol}.TO'")
    #         else:
    #             yf_asset_info = asset_info_extractor.get_asset_info_from_yf(formatted_symbol    )


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
