# Purpose: Dashboard module for managing the user interface and all menu navigation.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries

# Local Modules
from account_management.account_operations import UserAccountOperation, EmailAccountOperation
from access_management.login_manager import LoginManager
from database_management.database import Database
from user_interface.query_results import QueryResults

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from account_management.accounts import UserAccount, EmailAccount

# Configure logging
import logging


# Dashboard class for managing the user interface and all menu navigation
class Dashboard:
    def __init__(self, database: Database, login_manager: LoginManager) -> None:
        self.database = database
        self.login_manager = login_manager
        self.query_results = QueryResults()
        self.is_running = False
 
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
        while self.current_menu and self.is_running:
            # Print the menu options
            self.current_menu.print_options()
            # Get the user's choice
            choice = self.current_menu.get_valid_input()
            # Print the choice message
            self.current_menu.print_choice_msg(choice)

            next_menu = self.current_menu.menu_logic.get(choice)
            if next_menu:
                # Run the menu logic which executes the coresponding dashboard function based on user's choice
                next_menu()
                if self.login_manager.session_manager.get_current_user() is not None:
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

    # Login Menu Functions
    def create_account(self):
        self.login_manager.create_account()
        if self.login_manager.session_manager.get_current_user() is not None:
            logging.debug(f"User login: {self.login_manager.session_manager.get_current_user()}")
        else:
            logging.debug("User login failed.")

    def login(self):
        self.login_manager.login()

    def start_program(self):
        # Start the Dashboard
        self.is_running = True
        logging.info("Dashboard has started running.")

    def exit_program(self):
        # Stop the Dashboard
        self.is_running = False
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
        self.login_manager.logout()


    def view_portfolio(self):
        print("View Portfolio logic goes here...")

    
    def manage_portfolio(self):
        logging.info("Managing portfolio...")


    def market_data(self):
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

    
    def view_current_portfolio(self):
        # TODO - review and finish this function
        results = self.database.query_executor.execute_query_by_title("view_current_portfolio")
        self.query_results.print(results)
    

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
        self.database.query_executor.execute_query_by_title("query_net_ticker_summary", ticker)


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
        current_user = self.login_manager.session_manager.get_current_user() 
        # if current_user is not None:
        #     if current_user.user_id is not None:
        #         # self.database.import_file(current_user.user_id, "database", [".db"])
        # else:
        #     print("You must be logged in to import from a database file.")


    def import_existing_portfolio_from_email_account(self):
        logging.info("Importing existing portfolio from email account...")
        # TODO - finish this function
        # Get the user's email accounts
        email_accounts: list[EmailAccount] | None = self.database.query_executor.get_user_email_accounts_by_usage("import")


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


    def import_market_data_from_csv(self):
        print("Import Market Data from CSV logic goes here...")

    
    def import_market_data_from_excel(self):
        print("Import Market Data from Excel logic goes here...")

    
    def import_market_data_from_api(self):
        print("Import Market Data from API logic goes here...")
    

    def import_market_data_from_online_source(self):
        print("Import Market Data from Online Source logic goes here...")


    def modify_market_data_entry(self):
        print("Modify Market Data Entry logic goes here...")


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
        # TODO - Tradingview automated watchlist via Selenium and AutoIt Python packages
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
        print("View User Details logic goes here...")
    

    def manage_email_accounts(self):
        print("Manage Email Accounts logic goes here...")
    
    
    def change_account_username(self):
        print("Change Account Username logic goes here...")

    
    def change_account_password(self):
        print("Change Account Password logic goes here...")

    
    def delete_account(self):
        print("Delete Account logic goes here...")


    def view_current_email_accounts(self):
        print("View Current Email Accounts logic goes here...")
    

    def add_email_account(self):
        print("Add Email Account logic goes here...")
    

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
