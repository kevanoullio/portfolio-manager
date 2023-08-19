# Purpose: Asset Dataclass module for storing asset information prior to formatting and inserting into the database.

# Standard Libraries
from dataclasses import dataclass

# Third-party Libraries

# Local Modules

# Configure logging
import logging


# ExchangeListingsInfo dataclass for storing exchange listing information prior to formatting and inserting into the database
@dataclass
class ExchangeListingsInfo:
    asset_class_name: str
    asset_subclass_name: str
    exchange_currency_id: int
    exchange_id: int
    symbol: str
    security_name: str

    def __post_init__(self) -> None:
        logging.debug(f"Created ExchangeListingInfo object: {self}")
    
    def __str__(self) -> str:
        return f"AssetInfo(asset_class_name={self.asset_class_name}, asset_subclass_name={self.asset_subclass_name}, " \
               f"exchange_currency_id={self.exchange_currency_id}, exchange_id={self.exchange_id}, " \
               f"symbol={self.symbol}, security_name={self.security_name}"

    def to_dict(self) -> dict[str, str | int]:
        return {
            "asset_class_name": self.asset_class_name,
            "asset_subclass_name": self.asset_subclass_name,
            "exchange_currency_id": self.exchange_currency_id,
            "exchange_id": self.exchange_id,
            "symbol": self.symbol,
            "security_name": self.security_name
        }


# YFinanceAssetInfo dataclass for storing asset information with names prior to formatting and inserting into the database
@dataclass
class YFinanceAssetInfo:
    asset_class_name: str
    sector_name: str
    industry_name: str
    country_name: str
    city_name: str
    financial_currency_iso_code: str
    company_name: str
    business_summary: str
    website: str
    logo_url: str

    def __post_init__(self) -> None:
        logging.debug(f"Created AssetInfoWithNames object: {self}")
    
    def __str__(self) -> str:
        return f"AssetInfo(asset_class_name={self.asset_class_name}, sector_name={self.sector_name}," \
               f"industry_name={self.industry_name}, country_name={self.country_name}, city_name={self.city_name}, " \
               f"financial_currency_iso_code={self.financial_currency_iso_code}, " \
               f"company_name={self.company_name}, business_summary={self.business_summary}, " \
               f"website={self.website}, logo_url={self.logo_url})"

    def to_dict(self) -> dict[str, str]:
        return {
            "asset_class_name": self.asset_class_name,
            "sector_name": self.sector_name,
            "industry_name": self.industry_name,
            "country_name": self.country_name,
            "city_name": self.city_name,
            "financial_currency_iso_code": self.financial_currency_iso_code,
            "company_name": self.company_name,
            "business_summary": self.business_summary,
            "website": self.website,
            "logo_url": self.logo_url
        }

# AssetInfoWithNames dataclass for storing asset information with names prior to formatting and inserting into the database
@dataclass
class AssetInfoWithNames:
    asset_class_name: str
    asset_subclass_name: str
    sector_name: str
    industry_name: str
    country_name: str
    city_name: str
    financial_currency_iso_code: str
    exchange_currency_iso_code: str
    exchange_acronym: str
    symbol: str
    company_name: str
    business_summary: str
    website: str
    logo_url: str

    def __post_init__(self) -> None:
        logging.debug(f"Created AssetInfoWithNames object: {self}")
    
    def __str__(self) -> str:
        return f"AssetInfo(asset_class_name={self.asset_class_name}, asset_subclass_name={self.asset_subclass_name}, " \
               f"sector_name={self.sector_name}, industry_name={self.industry_name}, country_name={self.country_name}, " \
               f"city_name={self.city_name}, financial_currency_iso_code={self.financial_currency_iso_code}, " \
               f"exchange_currency_iso_code={self.exchange_currency_iso_code}, exchange_acronym={self.exchange_acronym}, " \
               f"symbol={self.symbol}, company_name={self.company_name}, business_summary={self.business_summary}, " \
               f"website={self.website}, logo_url={self.logo_url})"

    def to_dict(self) -> dict[str, str]:
        return {
            "asset_class_name": self.asset_class_name,
            "asset_subclass_name": self.asset_subclass_name,
            "sector_name": self.sector_name,
            "industry_name": self.industry_name,
            "country_name": self.country_name,
            "city_name": self.city_name,
            "financial_currency_iso_code": self.financial_currency_iso_code,
            "exchange_currency_iso_code": self.exchange_currency_iso_code,
            "exchange_acronym": self.exchange_acronym,
            "symbol": self.symbol,
            "company_name": self.company_name,
            "business_summary": self.business_summary,
            "website": self.website,
            "logo_url": self.logo_url
        }


