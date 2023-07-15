# Purpose: Dashboard module for managing the user interface and all menu navigation.

# Standard Libraries

# Third-party Libraries

# Local Modules
from session.session_manager import SessionManager
from user_authentication.authentication import Authentication
from user_authentication.login_manager import LoginManager

# Configure logging
import logging


# Dashboard class for managing the user interface and all menu navigation
class Dashboard:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager
        self.user_authentication = Authentication(self.session_manager)
        self.login_manager = LoginManager(self.session_manager)
    

    def __print_welcome_screen(self):
        print("\n====================================")
        print("|| Welcome to 'PORTFOLIO MANAGER' ||")
        print("====================================")


    def run(self):
        # Start the session
        self.session_manager.start_session()

        # Import the Login menu here to avoid circular import
        from user_interface.menu import Login
        self.current_menu = Login(self)
        # self.session_manager.db_is_running = True
        logging.info("Login Dashboard has started running.")
        self.__print_welcome_screen()

        # Main loop for the dashboard
        while self.current_menu:
            self.current_menu.print_options()
            choice = self.current_menu.get_valid_input()

            next_menu = self.current_menu.menu_logic.get(choice)
            if next_menu:
                # Run the menu logic which executes the coresponding dashboard function based on user's choice
                next_menu()
                if self.session_manager.logged_in:
                    self.current_menu = self.current_menu.get_next_menu(choice)
                else:
                    self.current_menu = Login(self)
                    continue
            else:
                self.current_menu = None


    def previous_menu(self):
        pass


    def create_account(self):
        self.login_manager.create_account()
        if self.session_manager.current_user is not None:
            logging.debug(f"User login: {self.session_manager.current_user}")
        else:
            logging.debug("User login failed.")


    def login(self):
        self.login_manager.login()
        if self.session_manager.current_user is not None:
            logging.debug(f"User login: {self.session_manager.current_user.username}")
        else:
            logging.debug("User login failed.")


    def exit_program(self):
        self.session_manager.exit_program()


    def portfolio_manager(self):
        print("Portfolio Manager logic goes here...")


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
        self.session_manager.close_session()
        logging.info("Main Dashboard has stopped running.")


    def view_portfolio(self):
        print("View Portfolio logic goes here...")

    
    def manage_portfolio(self):
        print("Manage Portfolio logic goes here...")


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
        print("View Current Portfolio logic goes here...")
    

    def view_entire_portfolio_history(self):
        print("View Entire Portfolio History logic goes here...")

    
    def search_for_current_investment(self):
        print("Search for Current Investment logic goes here...")


    def search_for_investment_in_portfolio_history(self):
        print("Search for Investment in Portfolio History logic goes here...")


    def build_portfolio_from_data_set(self):
        print("Build Portfolio from Data Set logic goes here...")
    

    def import_existing_portfolio_data_set(self):
        print("Import Existing Portfolio Data Set logic goes here...")

    
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
        print("Import Existing Portfolio from Database File logic goes here...")

    
    def import_existing_portfolio_from_email_account(self):
        print("Import Existing Portfolio from Email Account logic goes here...")


    def view_custom_import_scripts(self):
        print("View Custom Import Scripts logic goes here...")

    
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
