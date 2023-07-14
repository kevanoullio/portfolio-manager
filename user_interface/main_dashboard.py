# Purpose: Dashboard module for managing the user interface.

# Standard Libraries

# Third-party Libraries

# Local Modules
from session.session_manager import SessionManager
from user_interface.login_dashboard import LoginManager
from user_interface import menu

# Configure logging
import logging


# Dashboard class for managing the user interface
class MainDashboard:
    def __init__(self, session_manager: SessionManager, login_manager: LoginManager) -> None:
        self.session_manager = session_manager
        self.database = self.session_manager.database
        self.login_manager = login_manager
        self.main_menu = menu.Main(self.session_manager)
        self.portfolio_manager_menu = menu.PortfolioManager(self.session_manager)
        self.view_portfolio_menu = menu.ViewPortfolio(self.session_manager)
        self.manage_portfolio_menu = menu.ManagePortfolio(self.session_manager)
        self.import_existing_portfolio_menu = menu.ImportExistingPortfolio(self.session_manager)
        self.import_from_email_menu = menu.ImportFromEmail(self.session_manager)
        self.manage_custom_import_scripts_menu = menu.ManageCustomImportScripts(self.session_manager)
        self.custom_import_scripts_menu = menu.CustomImportScripts(self.session_manager)
        self.manage_market_data_menu = menu.ManageMarketData(self.session_manager)
        self.statistical_analysis_menu = menu.StatisticalAnalysis(self.session_manager)
        self.trading_strategies_menu = menu.TradingStrategies(self.session_manager)
        self.reports_menu = menu.Reports(self.session_manager)
        self.export_data_menu = menu.ExportData(self.session_manager)
        self.automation_menu = menu.Automation(self.session_manager)
        self.notifications_menu = menu.Notifications(self.session_manager)
        self.account_settings_menu = menu.AccountSettings(self.session_manager)
        self.help_and_information_menu = menu.HelpAndInformation(self.session_manager)


    def valid_input(self, choice: str, min_choice: int, max_choice: int) -> bool:
        if not choice.isdigit() or int(choice) < min_choice or int(choice) > max_choice:
            return False
        return True


    def run(self):
        self.session_manager.main_db_is_running = True
        logging.info("Main Dashboard has started running.")
        self.session_manager.start_session()
        self.handle_main_menu()


    def handle_main_menu(self):
        while self.session_manager.main_db_is_running:
            self.main_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 5):
                print("Invalid input. Please try again: ", end="")
                choice = input()
            
            choice = int(choice)
            if choice == 1:
                # Start the portfolio manager
                self.portfolio_manager_menu.is_active = True
                self.handle_portfolio_manager_menu()
            elif choice == 2:
                # Go to account settings
                self.account_settings_menu.is_active = True
                self.handle_account_settings_menu()
            elif choice == 3:
                # Display help menu
                self.help_and_information_menu.is_active = True
                self.handle_help_menu()
            elif choice == 4:
                # Save changes
                self.session_manager.save_changes()
            elif choice == 5:
                # Discard changes
                self.session_manager.discard_changes()
            elif choice == 0:
                # Log out the user and close the session
                self.login_manager.logout()
                self.session_manager.close_session()
                logging.info("Main Dashboard has stopped running.")
                self.session_manager.main_db_is_running = False


    def handle_portfolio_manager_menu(self):
        while self.portfolio_manager_menu.is_active:
            self.portfolio_manager_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 9):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                self.view_portfolio_menu.is_active = True
                self.handle_view_portfolio_menu()
            elif choice == 2:
                self.manage_portfolio_menu.is_active = True
                self.handle_manage_portfolio_menu()
            elif choice == 3:
                self.manage_market_data_menu.is_active = True
                self.handle_manage_market_data_menu()
            elif choice == 4:
                self.statistical_analysis_menu.is_active = True
                self.handle_statistical_analysis_menu()
            elif choice == 5:
                self.trading_strategies_menu.is_active = True
                self.handle_trading_strategies_menu()
            elif choice == 6:
                self.reports_menu.is_active = True
                self.handle_reports_menu()
            elif choice == 7:
                self.export_data_menu.is_active = True
                self.handle_export_data_menu()
            elif choice == 8:
                self.automation_menu.is_active = True
                self.handle_automation_menu()
            elif choice == 9:
                self.notifications_menu.is_active = True
                self.handle_notifications_menu()
            elif choice == 0:
                self.portfolio_manager_menu.is_active = False


    def handle_view_portfolio_menu(self):
        while self.view_portfolio_menu.is_active:
            self.view_portfolio_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 4):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for viewing current portfolio
                print("Viewing current portfolio...")
            elif choice == 2:
                # Code for viewing entire portfolio history
                print("Viewing entire portfolio history...")
            elif choice == 3:
                # Code to search for a current investment
                print("Searching for a current investment...")
            elif choice ==      4:
                # Get the ticker symbol of the investment to search for, ensure it's alphanumeric
                ticker = input("Enter the ticker symbol of the investment you would like to search for: ")
                while not ticker.isalnum():
                    print("Invalid ticker symbol. Please try again: ", end="")
                    ticker = input()
                # Execute the query to search for an investment in portfolio history
                self.database.execute_query_by_title("query_net_ticker_summary", ticker)
            elif choice == 0:
                self.view_portfolio_menu.is_active = False


    def handle_manage_portfolio_menu(self):
        while self.manage_portfolio_menu.is_active:
            self.manage_portfolio_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 6):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for building portfolio from data set(s)
                print("Building portfolio from data set(s)...")
            elif choice == 2:
                print("Importing existing portfolio data set...")
                self.import_existing_portfolio_menu.is_active = True
                self.handle_import_existing_portfolio_menu()
            elif choice == 3:
                print("Deleting existing portfolio data set...")
                # self.delete_existing_portfolio = True
                # self.handle_delete_existing_portfolio_menu()
            elif choice == 4:
                print("Managing custom import scripts...")
                self.custom_import_scripts = True
                self.handle_custom_import_scripts_menu()
            elif choice == 5:
                # Code for adding an investment manually
                print("Adding an investment manually...")
            elif choice == 6:
                # Code for modifying an investment entry
                print("Modifying an investment entry...")
            elif choice == 0:
                self.manage_portfolio_menu.is_active = False




    def handle_import_existing_portfolio_menu(self):
        while self.import_existing_portfolio_menu.is_active:
            self.import_existing_portfolio_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 6):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for importing from brokerage account
                print("Importing from Brokerage Account...")
            elif choice == 2:
                # Code for importing from CSV file
                print("Importing from CSV file...")
            elif choice == 3:
                # Code for importing from Excel file
                print("Importing from Excel file...")
            elif choice == 4:
                print("Importing from PDF file...")
                # self.import_from_pdf = True
                # self.handle_import_from_pdf_menu()
            elif choice == 5:
                print("Importing from Database file...")
                if self.session_manager.current_user is not None:
                    if self.session_manager.current_user.user_id is not None:
                        self.database.import_file(self.session_manager.current_user.user_id, "database", [".db"])
                else:
                    print("You must be logged in to import from a database file.")
            elif choice == 6:
                print("Importing from Email Account...")
                self.import_from_email_menu.is_active = True
                self.handle_import_from_email_menu()
            elif choice == 0:
                self.import_existing_portfolio_menu.is_active = False


    # def print_imported_email_accounts(self) -> int | None:
    #     if self.session_manager.current_user is None or self.session_manager.current_user.user_id is None:
    #         print("You must be logged in to view email accounts.")
    #         return None
    #     else:
    #         # Get the list of email accounts
    #         emails = self.database.query_executor.fetch_email_accounts(self.session_manager.current_user.user_id, "import_email_account")
    #         if emails is not None:
    #             print("\nCURRENT IMPORTED EMAIL ACCOUNTS:")
    #             # print("--------------------------------")
    #             for email in emails[0]:
    #                 print(f"{email}")
    #             return len(emails)
    #         else:
    #             print("No imported email accounts found.")
    #             return 0

    
    def handle_import_from_email_menu(self):
        while self.import_from_email_menu.is_active:
            # if self.session_manager.current_user is None or self.session_manager.current_user.user_id is None:
            #     print("You must be logged in to view email accounts.")
            #     self.import_from_email_menu.is_active = False
            # else:
            self.import_from_email_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 3):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                print("Viewing email accounts...")
                # self.print_imported_email_accounts()
            elif choice == 2:
                print("Adding an email account...")
                # self.user_authentication.query_executor.import_email_account(self.database, "import_email_account")
            elif choice == 3:
                # Code for removing an email account
                print("Removing an email account...")
                # self.print_imported_email_accounts()
                # self.user_authentication.query_executor.remove_email_account(self.database, "import_email_account")
            elif choice == 0:
                self.import_from_email_menu.is_active = False


    def handle_custom_import_scripts_menu(self):
        while self.custom_import_scripts_menu.is_active:
            self.custom_import_scripts_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 3):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                if self.custom_import_scripts_menu.number_of_options > 1:
                    # self.custom_imported_scripts = True
                    # self.handle_custom_imported_scripts_menu()
                    pass
                else:
                    print("No custom import scripts to view/run.")
            elif choice == 2:
                # Code for adding a custom import script
                print("Adding a custom import script...")
                # TODO rewrite using new import_file function
                self.database.import_custom_script(self.custom_import_scripts_menu.options)

            elif choice == 3:
                # Code for removing a custom import script
                print("Removing a custom import script...")
            elif choice == 0:
                self.custom_import_scripts_menu.is_active = False



    # def handle_custom_imported_scripts_menu(self):
    #     while self.custom_import_scripts_menu.is_active:
    #         self.custom_import_scripts_menu.print()
    #         choice = input("\nPlease choose a custom script to run: ")
    #         # Check if the input is valid
    #         while not self.valid_input(choice, 0, self.custom_import_scripts_menu.number_of_options - 1):
    #             print("Invalid input. Please try again: ", end="")
    #             choice = input()

    #         choice = int(choice)
    #         if self.custom_import_scripts_menu.number_of_options > 1 and choice != 0:
    #             for i in range(1, self.custom_import_scripts_menu.number_of_options):
    #                 if choice == i:
    #                     # Code for running the custom script
    #                     print(f"Running {self.custom_import_scripts_menu.options[i]}...")
    #         elif choice == 0:
    #             self.custom_import_scripts_menu.is_active = False
                

    def handle_manage_market_data_menu(self):
        while self.manage_market_data_menu.is_active:
            self.manage_market_data_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 6):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for importing from CSV
                print("Importing from CSV...")
            elif choice == 2:
                # Code for importing from Excel
                print("Importing from Excel...")
            elif choice == 3:
                # Code for importing from an API
                print("Importing from an API...")
            elif choice == 4:
                # Code for importing from online source
                print("Importing from online source...")
            elif choice == 5:
                # Code for adding a security manually
                print("Adding a security manually...")
            elif choice == 6:
                # Code for modifying a security entry
                print("Modifying a security entry...")
            elif choice == 0:
                self.manage_market_data_menu.is_active = False


    def handle_statistical_analysis_menu(self):
        while self.statistical_analysis_menu.is_active:
            self.statistical_analysis_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 9):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for portfolio details
                print("Portfolio Details...")
            elif choice == 2:
                # Code for performance analysis
                print("Performance Analysis...")
            elif choice == 3:
                # Code for risk analysis
                print("Risk Analysis...")
            elif choice == 4:
                # Code for correlation analysis
                print("Correlation Analysis...")
            elif choice == 5:
                # Code for portfolio optimization
                print("Portfolio Optimization...")
            elif choice == 6:
                # Code for portfolio backtesting
                print("Portfolio Backtesting...")
            elif choice == 7:
                # Code for portfolio simulation
                print("Portfolio Simulation...")
            elif choice == 8:
                # Code for portfolio forecasting
                print("Portfolio Forecasting...")
            elif choice == 9:
                # Code for portfolio stress testing
                print("Portfolio Stress Testing...")
            elif choice == 0:
                self.statistical_analysis_menu.is_active = False


    def handle_trading_strategies_menu(self):
        while self.trading_strategies_menu.is_active:
            self.trading_strategies_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 4):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for viewing current trading strategies
                print("Viewing current trading strategies...")
            elif choice == 2:
                # Code for adding a trading strategy
                print("Adding a trading strategy...")
            elif choice == 3:
                # Code for modifying a trading strategy
                print("Modifying a trading strategy...")
            elif choice == 4:
                # Code for removing a trading strategy
                print("Removing a trading strategy...")
            elif choice == 0:
                self.trading_strategies_menu.is_active = False


    def handle_reports_menu(self):
        while self.reports_menu.is_active:
            self.reports_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 4):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for viewing current reports
                print("Viewing current reports...")
            elif choice == 2:
                # Code for adding a report
                print("Adding a report...")
            elif choice == 3:
                # Code for modifying a report
                print("Modifying a report...")
            elif choice == 4:
                # Code for removing a report
                print("Removing a report...")
            elif choice == 0:
                self.reports_menu.is_active = False

    
    def handle_export_data_menu(self):
        while self.export_data_menu.is_active:
            self.export_data_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 5):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for exporting portfolio data
                print("Exporting portfolio data...")
            elif choice == 2:
                # Code for exporting market data
                print("Exporting market data...")
            elif choice == 3:
                # Code for exporting statistical analysis
                print("Exporting statistical analysis...")
            elif choice == 4:
                # Code for exporting trading strategies
                print("Exporting trading strategies...")
            elif choice == 5:
                # Code for exporting reports
                print("Exporting reports...")
            elif choice == 0:
                self.export_data_menu.is_active = False
    
    
    def handle_automation_menu(self):
        while self.automation_menu.is_active:
            self.automation_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 4):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for viewing current automations
                print("Viewing current automations...")
            elif choice == 2:
                # Code for adding an automation
                print("Adding an automation...")
            elif choice == 3:
                # Code for modifying an automation
                print("Modifying an automation...")
            elif choice == 4:
                # Code for removing an automation
                print("Removing an automation...")
            elif choice == 0:
                self.automation_menu.is_active = False


    def handle_notifications_menu(self):
        while self.notifications_menu.is_active:
            self.notifications_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 4):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for viewing current notifications
                print("Viewing current notifications...")
            elif choice == 2:
                # Code for adding a notification
                print("Adding a notification...")
            elif choice == 3:
                # Code for modifying a notification
                print("Modifying a notification...")
            elif choice == 4:
                # Code for removing a notification
                print("Removing a notification...")
            elif choice == 0:
                self.notifications_menu.is_active = False
        

    def handle_account_settings_menu(self):
        while self.account_settings_menu.is_active:
            self.account_settings_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 4):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for viewing account details
                print("Viewing account details...")
            elif choice == 2:
                # Code for changing username
                print("Changing username...")
            elif choice == 3:
                # Code for changing password
                print("Changing password...")
            elif choice == 4:
                # Code for deleting account
                print("Deleting account...")
            elif choice == 0:
                self.account_settings_menu.is_active = False
    

    def handle_help_menu(self):
        while self.help_and_information_menu.is_active:
            self.help_and_information_menu.print()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 8):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for viewing the user manual
                print("Viewing the user manual...")
            elif choice == 2:
                # Code for viewing the FAQ
                print("Viewing the FAQ...")
            elif choice == 3:
                # Code for viewing the glossary
                print("Viewing the glossary...")
            elif choice == 4:
                # Code for viewing the about page
                print("Viewing the about page...")
            elif choice == 5:
                # Code for viewing the contact page
                print("Viewing the contact page...")
            elif choice == 6:
                # Code for reporting a bug
                print("Reporting a bug...")
            elif choice == 7:
                # Code for requesting a feature
                print("Requesting a feature...")
            elif choice == 8:
                # Code for viewing the license
                print("Viewing the license...")
            elif choice == 0:
                self.help_and_information_menu.is_active = False


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