# AssetInfoWithIDs dataclass for storing asset information that exactly matches the database schema
@dataclass
class AssetInfoWithIDs:
    asset_class_id: int
    asset_subclass_id: int
    sector_id: int
    industry_id: int
    country_id: int
    city_id: int
    financial_currency_id: int
    exchange_currency_id: int
    exchange_id: int
    symbol: str
    company_name: str
    business_summary: str
    website: str
    logo_url: str

    def __post_init__(self) -> None:
        logging.debug(f"Created AssetInfoWithIDs object: {self}")
    
    def __str__(self) -> str:
        return f"AssetInfo(asset_class_id={self.asset_class_id}, asset_subclass_id={self.asset_subclass_id}, " \
               f"sector_id={self.sector_id}, industry_id={self.industry_id}, country_id={self.country_id}, " \
               f"city_id={self.city_id}, financial_currency_id={self.financial_currency_id}, " \
               f"exchange_currency_id={self.exchange_currency_id}, exchange_id={self.exchange_id}, " \
               f"symbol={self.symbol}, company_name={self.company_name}, business_summary={self.business_summary}, " \
               f"website={self.website}, logo_url={self.logo_url})"
    
    def to_dict(self) -> dict:
        return {
            "asset_class_id": self.asset_class_id,
            "asset_subclass_id": self.asset_subclass_id,
            "sector_id": self.sector_id,
            "industry_id": self.industry_id,
            "country_id": self.country_id,
            "city_id": self.city_id,
            "financial_currency_id": self.financial_currency_id,
            "exchange_currency_id": self.exchange_currency_id,
            "exchange_id": self.exchange_id,
            "symbol": self.symbol,
            "company_name": self.company_name,
            "business_summary": self.business_summary,
            "website": self.website,
            "logo_url": self.logo_url
        }


# AssetTransaction dataclass for storing asset transaction data
@dataclass
class AssetTransaction:
    user_id: int
    asset_id: int
    transaction_type_id: int
    brokerage_id: int
    asset_account_id: int
    quantity: float
    avg_price: float
    total: float
    transaction_date: str
    imported_from: str
    imported_date: str

    def __post_init__(self) -> None:
        logging.debug(f"Creating AssetTransaction object: {self}")

    def __str__(self) -> str:
        return f"AssetTransaction(user_id={self.user_id}, asset_id={self.asset_id}, " \
               f"transaction_type_id={self.transaction_type_id}, brokerage_id={self.brokerage_id}, " \
               f"asset_account_id={self.asset_account_id}, quantity={self.quantity}, avg_price={self.avg_price}, " \
               f"total={self.total}, transaction_date={self.transaction_date}, imported_from={self.imported_from}, " \
               f"imported_date={self.imported_date})"
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'asset_id': self.asset_id,
            'transaction_type_id': self.transaction_type_id,
            'brokerage_id': self.brokerage_id,
            'asset_account_id': self.asset_account_id,
            'quantity': self.quantity,
            'avg_price': self.avg_price,
            'total': self.total,
            'transaction_date': self.transaction_date,
            'imported_from': self.imported_from,
            'imported_date': self.imported_date
        }


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
