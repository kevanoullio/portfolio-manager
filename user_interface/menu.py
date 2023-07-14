# Purpose: Menu module for managing menu related functions.

# Standard Libraries

# Third-party Libraries

# Local Modules

# Configure logging
import logging


# Menu base class for managing menu related functions
class Menu:
    def __init__(self) -> None:
        self.is_active = False
        self.title = ""
        self.previous_menu = None
        self.options = {
            0: {"verb": "Return", "preposition": "to", "adjective": "Previous", "noun": "Menu"} if self.previous_menu is None else
               {"verb": "Return", "preposition": "to", "adjective": f"{self.previous_menu.title.title()}", "noun": "Menu"}
        }
        self.option_count = len(self.options)
        # self.selected_choice_msg = {
        #     option: f"{self.options[option].get('verb', '').lower() + 'ing ' if 'verb' in self.options[option] else ''}"
        #             f"{self.options[option].get('preposition', '').lower() + ' ' if 'preposition' in self.options[option] else ''}"
        #             f"{self.options[option].get('adjective', '').lower() + ' ' if 'adjective' in self.options[option] else ''}"
        #             f"{self.options[option].get('noun', '').lower() if 'noun' in self.options[option] else ''}..."
        #             .capitalize()
        #     for option in self.options
        # }


    def sort_options(self) -> list[int]:
        # Sort the keys excluding 0
        options_sorted = sorted([key for key in self.options.keys() if isinstance(key, int) and key != 0])
        # Sort the alphabetical keys and append them to the options list
        options_sorted.extend(sorted([key for key in self.options.keys() if isinstance(key, str)]))
        # Append 0 to the end of the options list
        options_sorted.append(0)
        return options_sorted


    def print_options(self) -> None:
        # Print the menu title
        print(f"\n{self.title.upper()}")
        print("-" * len(self.title))
        # Get the sorted options
        options_sorted = self.sort_options()
        # Print the sorted options
        for option in options_sorted:
            option_text = f"{option}: "
            if "verb" in self.options[option]:
                option_text += f"{self.options[option]['verb']} "
            if "preposition" in self.options[option]:
                option_text += f"{self.options[option]['preposition']} "
            if "adjective" in self.options[option]:
                option_text += f"{self.options[option]['adjective']} "
            if "noun" in self.options[option]:
                option_text += f"{self.options[option]['noun']}"
            print(option_text)


    def print_choice_msg(self, option: int | str) -> None:
        if option in self.options:
            # TODO - account for verbs that end in 'e' and 'y'
            choice_msg = f"{self.options[option].get('verb', '').lower() + 'ing ' if 'verb' in self.options[option] else ''}" \
                        f"{self.options[option].get('preposition', '').lower() + ' ' if 'preposition' in self.options[option] else ''}" \
                        f"{self.options[option].get('adjective', '').lower() + ' ' if 'adjective' in self.options[option] else ''}" \
                        f"{self.options[option].get('noun', '').lower() if 'noun' in self.options[option] else ''}..." \
                        .capitalize()
            print(f"{option}: {choice_msg}")
        else:
            print(f"Option {option} does not exist.")


    def add_option(self, verb: str = "", preposition: str = "", adjective: str = "", noun: str = "") -> None:
        self.option_count += 1
        new_option = {}
        if verb:
            new_option["verb"] = verb
        if preposition:
            new_option["preposition"] = preposition
        if adjective:
            new_option["adjective"] = adjective
        if noun:
            new_option["noun"] = noun
        self.options[self.option_count] = new_option
        logging.info(f"Option {self.option_count} has been added.")


    def remove_option(self, option_number: int) -> None:
        if option_number == 0:
            logging.warning(f"Option {option_number} cannot be removed.")
        elif option_number in self.options:
            del self.options[option_number]
            self.option_count -= 1
            logging.info(f"Option {option_number} has been removed.")
        else:
            logging.warning(f"Option {option_number} does not exist.")



