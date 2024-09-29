# Purpose: 

# Standard Libraries
from typing import TypedDict

# Third-party Libraries
import pandas as pd

# Local Modules
from import_modules.web_scraper import WebScraper

# Configure logging
import logging

# Website links:
# https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average
# https://en.wikipedia.org/wiki/S&P/TSX_Composite_Index#List_of_companies
# https://en.wikipedia.org/wiki/List_of_S%26P_500_companies

class IndexData(TypedDict):
    name: str
    symbol: str
    website_url: str
    table_index: int
    symbol_column: str


class IndexHoldingsExtractor:
    def __init__(self, index_data: IndexData) -> None:
        self._index_data = index_data

    def get_holdings_from_index(self) -> pd.DataFrame | None:
        # Reate the HTML text from the specified URL
        html_text = WebScraper(user_agent=True).get_html_content_as_text(self._index_data["website_url"])
        if html_text is None:
            return None
        # Extract the tables from the HTML text
        html_tables = pd.read_html(html_text)
        # Access the specific table based on the table_index
        index_table = html_tables[self._index_data["table_index"]]
        # Extract the column indicated by "ticker_column" and convert to a list
        index_holdings = index_table[self._index_data["symbol_column"]].tolist()
        # Create a DataFrame from the list of tickers
        index_holdings_df = pd.DataFrame(index_holdings, columns=["symbol"])
        return index_holdings_df


def main():
    # TODO - grab all info for each stock from yfinance and store in the database

    wiki = "https://en.wikipedia.org/wiki/"

    sp500 = "List_of_S&P_500_companies"
    nasdaq100 = "NASDAQ-100"
    dow30 = "Dow_Jones_Industrial_Average"
    russell2000 = "Russell_2000_Index"
    tsx60 = "S&P/TSX_60"
    tsx_composite = "S&P/TSX_Composite_Index"

    index_wiki_url = {
        "S&P 500": wiki + sp500,
        "NASDAQ 100": wiki + nasdaq100,
        "Dow Jones Industrial Average": wiki + dow30,
        "Russell 2000": wiki + russell2000,
        "S&P/TSX 60": wiki + tsx60,
        "S&P/TSX Composite Index": wiki + tsx_composite
    }

    index_holdings = {
        "S&P 500": [],
        "NASDAQ 100": [],
        "Dow Jones Industrial Average": [],
        "Russell 2000": [],
        "S&P/TSX 60": [],
        "S&P/TSX Composite Index": []
    }

    
if __name__ == "__main__":
    print("This module is not meant to be executed directly...")
