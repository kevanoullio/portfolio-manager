# Purpose: Import portfolio from CSV file

# Standard Libraries

# Third-party Libraries
import pandas as pd

# Local modules
from database_management.database import Database
from database_management.schema.asset_dataclass import AssetTransaction

# Local modules imported for Type Checking purposes only

# Configure logging
import logging


# AssetTransactionManager class for appending asset transactions, converting to DataFrame so they can be imported into the database
class AssetTransactionManager:
	def __init__(self, database: Database):
		self.__database = database

	def get_asset_id(self, asset_symbol: str) -> int | None:
		return self.__database.query_executor.get_asset_id_by_asset_symbol(asset_symbol)

	def get_transaction_type_id(self, transaction_type: str) -> int | None:
		return self.__database.query_executor.get_transaction_type_id_by_transaction_type_name(transaction_type)

	def get_brokerage_id_or_insert(self, brokerage_name: str) -> int | None:
		brokerage_id = self.__database.query_executor.get_brokerage_id_by_brokerage_name(brokerage_name)
		if brokerage_id is None:
			self.__database.query_executor.insert_brokerage(brokerage_name)
			print(f"Brokerage {brokerage_name} not found. Inserted into the database.")
			logging.info(f"Brokerage {brokerage_name} not found. Inserted into the database.")
		brokerage_id = self.__database.query_executor.get_brokerage_id_by_brokerage_name(brokerage_name)
		return brokerage_id

	def get_investment_account_id_or_insert(self, brokerage_id: int, investment_account_name: str) -> int | None:
		investment_account_id = self.__database.query_executor.get_investment_account_id_by_investment_account_name(brokerage_id, investment_account_name)
		if investment_account_id is None:
			self.__database.query_executor.insert_investment_account(brokerage_id, investment_account_name)
			print(f"Investment account {investment_account_name.lower().replace(' ', '_')} not found. Inserted into the database.")
			logging.info(f"Investment account {investment_account_name.lower().replace(' ', '_')} not found. Inserted into the database.")
		investment_account_id = self.__database.query_executor.get_investment_account_id_by_investment_account_name(brokerage_id, investment_account_name)
		return investment_account_id

	def find_asset_info(self, symbol: str) -> list[tuple] | None:
		query = f"SELECT * FROM asset_info WHERE symbol = '{symbol}'"
		asset_info = self.__database.query_executor.execute_query(query)
		return asset_info

	def insert_asset_transaction_to_database(self, asset_transaction: AssetTransaction) -> None:
		# Convert the asset transaction to a dictionary
		asset_transaction_dict = asset_transaction.to_dict()
		# Insert asset transaction into the database
		self.__database.query_executor.dictionary_to_existing_sql_table(asset_transaction_dict, "asset_transaction")


def import_portfolio_from_csv(database: Database) -> None:
	pass


if __name__ == "__main__":
	print("This module is not meant to be executed directly.")