# Login Menu class for managing the login menu
class Login(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "LOGIN MENU"
        self.options = {
            1: {"verb": "Create", "noun": "Account"},
            2: {"verb": "Log", "noun": "into Account"},
            0: {"verb": "Exit", "noun": "Program"}
        }
        self.menu_logic = {
            1: self.create_account,
            2: self.login,
            0: self.exit_program
        }
        self.next_menus = {
            1: Main(),
            2: Main()
        }


# Main Menu class for managing the main menu
class Main(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "MAIN MENU"
        self.previous_menu = Login()
        self.options = {
            1: {"noun": "Portfolio Manager"},
            2: {"noun": "Account Settings"},
            3: {"noun": "Help and Information"},
            4: {"noun": "Save Changes"},
            5: {"noun": "Discard Changes"},
            0: {"noun": "Log Out"}
        }


# PortfolioManager Menu class for managing the portfolio manager menu
class PortfolioManager(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "PORTFOLIO MANAGER"
        self.previous_menu = Main()
        self.options = {
            1: {"verb": "View", "noun": "Portfolio"},
            2: {"verb": "Manage", "noun": "Portfolio"},
            3: {"noun": "Market Data"},
            4: {"noun": "Statistical Analysis"},
            5: {"noun": "Trading Strategies"},
            6: {"noun": "Reports"},
            7: {"noun": "Export Data"},
            8: {"noun": "Automation"},
            9: {"noun": "Notifications"}
        }


# ViewPortfolio Menu class for managing the view portfolio menu
class ViewPortfolio(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "VIEW PORTFOLIO"
        self.previous_menu = PortfolioManager()
        self.options = {
            1: {"verb": "View", "noun": "Current Portfolio"},
            2: {"verb": "View", "noun": "Entire Portfolio History"},
            3: {"verb": "Search", "noun": "for Current Investment"},
            4: {"verb": "Search", "noun": "for Investment in Portfolio History"}
        }


# ManagePortfolio Menu class for managing the manage portfolio menu
class ManagePortfolio(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "MANAGE PORTFOLIO"
        self.previous_menu = PortfolioManager()
        self.options = {
            1: {"verb": "Build", "noun": "Portfolio from Data Set(s)"},
            2: {"verb": "Import", "noun": "Existing Portfolio Data Set"},
            3: {"verb": "Delete", "noun": "Existing Portfolio Data Set"},
            4: {"verb": "Manage", "noun": "Custom Import Scripts"},
            5: {"verb": "Add", "noun": "Investment Manually"},
            6: {"verb": "Modify", "noun": "Investment Entry"}
        }


# ImportExistingPortfolio Menu class for managing the import existing portfolio menu
class ImportExistingPortfolio(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "IMPORT EXISTING PORTFOLIO"
        self.previous_menu = ManagePortfolio()
        self.options = {
            1: {"verb": "Import", "noun": "Existing Portfolio from Brokerage Account"},
            2: {"verb": "Import", "noun": "Existing Portfolio from CSV File"},
            3: {"verb": "Import", "noun": "Existing Portfolio from Excel File"},
            4: {"verb": "Import", "noun": "Existing Portfolio from PDF file"},
            5: {"verb": "Import", "noun": "Existing Portfolio from Database file"},
            6: {"verb": "Import", "noun": "Existing Portfolio from Email Account"}
        }


# ImportFromEmail Menu class for managing the import from email menu
class ImportFromEmail(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "IMPORT FROM EMAIL ACCOUNT"
        self.previous_menu = ImportExistingPortfolio()
        self.options = {} # TODO - Add dynamic list of emails to choose from


# ManageCustomImportScripts Menu class for managing the manage custom import scripts menu
class ManageCustomImportScripts(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "MANAGE CUSTOM IMPORT SCRIPTS"
        self.previous_menu = ManagePortfolio()
        self.options = {
            1: {"verb": "View", "noun": "Custom Import Scripts"},
            2: {"verb": "Add", "noun": "Custom Import Script"},
            3: {"verb": "Remove", "noun": "Custom Import Script"}
        }


# CustomImportScripts Menu class for managing the custom import scripts menu
class CustomImportScripts(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "CUSTOM IMPORT SCRIPTS"
        self.options = {} # TODO - Add dynamic list of scripts to choose from


# ManageMarketData Menu class for managing the manage market data menu
class ManageMarketData(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "MANAGE MARKET DATA"
        self.previous_menu = PortfolioManager()
        self.options = {
            1: {"verb": "Import", "noun": "Market Data from CSV"},
            2: {"verb": "Import", "noun": "Market Data from Excel"},
            3: {"verb": "Import", "noun": "Market Data from an API"},
            4: {"verb": "Import", "noun": "Market Data from Online Source"},
            5: {"verb": "Add", "noun": "Security Manually"},
            6: {"verb": "Modify", "noun": "Security Entry"}
        }


# StatisticalAnalysis Menu class for managing the statistical analysis menu
class StatisticalAnalysis(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "STATISTICAL ANALYSIS"
        self.previous_menu = PortfolioManager()
        self.options = {
            1: {"noun": "Portfolio Details"},
            2: {"noun": "Performance Analysis"}, # CAGR, Annualized Return, Annualized Volatility, Annualized Sharpe Ratio, Annualized Sortino Ratio, Annualized Treynor Ratio, Annualized Jensen's Alpha, Annualized Information Ratio, Annualized Tracking Error, Annualized Value at Risk, Annualized Conditional Value at Risk
            3: {"noun": "Risk Analysis"}, # Beta, Alpha, R-Squared, Sharpe Ratio, Sortino Ratio, Treynor Ratio, Jensen's Alpha, Information Ratio, Tracking Error, Value at Risk, Conditional Value at Risk
            4: {"noun": "Correlation Analysis"}, # Correlation Matrix
            5: {"noun": "Portfolio Optimization"}, # Markowitz
            6: {"noun": "Portfolio Backtesting"}, # Sharpe Ratio
            7: {"noun": "Portfolio Simulation"}, # Monte Carlo Simulation
            8: {"noun": "Portfolio Forecasting"}, # ARIMA
            9: {"noun": "Portfolio Stress Testing"} # VaR
            # 10:. Custom Analysis") # Another menu with a list of custom analysis
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
    def __init__(self) -> None:
        super().__init__()
        self.title = "TRADING STRATEGIES"
        self.previous_menu = PortfolioManager()
        self.options = {
            1: {"verb": "View", "noun": "Current Trading Strategies"},
            2: {"verb": "Add", "noun": "Trading Strategy"},
            3: {"verb": "Modify", "noun": "Trading Strategy"},
            4: {"verb": "Remove", "noun": "Trading Strategy"}
        }


# Reports Menu class for managing the reports menu
class Reports(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "REPORTS"
        self.previous_menu = PortfolioManager()
        self.options = {
            1: {"verb": "View", "noun": "Current Reports"},
            2: {"verb": "Add", "noun": "Report"},
            3: {"verb": "Modify", "noun": "Report"},
            4: {"verb": "Remove", "noun": "Report"}
        }


# ExportData Menu class for managing the export data menu
class ExportData(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "EXPORT DATA"
        self.previous_menu = PortfolioManager()
        self.options = {
            1: {"verb": "Export", "noun": "Portfolio Data"},
            2: {"verb": "Export", "noun": "Market Data"},
            3: {"verb": "Export", "noun": "Statistical Analysis"},
            4: {"verb": "Export", "noun": "Trading Strategies"},
            5: {"verb": "Export", "noun": "Reports"}
        }


# Automation Menu class for managing the automation menu
class Automation(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "AUTOMATION"
        self.previous_menu = PortfolioManager()
        self.options = {
            1: {"verb": "View", "noun": "Current Automations"},
            2: {"verb": "Add", "noun": "Automation"},
            3: {"verb": "Modify", "noun": "Automation"},
            4: {"verb": "Remove", "noun": "Automation"}
        }


# Notifications Menu class for managing the notifications menu
class Notifications(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "NOTIFICATIONS"
        self.previous_menu = PortfolioManager()
        self.options = {
            1: {"verb": "View", "noun": "Current Notifications"},
            2: {"verb": "Add", "noun": "Notification"},
            3: {"verb": "Modify", "noun": "Notification"},
            4: {"verb": "Remove", "noun": "Notification"}
        }


# AccountSettings Menu class for managing the account settings menu
class AccountSettings(Menu):
    def __init__(self):
        super().__init__()
        self.title = "ACCOUNT SETTINGS"
        self.previous_menu = Main()
        self.options = {
            1: {"verb": "View", "noun": "User Details"},
            2: {"verb": "Manage", "noun": "Email Accounts"},
            3: {"verb": "Change", "noun": "Account Username"},
            4: {"verb": "Change", "noun": "Account Password"},
            5: {"verb": "Delete", "noun": "Account"},
        }


# ViewUserDetails Menu class for managing the user's email accounts
class ManageEmailAccounts(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "MANAGE EMAIL ACCOUNTS"
        self.previous_menu = AccountSettings()
        self.options = {
            1: {"verb": "View", "noun": "Current Email Accounts"},
            2: {"verb": "Add", "noun": "Email Account"},
            3: {"verb": "Remove", "noun": "Email Account"}
        }


# CurrentEmailAccounts Menu class for managing the user's current email accounts
class CurrentEmailAccounts(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "CURRENT EMAIL ACCOUNTS"
        self.previous_menu = ManageEmailAccounts()
        self.options = {} # TODO - Populate user's current email accounts


# HelpAndInformation Menu class for managing the help and information menu
class HelpAndInformation(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.title = "HELP AND INFORMATION"
        self.previous_menu = Main()
        self.options = {
            1: {"verb": "View", "noun": "User Manual"},
            2: {"verb": "View", "noun": "FAQ"},
            3: {"verb": "View", "noun": "Glossary"},
            4: {"noun": "About"},
            5: {"noun": "Contact Us"},
            6: {"verb": "Report", "noun": "a Bug"},
            7: {"verb": "Request", "noun": "a Feature"},
            8: {"verb": "View", "noun": "the License"}
        }


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")  
