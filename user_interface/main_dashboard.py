# Purpose: Dashboard module for managing the user interface.

# Standard Libraries

# Third-party Libraries

# Local Modules
from session.session_manager import SessionManager
from user_interface.login_dashboard import LoginManager

# Configure logging
import logging
from config import configure_logging
configure_logging()


# Dashboard class for managing the user interface
class MainDashboard:
    def __init__(self, session_manager: SessionManager, login_manager: LoginManager) -> None:
        self.session_manager = session_manager
        self.database = self.session_manager.database
        self.login_manager = login_manager
        self.portfolio_manager = False
        self.view_portfolio = False
        self.manage_portfolio = False
        self.import_existing_portfolio = False
        self.import_from_email = False
        self.custom_import_scripts = False
        self.custom_imported_scripts = False
        self.manage_market_data = False
        self.statistical_analysis = False
        self.trading_strategies = False
        self.reports = False
        self.export_data = False
        self.automation = False
        self.notifications = False
        self.account_settings = False
        self.help = False
        self.logout = False
        self.exit = False


    def valid_input(self, choice: str, min_choice: int, max_choice: int) -> bool:
        if not choice.isdigit() or int(choice) < min_choice or int(choice) > max_choice:
            return False
        return True


    def run(self):
        logging.info("Main Dashboard has started running.")
        self.session_manager.main_db_is_running = True
        self.handle_main_menu()


    def print_main_menu(self):
        print("\nMAIN MENU")
        print("----------")
        print("1. Portfolio Manager")
        print("2. Account Settings")
        print("3. Save Changes")
        print("4. Discard Changes")
        print("5. Log out")
        print("6. Help")
        print("0. Exit")


    def handle_main_menu(self):
        while self.session_manager.logged_in:
            self.print_main_menu()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 6):
                print("Invalid input. Please try again: ", end="")
                choice = input()
            
            choice = int(choice)
            if choice == 1:
                # Start the portfolio manager
                self.portfolio_manager = True
                self.handle_portfolio_manager_menu()
            elif choice == 2:
                # Go to account settings
                self.account_settings = True
                self.handle_account_settings_menu()
            elif choice == 3:
                # Code for saving changes
                print("Portfolio saved!")
            elif choice == 4:
                # Code for discarding changes
                print("Most recent Portfolio changes discarded!")
            elif choice == 5:
                # Log out the user
                self.login_manager.logout()
            elif choice == 6:
                self.help = True
                self.handle_help_menu()
            elif choice == 0:
                # Log out the user
                self.session_manager.main_db_is_running = False
                self.login_manager.logout()


    def print_portfolio_manager_menu(self):
        print("\nPORTFOLIO MANAGER")
        print("------------------")
        print("1. View Portfolio")
        print("2. Manage Portfolio")
        print("3. Market Data")
        print("4. Statistical Analysis")
        print("5. Trading Strategies")
        print("6. Reports")
        print("7. Export Data")
        print("8. Automation")
        print("9. Notifications")
        print("0. Return to Main Menu")


    def handle_portfolio_manager_menu(self):
        while self.portfolio_manager:
            self.print_portfolio_manager_menu()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 9):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                self.view_portfolio = True
                self.handle_view_portfolio_menu()
            elif choice == 2:
                self.manage_portfolio = True
                self.handle_manage_portfolio_menu()
            elif choice == 3:
                self.manage_market_data = True
                self.handle_manage_market_data_menu()
            elif choice == 4:
                self.statistical_analysis = True
                self.handle_statistical_analysis_menu()
            elif choice == 5:
                self.trading_strategies = True
                self.handle_trading_strategies_menu()
            elif choice == 6:
                self.reports = True
                self.handle_reports_menu()
            elif choice == 7:
                self.export_data = True
                self.handle_export_data_menu()
            elif choice == 8:
                self.automation = True
                self.handle_automation_menu()
            elif choice == 9:
                self.notifications = True
                self.handle_notifications_menu()
            elif choice == 0:
                self.portfolio_manager = False


    def print_view_portfolio_menu(self):
        print("\nVIEW PORTFOLIO")
        print("---------------")
        print("1. View Current Portfolio")
        print("2. View Entire Portfolio History")
        print("3. Search for A Current Investment")
        print("4. Search for An Investment in Portfolio History")
        print("0. Return to Portfolio Manager Menu")


    def handle_view_portfolio_menu(self):
        while self.view_portfolio:
            self.print_view_portfolio_menu()
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
                self.view_portfolio = False


    def print_manage_portfolio_menu(self):
        print("\nMANAGE PORTFOLIO")
        print("-----------------")
        print("1. Build Portfolio from Data Set(s)")
        print("2. Import Existing Portfolio Data Set")
        print("3. Delete Existing Portfolio Data Set")
        print("4. Manage Custom Import Scripts")
        print("5. Add An Investment Manually")
        print("6. Modify An Investment Entry")
        print("0. Return to Portfolio Manager Menu")


    def handle_manage_portfolio_menu(self):
        while self.manage_portfolio:
            self.print_manage_portfolio_menu()
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
                self.import_existing_portfolio = True
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
                self.manage_portfolio = False


    def print_import_existing_portfolio_menu(self):
        print("\nIMPORT EXISTING PORTFOLIO")
        print("--------------------------")
        print("1. Import Existing Portfolio from Brokerage Account")
        print("2. Import Existing Portfolio from CSV File")
        print("3. Import Existing Portfolio from Excel File")
        print("4. Import Existing Portfolio from PDF file")
        print("5. Import Existing Portfolio from Database file")
        print("6. Import Existing Portfolio from Email Account")
        print("0. Return to Manage Portfolio Menu")


    def handle_import_existing_portfolio_menu(self):
        while self.import_existing_portfolio:
            self.print_import_existing_portfolio_menu()
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
                self.import_from_email = True
                self.handle_import_from_email_menu()
            elif choice == 0:
                self.import_existing_portfolio = False


    def print_imported_email_accounts(self) -> int | None:
        if self.session_manager.current_user is None or self.session_manager.current_user.user_id is None:
            print("You must be logged in to view email accounts.")
            return None
        else:
            # Get the list of email accounts
            emails = self.database.query_executor.fetch_email_accounts(self.session_manager.current_user.user_id, "import_email_account")
            if emails is not None:
                print("\nCURRENT IMPORTED EMAIL ACCOUNTS:")
                # print("--------------------------------")
                for email in emails:
                    print(f"{email}")
                return len(emails)
            else:
                print("No imported email accounts found.")
                return 0


    def print_import_from_email_menu(self):
        print("\nIMPORT FROM EMAIL ACCOUNT")
        print("--------------------------")
        print("1. View Imported Email Accounts")
        print("2. Add Email Account")
        print("3. Remove Email Account")
        print("0. Return to Manage Portfolio Menu")

    
    def handle_import_from_email_menu(self):
        while self.import_from_email:
            if self.session_manager.current_user is None or self.session_manager.current_user.user_id is None:
                print("You must be logged in to view email accounts.")
                self.import_from_email = False
            else:
                # Print the menu
                self.print_import_from_email_menu()
                choice = input("\nPlease enter your choice: ")
                # Check if the input is valid
                while not self.valid_input(choice, 0, 3):
                    print("Invalid input. Please try again: ", end="")
                    choice = input()

                choice = int(choice)
                if choice == 1:
                    print("Viewing email accounts...")
                    self.print_imported_email_accounts()
                elif choice == 2:
                    print("Adding an email account...")
                    # self.user_authentication.query_executor.import_email_account(self.database, "import_email_account")
                elif choice == 3:
                    # Code for removing an email account
                    print("Removing an email account...")
                    self.print_imported_email_accounts()
                    # self.user_authentication.query_executor.remove_email_account(self.database, "import_email_account")
                elif choice == 0:
                    self.import_from_email = False


    def print_custom_import_scripts_menu(self):
        print("\nMANAGE CUSTOM IMPORT SCRIPTS")
        print("-----------------------------")
        print("1. View/Run Custom Import Scripts")
        print("2. Add Custom Import Script")
        print("3. Remove Custom Import Script")
        print("0. Return to Manage Portfolio Menu")


    def handle_custom_import_scripts_menu(self):
        while self.custom_import_scripts:
            self.print_custom_import_scripts_menu()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 3):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                if len(self.custom_imported_scripts_menu) > 1:
                    self.custom_imported_scripts = True
                    self.handle_custom_imported_scripts_menu()
                else:
                    print("No custom import scripts to view/run.")
            elif choice == 2:
                # Code for adding a custom import script
                print("Adding a custom import script...")
                # TODO rewrite using new import_file function
                self.database.import_custom_script(self.custom_imported_scripts_menu)

            elif choice == 3:
                # Code for removing a custom import script
                print("Removing a custom import script...")
            elif choice == 0:
                self.custom_import_scripts = False


    # Dynamic menu of imported custom scripts
    custom_imported_scripts_menu = [
        "0. Return to Custom Import Scripts Menu"
    ]


    def print_custom_imported_scripts_menu(self):
        print("\nCUSTOM IMPORTED SCRIPTS")
        print("------------------------")
        for i in range(1, len(self.custom_imported_scripts_menu)):
            print(f"{i}. {self.custom_imported_scripts_menu[i]}")
        print(self.custom_imported_scripts_menu[0])


    def handle_custom_imported_scripts_menu(self):
        while self.custom_imported_scripts:
            self.print_custom_imported_scripts_menu()
            choice = input("\nPlease choose a custom script to run: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, len(self.custom_imported_scripts_menu) - 1):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if len(self.custom_imported_scripts_menu) > 1 and choice != 0:
                for i in range(1, len(self.custom_imported_scripts_menu)):
                    if choice == i:
                        # Code for running the custom script
                        print(f"Running {self.custom_imported_scripts_menu[i]}...")
            elif choice == 0:
                self.custom_imported_scripts = False
                

    def print_manage_market_data_menu(self):
        print("\nMARKET DATA")
        print("------------")
        print("1. Import Market Data from CSV")
        print("2. Import Market Data from Excel")
        print("3. Import Market Data from an API")
        print("4. Import Market Data from Online Source")
        print("5. Add A Security Manually")
        print("6. Modify A Security Entry")
        print("0. Return to Portfolio Manager Menu")


    def handle_manage_market_data_menu(self):
        while self.manage_market_data:
            self.print_manage_market_data_menu()
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
                self.manage_market_data = False


    def print_statistical_analysis_menu(self):
        print("\nSTATISTICAL ANALYSIS")
        print("---------------------")
        print("1. Portfolio Details")
        print("2. Performance Analysis") # CAGR, Annualized Return, Annualized Volatility, Annualized Sharpe Ratio, Annualized Sortino Ratio, Annualized Treynor Ratio, Annualized Jensen's Alpha, Annualized Information Ratio, Annualized Tracking Error, Annualized Value at Risk, Annualized Conditional Value at Risk
        print("3. Risk Analysis") # Beta, Alpha, R-Squared, Sharpe Ratio, Sortino Ratio, Treynor Ratio, Jensen's Alpha, Information Ratio, Tracking Error, Value at Risk, Conditional Value at Risk
        print("4. Correlation Analysis") # Correlation Matrix
        print("5. Portfolio Optimization") # Markowitz
        print("6. Portfolio Backtesting") # Sharpe Ratio
        print("7. Portfolio Simulation") # Monte Carlo Simulation
        print("8. Portfolio Forecasting") # ARIMA
        print("9. Portfolio Stress Testing") # VaR
        # print("10. Custom Analysis") # Another menu with a list of custom analysis
        print("0. Return to Portfolio Manager Menu")


    # def statistical_analysis_menu(self) -> int:
    #     print("\nStatistical Analysis...")
    #     print("1. View Current Statistical Analysis")
    #     print("2. Add A Statistical Analysis")
    #     print("3. Modify A Statistical Analysis")
    #     print("4. Remove A Statistical Analysis")
    #     print("0. Return to Portfolio Manager Menu")
    #     print("\nPlease enter your choice: ", end="")
    #     choice = input()
    #     # Check if the input is valid
    #     while not self.valid_input(choice, 0, 4):
    #         print("Invalid input. Please try again: ", end="")
    #         choice = input()
    #     return int(choice)


    def handle_statistical_analysis_menu(self):
        while self.statistical_analysis:
            self.print_statistical_analysis_menu()
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
                self.statistical_analysis = False


    def print_trading_strategies_menu(self):
        print("\nTRADING STRATEGIES")
        print("-------------------")
        print("1. View Current Trading Strategies")
        print("2. Add A Trading Strategy")
        print("3. Modify A Trading Strategy")
        print("4. Remove A Trading Strategy")
        print("0. Return to Portfolio Manager Menu")


    def handle_trading_strategies_menu(self):
        while self.trading_strategies:
            self.print_trading_strategies_menu()
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
                self.trading_strategies = False


    def print_reports_menu(self):
        print("\nREPORTS")
        print("--------")
        print("1. View Current Reports")
        print("2. Add A Report")
        print("3. Modify A Report")
        print("4. Remove A Report")
        print("0. Return to Portfolio Manager Menu")


    def handle_reports_menu(self):
        while self.reports:
            self.print_reports_menu()
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
                self.reports = False


    def print_export_data_menu(self):
        print("\nEXPORT DATA")
        print("------------")
        print("1. Export Portfolio Data")
        print("2. Export Market Data")
        print("3. Export Statistical Analysis")
        print("4. Export Trading Strategies")
        print("5. Export Reports")
        print("0. Return to Portfolio Manager Menu")

    
    def handle_export_data_menu(self):
        while self.export_data:
            self.print_export_data_menu()
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
                self.export_data = False
    

    def print_automation_menu(self):
        print("\nAUTOMATION")
        print("-----------")
        print("1. View Current Automations")
        print("2. Add An Automation")
        print("3. Modify An Automation")
        print("4. Remove An Automation")
        print("0. Return to Portfolio Manager Menu")

    
    def handle_automation_menu(self):
        while self.automation:
            self.print_automation_menu()
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
                self.automation = False


    def print_notifications_menu(self):
        print("\nNOTIFICATIONS")
        print("--------------")
        print("1. View Current Notifications")
        print("2. Add A Notification")
        print("3. Modify A Notification")
        print("4. Remove A Notification")
        print("0. Return to Portfolio Manager Menu")


    def handle_notifications_menu(self):
        while self.notifications:
            self.print_notifications_menu()
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
                self.notifications = False


    def print_account_settings_menu(self):
        print("\nACCOUNT SETTINGS")
        print("-----------------")
        print("1. View Account Details")
        print("2. Change Username")
        print("3. Change Password")
        print("4. Delete Account")
        print("0. Return to Main Menu")
        

    def handle_account_settings_menu(self):
        while self.account_settings:
            self.print_account_settings_menu()
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
                self.account_settings = False
    

    def print_help_menu(self):
        print("\nHELP")
        print("-----")
        print("1. User Manual")
        print("2. FAQ")
        print("3. Glossary")
        print("4. About")
        print("5. Contact Us")
        print("6. Report A Bug")
        print("7. Request A Feature")
        print("8. View the License")
        print("0. Return to Main Menu")


    def handle_help_menu(self):
        while self.help:
            self.print_help_menu()
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
                self.help = False


    def print_logout_menu(self):
        print("\nLOGOUT")
        print("-------")
        print("1. Save and Logout")
        print("2. Discard and Logout")
        print("0. Return to Main Menu")


    def handle_logout_menu(self):
        while self.logout:
            self.print_logout_menu()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 2):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for saving and logging out
                print("Saving and logging out...")
            elif choice == 2:
                # Code for discarding and logging out
                print("Discarding and logging out...")
            elif choice == 0:
                self.logout = False


    def print_exit_menu(self):
        print("\nEXIT")
        print("-----")
        print("1. Save and Exit")
        print("2. Discard and Exit")
        print("0. Return to Main Menu")

    
    def handle_exit_menu(self):
        while self.exit:
            self.print_exit_menu()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 2):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                # Code for saving and exiting
                print("Saving and exiting...")
            elif choice == 2:
                # Code for discarding and exiting
                print("Discarding and exiting...")
            elif choice == 0:
                self.exit = False


if __name__ == "__main__":
    pass
