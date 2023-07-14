# Purpose: Menu module for managing menu related functions.

# Standard Libraries

# Third-party Libraries

# Local Modules
from session.session_manager import SessionManager

# Configure logging
import logging


# Menu class for managing menu related functions
class Menu:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager
        self.is_active = False
        self.title = ""
        self.number_of_options = 0
        self.options = {}


    def print(self) -> None:
        print(f"\n{self.title.upper()}")
        print("-" * len(self.title))
        for key, value in self.options.items():
            print(f"{key}. {value}")


    def add_option(self, value: str) -> None:
        self.options[self.number_of_options] = value
        self.number_of_options += 1


    def remove_option(self, key: int) -> None:
        if key in self.options:
            del self.options[key]
            self.number_of_options -= 1
        else:
            logging.warning(f"Option {key} does not exist.")



# Login Menu class for managing the login menu
class Login(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "LOGIN MENU"
        self.number_of_options = 3
        self.options = {
            1: "Create an account",
            2: "Log into account",
            0: "Exit"
        }


# Main Menu class for managing the main menu
class Main(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "MAIN MENU"
        self.number_of_options = 6
        self.options = {
            1: "Portfolio Manager",
            2: "Account Settings",
            3: "Help and Information",
            4: "Save Changes",
            5: "Discard Changes",
            0: "Log Out"
        }


# PortfolioManager Menu class for managing the portfolio manager menu
class PortfolioManager(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "PORTFOLIO MANAGER"
        self.number_of_options = 10
        self.options = {
            1: "View Portfolio",
            2: "Manage Portfolio",
            3: "Market Data",
            4: "Statistical Analysis",
            5: "Trading Strategies",
            6: "Reports",
            7: "Export Data",
            8: "Automation",
            9: "Notifications",
            0: "Return to Main Menu"
        }


# ViewPortfolio Menu class for managing the view portfolio menu
class ViewPortfolio(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "VIEW PORTFOLIO"
        self.number_of_options = 4
        self.options = {
            1: "View Current Portfolio",
            2: "View Entire Portfolio History",
            3: "Search for A Current Investment",
            4: "Search for An Investment in Portfolio History",
            0: "Return to Portfolio Manager Menu"
        }


# ManagePortfolio Menu class for managing the manage portfolio menu
class ManagePortfolio(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "MANAGE PORTFOLIO"
        self.number_of_options = 6
        self.options = {
            1: "Build Portfolio from Data Set(s)",
            2: "Import Existing Portfolio Data Set",
            3: "Delete Existing Portfolio Data Set",
            4: "Manage Custom Import Scripts",
            5: "Add An Investment Manually",
            6: "Modify An Investment Entry",
            0: "Return to Portfolio Manager Menu"
        }


# ImportExistingPortfolio Menu class for managing the import existing portfolio menu
class ImportExistingPortfolio(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "IMPORT EXISTING PORTFOLIO"
        self.number_of_options = 7
        self.options = {
            1: "Import Existing Portfolio from Brokerage Account",
            2: "Import Existing Portfolio from CSV File",
            3: "Import Existing Portfolio from Excel File",
            4: "Import Existing Portfolio from PDF file",
            5: "Import Existing Portfolio from Database file",
            6: "Import Existing Portfolio from Email Account",
            0: "Return to Manage Portfolio Menu"
        }


# ImportFromEmail Menu class for managing the import from email menu
class ImportFromEmail(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "IMPORT FROM EMAIL ACCOUNT"
        self.number_of_options = 4
        self.options = {
            1: "View Imported Email Accounts",
            2: "Add Email Account",
            3: "Remove Email Account",
            0: "Return to Manage Portfolio Menu"
        }


# ManageCustomImportScripts Menu class for managing the manage custom import scripts menu
class ManageCustomImportScripts(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "MANAGE CUSTOM IMPORT SCRIPTS"
        self.number_of_options = 4
        self.options = {
            1: "View/Run Custom Import Scripts",
            2: "Add Custom Import Script",
            3: "Remove Custom Import Script",
            0: "Return to Manage Portfolio Menu"
        }


# CustomImportScripts Menu class for managing the custom import scripts menu
class CustomImportScripts(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "CUSTOM IMPORT SCRIPTS"
        self.number_of_options = 1
        self.options = {
            0: "Return to Manage Custom Import Scripts Menu"
        }


# ManageMarketData Menu class for managing the manage market data menu
class ManageMarketData(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "MANAGE MARKET DATA"
        self.number_of_options = 7
        self.options = {
            1: "Import Market Data from CSV",
            2: "Import Market Data from Excel",
            3: "Import Market Data from an API",
            4: "Import Market Data from Online Source",
            5: "Add A Security Manually",
            6: "Modify A Security Entry",
            0: "Return to Portfolio Manager Menu"
        }


# StatisticalAnalysis Menu class for managing the statistical analysis menu
class StatisticalAnalysis(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "STATISTICAL ANALYSIS"
        self.number_of_options = 9
        self.options = {
            1: "Portfolio Details",
            2: "Performance Analysis",  # CAGR, Annualized Return, Annualized Volatility, Annualized Sharpe Ratio, Annualized Sortino Ratio, Annualized Treynor Ratio, Annualized Jensen's Alpha, Annualized Information Ratio, Annualized Tracking Error, Annualized Value at Risk, Annualized Conditional Value at Risk
            3: "Risk Analysis", # Beta, Alpha, R-Squared, Sharpe Ratio, Sortino Ratio, Treynor Ratio, Jensen's Alpha, Information Ratio, Tracking Error, Value at Risk, Conditional Value at Risk
            4: "Correlation Analysis", # Correlation Matrix
            5: "Portfolio Optimization", # Markowitz
            6: "Portfolio Backtesting", # Sharpe Ratio
            7: "Portfolio Simulation", # Monte Carlo Simulation
            8: "Portfolio Forecasting", # ARIMA
            9: "Portfolio Stress Testing", # VaR
            # 10:. Custom Analysis") # Another menu with a list of custom analysis
            0: "Return to Portfolio Manager Menu" 
        }


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


# TradingStrategies Menu class for managing the trading strategies menu
class TradingStrategies(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "TRADING STRATEGIES"
        self.number_of_options = 5
        self.options = {
            1: "View Current Trading Strategies",
            2: "Add A Trading Strategy",
            3: "Modify A Trading Strategy",
            4: "Remove A Trading Strategy",
            0: "Return to Portfolio Manager Menu"
        }


# Reports Menu class for managing the reports menu
class Reports(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "REPORTS"
        self.number_of_options = 5
        self.options = {
            1: "View Current Reports",
            2: "Add A Report",
            3: "Modify A Report",
            4: "Remove A Report",
            0: "Return to Portfolio Manager Menu"
        }


# ExportData Menu class for managing the export data menu
class ExportData(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "EXPORT DATA"
        self.number_of_options = 6
        self.options = {
            1: "Export Portfolio Data",
            2: "Export Market Data",
            3: "Export Statistical Analysis",
            4: "Export Trading Strategies",
            5: "Export Reports",
            0: "Return to Portfolio Manager Menu"
        }


# Automation Menu class for managing the automation menu
class Automation(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "AUTOMATION"
        self.number_of_options = 4
        self.options = {
            1: "View Current Automations",
            2: "Add An Automation",
            3: "Modify An Automation",
            4: "Remove An Automation",
            0: "Return to Portfolio Manager Menu"
        }


# Notifications Menu class for managing the notifications menu
class Notifications(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "NOTIFICATIONS"
        self.number_of_options = 5
        self.options = {
            1: "View Current Notifications",
            2: "Add A Notification",
            3: "Modify A Notification",
            4: "Remove A Notification",
            0: "Return to Portfolio Manager Menu"
        }


# AccountSettings Menu class for managing the account settings menu
class AccountSettings(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "ACCOUNT SETTINGS"
        self.number_of_options = 5
        self.options = {
            1: "View Account Details",
            2: "Change Username",
            3: "Change Password",
            4: "Delete Account",
            0: "Return to Main Menu"
        }


# HelpAndInformation Menu class for managing the help and information menu
class HelpAndInformation(Menu):
    def __init__(self, session_manager: SessionManager) -> None:
        super().__init__(session_manager)
        self.title = "HELP AND INFORMATION"
        self.number_of_options = 9
        self.options = {
            1: "User Manual",
            2: "FAQ",
            3: "Glossary",
            4: "About",
            5: "Contact Us",
            6: "Report A Bug",
            7: "Request A Feature",
            8: "View the License",
            0: "Return to Main Menu"
        }


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
