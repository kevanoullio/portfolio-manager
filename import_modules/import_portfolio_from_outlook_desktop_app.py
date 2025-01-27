# Purpose: Read emails from Outlook desktop application using win32com module.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries
from exchangelib import Credentials, Account, DELEGATE

# Local Modules
from database_management.database import Database
from database_management.schema.asset_dataclass import AssetTransaction
from user_interface.user_input import UserInput
from access_management.account_authenticator import AccountAuthenticator
from exceptions.authentication_exceptions import InvalidCredentialsError

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
	from account_management.accounts import EmailAccount

# Configure logging
import logging

# Global variables
last_uid_cache: int | None = None



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


def select_email_account(database: Database) -> EmailAccount | None:
	# Fetch all email addresses of usage "import" from the user
	import_email_accounts: list[EmailAccount] | None = database.query_executor.get_user_email_accounts_by_usage("import")
	logging.debug(f"Import email accounts: {import_email_accounts}")

	# Check if any import email addresses are found
	if import_email_accounts is None or len(import_email_accounts) <= 0:
		print("No email accounts for importing portfolios found.")
		print("Please add an email account in the account settings.")
		return None

	# TODO - Replace with AvailableEmailAccount class???
	# Print the available email accounts
	title = "AVAILABLE EMAIL ACCOUNTS:"
	print(f"\n{title}")
	for i, email_account in enumerate(import_email_accounts, start=1):
		print(f"{i}: {email_account.address}")

	# Initialize the UserInput class
	user_input = UserInput()

	# Get the user's choice
	choice = user_input.get_valid_menu_choice(len(import_email_accounts), "Choose the email account you would like to import from: ")
	# Get the email account based on the user's choice
	selected_import_email_account = import_email_accounts[choice - 1]
	logging.debug(f"Selected import email account: {selected_import_email_account}")

	# # Prompt the user for the email account password
	# provided_password_bytes: str | bytes = UserInput.password_prompt(encode=True, hash=False, prompt="Verify your email credentials by entering your email password: ", confirm=False)

	# # Ensure that the password is hashed before proceeding
	# if not isinstance(provided_password_bytes, bytes):
	# 	raise TypeError("Password must be hashed before proceeding.")

	# # Validate the user's email credentials
	# account_authenticator = AccountAuthenticator(database)
	# try:
	# 	if account_authenticator.authenticate_email_credentials(selected_import_email_account.address, provided_password_bytes):
	# 		return selected_import_email_account
	# except InvalidCredentialsError as e:
	# 	print(f"{e}")
	# 	return None
	return selected_import_email_account


def select_email_folder(folder_list: list[str]) -> str | None:
	# List available folders
	title = "Available folders:"
	print(f"\n{title}")
	print("-" * len(title))
	for folder in folder_list:
		print(folder)
	print("\n")

	folder_name = input("Enter the folder name (copy/paste from above): ").strip()
	return folder_name


def select_brokerage_name(asset_transaction_manager: AssetTransactionManager) -> int | None:
	# Prompt the user for the brokerage
	brokerage_name = input("Enter the brokerage name: ").strip()
	brokerage_id = asset_transaction_manager.get_brokerage_id_or_insert(brokerage_name)

	# Check if the brokerage ID was retrieved
	if brokerage_id is None:
		print("Failed to get brokerage ID.")
		return None

	return brokerage_id


def read_emails_from_outlook(email_address: str, password: bytes, folder_name: str = "Inbox"):
    # Set up credentials
    credentials = Credentials(email_address, password.decode())

    # Connect to the account
    account = Account(email_address, credentials=credentials, autodiscover=True, access_type=DELEGATE)

    # Access the folder
    folder = account.inbox if folder_name.lower() == "inbox" else account.root / folder_name

    # Iterate through emails
    for item in folder.all().order_by('-datetime_received')[:10]:  # Fetch the latest 10 emails
        print("Subject:", item.subject)
        print("Sender:", item.sender.email_address)
        print("Body:", item.body)
        print("-" * 50)


def import_from_outlook_desktop_app(database: Database):
	# Fetch the email account to import from
	email_account: EmailAccount | None = select_email_account(database)

	# Check if an email account was selected
	if email_account is None:
		print("No email account selected.")
		return

	# Prompt the user for the email account password
	provided_password_hash: str | bytes = UserInput.password_prompt(encode=True, hash=False, prompt="Verify your email credentials by entering your email password: ", confirm=False)

	# Ensure that the password is hashed before proceeding
	if not isinstance(provided_password_hash, bytes):
		raise TypeError("Password must be hashed before proceeding.")

	# Select the folder to import from
	folder_list = ["Inbox", "Drafts", "Junk Email", "Deleted Items"]
	selected_folder = select_email_folder(folder_list)

	# Check if a folder was selected
	if selected_folder is None:
		print("No folder selected.")
		return

	# Get the UID of the last email in the selected folder
	last_uid = database.query_executor.get_last_uid_by_email_address_and_folder_name(email_account.address, selected_folder)
	last_uid_cache = last_uid

	# Search for emails with a UID greater than the last processed email in the selected folder
	if last_uid_cache is not None:
		search_query = f"UID {int(last_uid_cache) + 1}:*"
	else:
		search_query = "ALL"

	# Prompt the user for the brokerage name
	asset_transaction_manager = AssetTransactionManager(database)
	brokerage_id = select_brokerage_name(asset_transaction_manager)

	# Check if the brokerage ID was retrieved
	if brokerage_id is None:
		print("No brokerage selected.")
		return

	# Read emails from the selected email account
	read_emails_from_outlook(email_account.address, provided_password_hash, selected_folder)

	print("No new emails to process.")
	print("Import complete!")


if __name__ == "__main__":
	print("This module is not meant to be executed directly.")
