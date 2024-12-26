# Purpose: Dashboard module for managing the user interface and all menu navigation.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries
import pandas as pd

# Local Modules
from access_management.login_manager import LoginManager
from database_management.database import Database
from user_interface.query_results import QueryResults
from user_interface.user_input import UserInput
from account_management.account_operations import UserAccountOperation, EmailAccountOperation
from import_modules.import_market_data.exchange_listings_extractor import ExchangeListingsExtractor
from import_modules.import_market_data.asset_info_extractor import AssetInfoExtractor
from exceptions.authentication_exceptions import AuthenticationError

# Local modules imported for Type Checking purposes only
# if TYPE_CHECKING:
# 	from account_management.accounts import UserAccount, EmailAccount

# Configure logging
import logging


# Dashboard class for managing the user interface and all menu navigation
class Dashboard:
	def __init__(self, database: Database, login_manager: LoginManager) -> None:
		self.__database = database
		self.__login_manager = login_manager
		self.__query_results = QueryResults()
		# self.__user_account_operation = UserAccountOperation(self.__database)
		self.__email_account_operation = EmailAccountOperation(self.__database)
		self.__is_running = False

	def __print_welcome_screen(self):
		print("\n====================================")
		print("|| Welcome to 'PORTFOLIO MANAGER' ||")
		print("====================================")

	def run(self):
		# Start the Program
		self.start_program()
		# Print the welcome screen
		self.__print_welcome_screen()

		# Import the Login menu here to avoid circular import
		from user_interface.menu import Login
		self.current_menu = Login(self)
		logging.info("Login Dashboard has started running.")

		# Main loop for the dashboard
		while self.current_menu and self.__is_running:
			# Print the menu options
			self.current_menu.print_options()
			# Get the user's choice
			choice = self.current_menu.get_valid_menu_choice()
			# Print the choice message
			self.current_menu.print_choice_msg(choice)

			next_menu = self.current_menu.menu_logic.get(choice)
			if next_menu:
				# Run the menu logic which executes the coresponding dashboard function based on user's choice
				next_menu()
				if self.__database.session_manager.get_current_user() is not None:
					self.current_menu = self.current_menu.get_next_menu(choice)
				else: # FIXME - seems like a hacky way to get the logout to work
					self.current_menu = Login(self)
					continue
			else:
				self.current_menu = None

	# menu_logic is a list of functions that are executed based on the user's choice
	# Without this function, instead of going back to the previous menu, the program would exit
	def previous_menu(self):
		pass

	def menu_without_logic(self):
		pass

	# Login Menu Functions
	def create_account(self):
		self.__login_manager.create_user_account()
		if self.__database.session_manager.get_current_user() is not None:
			logging.debug(f"User login: {self.__database.session_manager.get_current_user()}")
		else:
			logging.debug("User login failed.")

	def login(self):
		self.__login_manager.user_account_login()

	def start_program(self):
		# Start the Dashboard
		self.__is_running = True
		logging.info("Dashboard has started running.")

	def exit_program(self):
		# Stop the Dashboard
		self.__is_running = False
		logging.info("Dashboard has stopped running.")


	# Main Menu Functions
	def portfolio_manager(self):
		logging.info("Portfolio manager...")


	def account_settings(self):
		print("Account Settings logic goes here...")


	def help_information(self):
		print("Help Information logic goes here...")


	def save_changes(self):
		print("Save Changes logic goes here...")


	def discard_changes(self):
		print("Discard Changes logic goes here...")


	def logout(self):
		self.__login_manager.user_account_logout()


	def view_portfolio(self):
		print("View Portfolio logic goes here...")


	def manage_portfolio(self):
		logging.info("Managing portfolio...")


	def manage_market_data(self):
		print("Market Data logic goes here...")


	def statistical_analysis(self):
		print("Statistical Analysis logic goes here...")


	def trading_strategies(self):
		print("Trading Strategies logic goes here...")


	def reports(self):
		print("Reports logic goes here...")


	def export_data(self):
		print("Export Data logic goes here...")


	def automation(self):
		print("Automation logic goes here...")


	def notifications(self):
		print("Notifications logic goes here...")


	def view_portfolio_summary(self):
		# TODO - review and finish this function
		print("\nNET VALUE OF SECURITIES:")
		results = self.__database.query_executor.execute_complex_query_by_title("net_value_of_securities")
		self.__query_results.simple_row_print(results, currency=True)

		print("\nTOTAL VALUE OF SECURITIES:")
		results = self.__database.query_executor.execute_complex_query_by_title("total_value_of_securities")
		self.__query_results.simple_row_print(results, currency=True)

		print("\nTOTAL VALUE OF DIVIDENDS:")
		results = self.__database.query_executor.execute_complex_query_by_title("total_value_of_dividends")
		self.__query_results.simple_row_print(results, currency=True)

		print("\nTOTAL VALUE OF DIVIDENDS BY SECURITY:")
		results = self.__database.query_executor.execute_complex_query_by_title("total_value_of_dividends_by_security")
		self.__query_results.simple_row_print(results, currency=True)


	def view_current_portfolio(self):
		# TODO - review and finish this function
		results = self.__database.query_executor.execute_complex_query_by_title("view_current_portfolio")
		print("CURRENT PORTFOLIO:")
		headers = ["symbol", "total_buy_qty", "total_buy_amnt", "avg_buy_price", "total_sell_qty", "total_sell_amnt",
			   "avg_sell_price", "total_divs", "net_qty", "net_value", "net_avg_price", "break_even_value"]
		self.__query_results.print_rows_with_headers(headers, results, currency=True)


	def view_entire_portfolio_history(self):
		print("View Entire Portfolio History logic goes here...")


	def search_for_current_investment(self):
		print("Search for Current Investment logic goes here...")


	def search_for_investment_in_portfolio_history(self):
		# TODO - review and finish this function
		# Get the ticker symbol of the investment to search for, ensure it's alphanumeric
		ticker = input("Enter the ticker symbol of the investment you would like to search for: ")
		while not ticker.isalnum():
			print("Invalid ticker symbol. Please try again: ", end="")
			ticker = input()
		# Execute the query to search for an investment in portfolio history
		results = self.__database.query_executor.execute_complex_query_by_title("net_ticker_summary", (ticker, ticker, ticker))
		# Print the query results
		self.__query_results.simple_row_print(results)


	def build_portfolio_from_data_set(self):
		print("Build Portfolio from Data Set logic goes here...")


	def import_existing_portfolio_data_set(self):
		logging.info("Importing existing portfolio data set...")


	def delete_existing_portfolio_data_set(self):
		print("Delete Existing Portfolio Data Set logic goes here...")


	def manage_custom_import_scripts(self):
		print("Manage Custom Import Scripts logic goes here...")


	def add_investment_manually(self):
		print("Add Investment Manually logic goes here...")


	def modify_investment_entry(self):
		print("Modify Investment Entry logic goes here...")


	def import_existing_portfolio_from_brokerage_account(self):
		print("Import Existing Portfolio from Brokerage Account logic goes here...")


	def import_existing_portfolio_from_csv_file(self):
		print("Import Existing Portfolio from CSV File logic goes here...")


	def import_existing_portfolio_from_excel_file(self):
		print("Import Existing Portfolio from Excel File logic goes here...")


	def import_existing_portfolio_from_pdf_file(self):
		print("Import Existing Portfolio from PDF File logic goes here...")


	def import_existing_portfolio_from_database_file(self):
		# TODO - fix and finish this function
		current_user = self.__database.session_manager.get_current_user()
		# if current_user is not None:
		#     if current_user.user_id is not None:
		#         # self.database.import_file(current_user.user_id, "database", [".db"])
		# else:
		#     print("You must be logged in to import from a database file.")


	def import_existing_portfolio_from_email_account(self):
		# TODO - Use AvailableEmailAccount class instead???
		# Call the import_from_email_account script
		from import_modules.import_from_email_account import import_from_email_account
		import_from_email_account(self.__database)


	# def get_available_email_accounts(self) -> list[EmailAccount] | None:
	#     # Fetch all email addresses of usage "import" from the user
	#     import_email_accounts = self.__database.__query_executor.get_user_email_accounts_by_usage("import")
	#     # Return the list of email accounts, if there's no emails, it returns None
	#     return import_email_accounts


	def view_custom_import_scripts(self):
		print("View Custom Import Scripts logic goes here...")
		# If you want to allow users to dynamically import and execute scripts in your program without hardcoding the import statements, you can use the `importlib` module in Python. This module provides functions to dynamically import modules at runtime. Here's an example of how you can use `importlib` to achieve this:

		# ```python
		# import importlib

		# # Get the name of the script to import (assuming it's provided by the user)
		# script_name = "external_script"

		# # Import the script dynamically
		# try:
		#     imported_module = importlib.import_module(script_name)
		# except ModuleNotFoundError:
		#     print(f"Script '{script_name}' not found.")
		#     return

		# # Access functions and classes from the imported module
		# if hasattr(imported_module, "my_function"):
		#     imported_module.my_function()

		# if hasattr(imported_module, "MyClass"):
		#     obj = imported_module.MyClass()

		# # Call the main function if it exists
		# if hasattr(imported_module, "main"):
		#     imported_module.main()
		# ```

		# In this example, `importlib.import_module()` is used to dynamically import the script specified by the user. The `script_name` variable holds the name of the script (without the `.py` extension). If the script is found, you can access its functions and classes using `hasattr()` to check if they exist before using them.

		# Note that dynamically importing and executing user-provided scripts can introduce security risks. Ensure that you validate and sanitize user input to prevent potential code injection attacks or other malicious activities.


	def add_custom_import_script(self):
		print("Add Custom Import Script logic goes here...")


	def remove_custom_import_script(self):
		print("Remove Custom Import Script logic goes here...")


	def view_market_data(self):
		print("View Market Data logic goes here...")


	def initialize_market_data(self):
		print("Initialize Market Data logic goes here...")


	def initialize_all_asset_information_data(self):
		self.initialize_nasdaq_asset_information_data()
		self.initialize_nyse_asset_information_data()
		self.initialize_nyse_mkt_asset_information_data()
		self.initialize_nyse_arca_asset_information_data()
		self.initialize_bats_asset_information_data()
		self.initialize_tsx_asset_information_data()
		self.initialize_tsxv_asset_information_data()
		self.initialize_cse_asset_information_data()
		self.initialize_cboe_canada_asset_information_data()


	def __initialize_nasdaq_trader_market_listings(self, country_iso_code: str, exchange_name: str, exchange_acronym: str, exchange_in_url: str, exchange_filter: str | None) -> None:
		# Initialize the exchange listings object
		exchange_listings_extractor = ExchangeListingsExtractor(self.__database)
		# Initialize the exchange listings
		exchange_listings_extractor.initialize_nasdaq_trader_market_data(country_iso_code, exchange_name, exchange_acronym, exchange_in_url, exchange_filter)

		# Get the exchange listings
		df_exchange_listings_info = exchange_listings_extractor.get_exchange_listings_info_dataframe()
		if df_exchange_listings_info is None:
			raise Exception("Exchange listings info not initialized.")

		# Initialize the asset information
		asset_info_extractor = AssetInfoExtractor(self.__database)
		asset_info_extractor.initialize_asset_info(df_exchange_listings_info, exchange_acronym)

		# Print and log the success message
		print(f"{exchange_name} listings initialized successfully.")
		logging.info(f"{exchange_name} listings initialized successfully.")


	def initialize_nasdaq_asset_information_data(self):
		# Set the exchange variables
		country_iso_code = "USA"
		exchange_name = "NASDAQ Stock Exchange"
		exchange_acronym = "NASDAQ"
		exchange_in_url = "nasdaq"
		exchange_filter = None

		# Initialize the exchange listings
		self.__initialize_nasdaq_trader_market_listings(country_iso_code, exchange_name, exchange_acronym,
										   exchange_in_url, exchange_filter)


	def initialize_nyse_asset_information_data(self):
		# Set the exchange variables
		country_iso_code = "USA"
		exchange_name = "New York Stock Exchange"
		exchange_acronym = "NYSE"
		exchange_in_url = "other"
		exchange_filter = "N"

		# Initialize the exchange listings
		self.__initialize_nasdaq_trader_market_listings(country_iso_code, exchange_name, exchange_acronym,
										   exchange_in_url, exchange_filter)


	def initialize_nyse_mkt_asset_information_data(self):
		# Set the exchange variables
		country_iso_code = "USA"
		exchange_name = "NYSE American"
		exchange_acronym = "NYSE MKT"
		exchange_in_url = "other"
		exchange_filter = "A"

		# Initialize the exchange listings
		self.__initialize_nasdaq_trader_market_listings(country_iso_code, exchange_name, exchange_acronym,
										   exchange_in_url, exchange_filter)


	def initialize_nyse_arca_asset_information_data(self):
		# Set the exchange variables
		country_iso_code = "USA"
		exchange_name = "NYSE Arca"
		exchange_acronym = "NYSE ARCA"
		exchange_in_url = "other"
		exchange_filter = "P"

		# Initialize the exchange listings
		self.__initialize_nasdaq_trader_market_listings(country_iso_code, exchange_name, exchange_acronym,
										   exchange_in_url, exchange_filter)


	def initialize_bats_asset_information_data(self):
		# Set the exchange variables
		country_iso_code = "USA"
		exchange_name = "BATS Global Markets"
		exchange_acronym = "BATS"
		exchange_in_url = "other"
		exchange_filter = "Z"

		# Initialize the exchange listings
		self.__initialize_nasdaq_trader_market_listings(country_iso_code, exchange_name, exchange_acronym,
										   exchange_in_url, exchange_filter)


	def __initialize_cboe_canada_market_listings(self, country_iso_code: str, exchange_name: str, exchange_acronym: str, exchange_filter: str) -> None:
		# Initialize the exchange listings
		exchange_listings_extractor = ExchangeListingsExtractor(self.__database)
		# Initialize the exchange listings
		exchange_listings_extractor.initialize_cboe_canada_market_data(country_iso_code, exchange_name, exchange_acronym, exchange_filter)

		# Get the exchange listings
		df_exchange_listings_info = exchange_listings_extractor.get_exchange_listings_info_dataframe()
		if df_exchange_listings_info is None:
			raise Exception("Exchange listings info not initialized.")

		# Initialize the asset information
		asset_info_extractor = AssetInfoExtractor(self.__database)
		asset_info_extractor.initialize_asset_info(df_exchange_listings_info, exchange_acronym)

		# Print and log the success message
		print(f"{exchange_name} listings initialized successfully.")
		logging.info(f"{exchange_name} listings initialized successfully.")


	def initialize_tsx_asset_information_data(self):
		# Set the exchange variables
		country_iso_code = "CAN"
		exchange_name = "Toronto Stock Exchange"
		exchange_acronym = "TSX"
		exchange_filter = "XTSE"

		# Initialize the exchange listings
		self.__initialize_cboe_canada_market_listings(country_iso_code, exchange_name,
													 exchange_acronym, exchange_filter)


	def initialize_tsxv_asset_information_data(self):
		# Set the exchange variables
		country_iso_code = "CAN"
		exchange_name = "TSX Venture Exchange"
		exchange_acronym = "TSXV"
		exchange_filter = "XTSX"

		# Initialize the exchange listings
		self.__initialize_cboe_canada_market_listings(country_iso_code, exchange_name,
													 exchange_acronym, exchange_filter)


	def initialize_cse_asset_information_data(self):
		# Set the exchange variables
		country_iso_code = "CAN"
		exchange_name = "Canadian Securities Exchange"
		exchange_acronym = "CSE"
		exchange_filter = "XCNQ"

		# Initialize the exchange listings
		self.__initialize_cboe_canada_market_listings(country_iso_code, exchange_name,
													 exchange_acronym, exchange_filter)


	def initialize_cboe_canada_asset_information_data(self):
		# Set the exchange variables
		country_iso_code = "CAN"
		exchange_name = "Cboe Canada"
		exchange_acronym = "Cboe CA"
		exchange_filter = "NEOE"

		# Initialize the exchange listings
		self.__initialize_cboe_canada_market_listings(country_iso_code, exchange_name,
													 exchange_acronym, exchange_filter)


	def initialize_index_holdings_data(self):
		print("Initialize Index Holdings Data logic goes here...")


	def initialize_macro_data(self):
		print("Initialize Macro Data logic goes here...")


	def import_custom_market_data(self):
		print("Import Custom Market Data logic goes here...")


	def import_market_data_from_csv(self):
		print("Import Market Data from CSV logic goes here...")


	def import_market_data_from_excel(self):
		print("Import Market Data from Excel logic goes here...")


	def import_market_data_from_database(self):
		print("Import Market Data from Database logic goes here...")


	def import_market_data_from_api(self):
		print("Import Market Data from API logic goes here...")


	def import_market_data_from_online_source(self):
		print("Import Market Data from Online Source logic goes here...")


	def modify_market_data(self):
		print("Modify Market Data Entry logic goes here...")


	def modify_single_market_data_entry(self):
		print("Modify Single Market Data Entry logic goes here...")


	def modify_entire_market_data_column(self):
		print("Modify Entire Market Data Column logic goes here...")


	def modify_entire_market_data_table(self):
		print("Modify Entire Market Data Table logic goes here...")


	def portfolio_overview(self):
		print("Portfolio Overview logic goes here...")


	def performance_analysis(self):
		print("Performance Analysis logic goes here...")


	def risk_analysis(self):
		print("Risk Analysis logic goes here...")


	def correlation_analysis(self):
		print("Correlation Analysis logic goes here...")


	def portfolio_optimization(self):
		print("Portfolio Optimization logic goes here...")


	def portfolio_backtesting(self):
		print("Portfolio Backtesting logic goes here...")


	def portfolio_simulation(self):
		print("Portfolio Simulation logic goes here...")


	def portfolio_forecasting(self):
		print("Portfolio Forecasting logic goes here...")


	def portfolio_stress_testing(self):
		print("Portfolio Stress Testing logic goes here...")


	def current_trading_strategies(self):
		print("Current Trading Strategies logic goes here...")


	def add_trading_strategy(self):
		print("Add Trading Strategy logic goes here...")


	def modify_trading_strategy(self):
		print("Modify Trading Strategy logic goes here...")


	def remove_trading_strategy(self):
		print("Remove Trading Strategy logic goes here...")


	def view_current_reports(self):
		print("View Current Reports logic goes here...")


	def add_report(self):
		print("Add Report logic goes here...")


	def modify_report(self):
		print("Modify Report logic goes here...")


	def remove_report(self):
		print("Remove Report logic goes here...")


	def export_portfolio_data(self):
		print("Export Portfolio Data logic goes here...")


	def export_market_data(self):
		print("Export Market Data logic goes here...")


	def export_statistical_analysis(self):
		print("Export Statistical Analysis logic goes here...")


	def export_trading_strategies(self):
		print("Export Trading Strategies logic goes here...")


	def export_reports(self):
		print("Export Reports logic goes here...")


	def view_automations(self):
		print("View Automations logic goes here...")


	def add_automation(self):
		print("Add Automation logic goes here...")
		# TODO - Tradingview automated watchlist
		# OR jur auto export a watchlist text file of my current portfolio
		# choose between daily/wkly/mthly and diff the text, if different update and delete old watchlist text file
		# can import into tradingview manually whenver I'm ready to analyze the portfolio
		# Use ###Stock (section), NASDAQ:GOOGL, NEO:GOOG, etc for portfolio watchlist

	def modify_automation(self):
		print("Modify Automation logic goes here...")


	def remove_automation(self):
		print("Remove Automation logic goes here...")


	def view_notifications(self):
		print("View Notifications logic goes here...")


	def add_notification(self):
		print("Add Notification logic goes here...")


	def modify_notification(self):
		print("Modify Notification logic goes here...")


	def remove_notification(self):
		print("Remove Notification logic goes here...")


	def view_user_details(self):
		# Print the username
		user = self.__database.session_manager.get_current_user()
		if user is not None:
			print(user)
		else:
			print("No user details found.")
		# Print the user email accounts
		email_accounts = self.__database.query_executor.get_all_current_user_email_accounts()
		if email_accounts is not None:
			for email_account in email_accounts:
				print(email_account)


	def manage_email_accounts(self):
		print("Manage Email Accounts logic goes here...")


	def change_account_username(self):
		print("Change Account Username logic goes here...")


	def change_account_password(self):
		print("Change Account Password logic goes here...")


	def delete_account(self):
		print("Delete Account logic goes here...")


	def view_current_email_accounts(self):
		email_accounts = self.__database.query_executor.get_all_current_user_email_accounts()
		logging.debug(f"Current email accounts: {email_accounts}")
		if email_accounts is not None:
			for email_account in email_accounts:
				print(email_account)
		else:
			print("\nNo email accounts found.")


	def add_email_account(self):
		# TODO - make this function less hacky, and use the menu if possible
		title = "ADD EMAIL ACCOUNTS"
		print(f"\n{title}")
		print("-" * len(title))
		# Run through the prompts to get the email address and password
		try:
			self.__email_account_operation.add_email_account()
		except AuthenticationError as e:
			print(f"Error getting email usage by email address: {e.message}")
			logging.warning(f"Error getting email usage by email address. {e.message}")


	def remove_email_account(self):
		print("Remove Email Account logic goes here...")


	def view_user_manual(self):
		print("View User Manual logic goes here...")


	def view_faq(self):
		print("View FAQ logic goes here...")


	def view_glossary(self):
		print("View Glossary logic goes here...")


	def about(self):
		print("About logic goes here...")


	def contact_us(self):
		print("Contact Us logic goes here...")


	def report_bug(self):
		print("Report Bug logic goes here...")


	def request_feature(self):
		print("Request Feature logic goes here...")


	def view_license(self):
		print("View License logic goes here...")


if __name__ == "__main__":
	print("This module is not meant to be executed directly...")
