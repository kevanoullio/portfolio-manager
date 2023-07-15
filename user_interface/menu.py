# Purpose: Menu module for managing menu related functions.

# Standard Libraries

# Third-party Libraries

# Local Modules
from user_interface.dashboard import Dashboard

# Configure logging
import logging


# Menu base class for managing menu related functions
class Menu:
    def __init__(self, dashboard: Dashboard) -> None:
        self.dashboard = dashboard
        self.is_active = False
        self.title = ""
        self.previous_menu = None
        self.next_menu_mapping = None
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


    def get_valid_input(self):
        while True:
            choice = input("\nPlease enter your choice: ")

            # Check if the input is a digit
            if not choice.isdigit():
                print("Invalid input. Please enter a digit.")
                continue

            choice = int(choice)

            # Check if the input is within the valid range
            logging.debug(f"Choice: {choice}")
            logging.debug(f"Option count: {self.option_count}")
            if choice < 0 or choice >= self.option_count:
                print("Invalid input. Please enter a valid option.")
                continue

            return choice


    def get_next_menu(self, choice: int):
        if self.next_menu_mapping is None:
            return None
        else:
            next_menu = self.next_menu_mapping.get(choice)
            if next_menu:
                return next_menu(self.dashboard)
            return None
    

# Login Menu class for managing the login menu
class Login(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "LOGIN MENU"
        self.options = {
            1: {"verb": "Create", "noun": "Account"},
            2: {"verb": "Log", "noun": "into Account"},
            0: {"verb": "Exit", "noun": "Program"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: Main,
            2: Main,
            0: None
        }
        self.menu_logic = {
            1: self.dashboard.create_account,
            2: self.dashboard.login,
            0: self.dashboard.exit_program
        }


# Main Menu class for managing the main menu
class Main(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MAIN MENU"
        self.previous_menu = Login(dashboard)
        self.options = {
            1: {"noun": "Portfolio Manager"},
            2: {"noun": "Account Settings"},
            3: {"noun": "Help and Information"},
            4: {"noun": "Save Changes"},
            5: {"noun": "Discard Changes"},
            0: {"noun": "Log Out"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: PortfolioManager,
            2: AccountSettings,
            3: HelpAndInformation,
            4: None,
            5: None,
            0: None
        }
        self.menu_logic = {
            1: self.dashboard.portfolio_manager,
            2: self.dashboard.account_settings,
            3: self.dashboard.help_information,
            4: self.dashboard.save_changes,
            5: self.dashboard.discard_changes,
            0: self.dashboard.log_out
        }


# PortfolioManager Menu class for managing the portfolio manager menu
class PortfolioManager(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO MANAGER"
        self.previous_menu = Main(dashboard)
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
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: ViewPortfolio,
            2: ManagePortfolio,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None
        }
        self.menu_logic = {
            1: self.dashboard.view_portfolio,
            2: self.dashboard.manage_portfolio,
            3: self.dashboard.market_data,
            4: self.dashboard.statistical_analysis,
            5: self.dashboard.trading_strategies,
            6: self.dashboard.reports,
            7: self.dashboard.export_data,
            8: self.dashboard.automation,
            9: self.dashboard.notifications
        }


# ViewPortfolio Menu class for managing the view portfolio menu
class ViewPortfolio(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW PORTFOLIO"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {
            1: {"verb": "View", "noun": "Current Portfolio"},
            2: {"verb": "View", "noun": "Entire Portfolio History"},
            3: {"verb": "Search", "noun": "for Current Investment"},
            4: {"verb": "Search", "noun": "for Investment in Portfolio History"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: None,
            2: None,
            3: None,
            4: None
        }
        self.menu_logic = {
            1: self.dashboard.view_current_portfolio,
            2: self.dashboard.view_entire_portfolio_history,
            3: self.dashboard.search_for_current_investment,
            4: self.dashboard.search_for_investment_in_portfolio_history
        }


# ManagePortfolio Menu class for managing the manage portfolio menu
class ManagePortfolio(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MANAGE PORTFOLIO"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {
            1: {"verb": "Build", "noun": "Portfolio from Data Set(s)"},
            2: {"verb": "Import", "noun": "Existing Portfolio Data Set"},
            3: {"verb": "Delete", "noun": "Existing Portfolio Data Set"},
            4: {"verb": "Manage", "noun": "Custom Import Scripts"},
            5: {"verb": "Add", "noun": "Investment Manually"},
            6: {"verb": "Modify", "noun": "Investment Entry"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: BuildPortfolio,
            2: ImportExistingPortfolio,
            3: None,
            4: None,
            5: None,
            6: None
        }
        self.menu_logic = {
            1: self.dashboard.build_portfolio_from_data_set,
            2: self.dashboard.import_existing_portfolio_data_set,
            3: self.dashboard.delete_existing_portfolio_data_set,
            4: self.dashboard.manage_custom_import_scripts,
            5: self.dashboard.add_investment_manually,
            6: self.dashboard.modify_investment_entry
        }


# BuildPortfolio Menu class for managing the build portfolio menu
class BuildPortfolio(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "BUILD PORTFOLIO"
        self.previous_menu = ManagePortfolio(dashboard)
        self.options = {
            1: {}
        }
        # TODO - finish this menu


# ImportExistingPortfolio Menu class for managing the import existing portfolio menu
class ImportExistingPortfolio(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT EXISTING PORTFOLIO"
        self.previous_menu = ManagePortfolio(dashboard)
        self.options = {
            1: {"verb": "Import", "noun": "Existing Portfolio from Brokerage Account"},
            2: {"verb": "Import", "noun": "Existing Portfolio from CSV File"},
            3: {"verb": "Import", "noun": "Existing Portfolio from Excel File"},
            4: {"verb": "Import", "noun": "Existing Portfolio from PDF file"},
            5: {"verb": "Import", "noun": "Existing Portfolio from Database file"},
            6: {"verb": "Import", "noun": "Existing Portfolio from Email Account"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: ImportFromBrokerageAccount,
            2: ImportFromCSVFile,
            3: ImportFromExcelFile,
            4: ImportFromPDFFile,
            5: ImportFromDatabaseFile,
            6: ImportFromEmail
        }
        self.menu_logic = {
            1: self.dashboard.import_existing_portfolio_from_brokerage_account,
            2: self.dashboard.import_existing_portfolio_from_csv_file,
            3: self.dashboard.import_existing_portfolio_from_excel_file,
            4: self.dashboard.import_existing_portfolio_from_pdf_file,
            5: self.dashboard.import_existing_portfolio_from_database_file,
            6: self.dashboard.import_existing_portfolio_from_email_account
        }


# ImportFromBrokerageAccount Menu class for managing the import from brokerage account menu
class ImportFromBrokerageAccount(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT FROM BROKERAGE ACCOUNT"
        self.previous_menu = ImportExistingPortfolio(dashboard)
        self.options = {} # TODO - Add dynamic list of brokerage accounts to choose from
        # TODO - finish this menu


# ImportFromCSVFile Menu class for managing the import from CSV file menu
class ImportFromCSVFile(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT FROM CSV FILE"
        self.previous_menu = ImportExistingPortfolio(dashboard)
        self.options = {} # TODO - Add dynamic list of CSV files to choose from
        # TODO - finish this menu


# ImportFromExcelFile Menu class for managing the import from Excel file menu
class ImportFromExcelFile(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT FROM EXCEL FILE"
        self.previous_menu = ImportExistingPortfolio(dashboard)
        self.options = {} # TODO - Add dynamic list of Excel files to choose from
        # TODO - finish this menu


# ImportFromPDFFile Menu class for managing the import from PDF file menu
class ImportFromPDFFile(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT FROM PDF FILE"
        self.previous_menu = ImportExistingPortfolio(dashboard)
        self.options = {} # TODO - Add dynamic list of PDF files to choose from
        # TODO - finish this menu


# ImportFromDatabaseFile Menu class for managing the import from database file menu
class ImportFromDatabaseFile(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT FROM DATABASE FILE"
        self.previous_menu = ImportExistingPortfolio(dashboard)
        self.options = {} # TODO - Add dynamic list of database files to choose from
        # TODO - finish this menu


# ImportFromEmail Menu class for managing the import from email menu
class ImportFromEmail(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT FROM EMAIL ACCOUNT"
        self.previous_menu = ImportExistingPortfolio(dashboard)
        self.options = {} # TODO - Add dynamic list of emails to choose from
        # TODO - finish this menu


# ManageCustomImportScripts Menu class for managing the manage custom import scripts menu
class ManageCustomImportScripts(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MANAGE CUSTOM IMPORT SCRIPTS"
        self.previous_menu = ManagePortfolio(dashboard)
        self.options = {
            1: {"verb": "View", "noun": "Custom Import Scripts"},
            2: {"verb": "Add", "noun": "Custom Import Script"},
            3: {"verb": "Remove", "noun": "Custom Import Script"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: CustomImportScripts,
            2: AddCustomImportScript,
            3: RemoveCustomImportScript
        }
        self.menu_logic = {
            1: self.dashboard.view_custom_import_scripts,
            2: self.dashboard.add_custom_import_script,
            3: self.dashboard.remove_custom_import_script
        }


# AddCustomImportScript Menu class for managing the add custom import script menu
class AddCustomImportScript(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD CUSTOM IMPORT SCRIPT"
        self.previous_menu = ManageCustomImportScripts(dashboard)
        self.options = {} # TODO - Add dynamic list of scripts to choose from
        # TODO - finish this menu


# RemoveCustomImportScript Menu class for managing the remove custom import script menu
class RemoveCustomImportScript(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE CUSTOM IMPORT SCRIPT"
        self.previous_menu = ManageCustomImportScripts(dashboard)
        self.options = {} # TODO - Add dynamic list of scripts to choose from
        # TODO - finish this menu


# CustomImportScripts Menu class for managing the custom import scripts menu
class CustomImportScripts(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CUSTOM IMPORT SCRIPTS"
        self.options = {} # TODO - Add dynamic list of scripts to choose from


# ManageMarketData Menu class for managing the manage market data menu
class ManageMarketData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MANAGE MARKET DATA"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {
            1: {"verb": "Import", "noun": "Market Data from CSV"},
            2: {"verb": "Import", "noun": "Market Data from Excel"},
            3: {"verb": "Import", "noun": "Market Data from an API"},
            4: {"verb": "Import", "noun": "Market Data from Online Source"},
            6: {"verb": "Modify", "noun": "Market Data Entry"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: ImportMarketDataFromCSV,
            2: ImportMarketDataFromExcel,
            3: ImportMarketDataFromAPI,
            4: ImportMarketDataFromOnlineSource,
            5: ModifyMarketDataEntry
        }
        self.menu_logic = {
            1: self.dashboard.import_market_data_from_csv,
            2: self.dashboard.import_market_data_from_excel,
            3: self.dashboard.import_market_data_from_api,
            4: self.dashboard.import_market_data_from_online_source,
            5: self.dashboard.modify_market_data_entry
        }


# ImportMarketDataFromCSV Menu class for managing the import market data from CSV menu
class ImportMarketDataFromCSV(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT MARKET DATA FROM CSV"
        self.previous_menu = ManageMarketData(dashboard)
        self.options = {} # TODO - Add dynamic list of CSV files to choose from
        # TODO - finish this menu


# ImportMarketDataFromExcel Menu class for managing the import market data from Excel menu
class ImportMarketDataFromExcel(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT MARKET DATA FROM EXCEL"
        self.previous_menu = ManageMarketData(dashboard)
        self.options = {} # TODO - Add dynamic list of Excel files to choose from
        # TODO - finish this menu


# ImportMarketDataFromAPI Menu class for managing the import market data from API menu
class ImportMarketDataFromAPI(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT MARKET DATA FROM API"
        self.previous_menu = ManageMarketData(dashboard)
        self.options = {} # TODO - Add dynamic list of APIs to choose from
        # TODO - finish this menu


# ImportMarketDataFromOnlineSource Menu class for managing the import market data from online source menu
class ImportMarketDataFromOnlineSource(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT MARKET DATA FROM ONLINE SOURCE"
        self.previous_menu = ManageMarketData(dashboard)
        self.options = {} # TODO - Add dynamic list of online sources to choose from
        # TODO - finish this menu


# ModifyMarketDataEntry Menu class for managing the modify market data entry menu
class ModifyMarketDataEntry(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY MARKET DATA ENTRY"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {} # TODO - Add dynamic list of market data to choose from
        # TODO - finish this menu


# StatisticalAnalysis Menu class for managing the statistical analysis menu
class StatisticalAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "STATISTICAL ANALYSIS"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {
            1: {"noun": "Portfolio Overview"}, # Basic overview of all statistics
            2: {"noun": "Performance Analysis"}, # CAGR, Annualized Return, Annualized Volatility, Annualized Sharpe Ratio, Annualized Sortino Ratio, Annualized Treynor Ratio, Annualized Jensen's Alpha, Annualized Information Ratio, Annualized Tracking Error, Annualized Value at Risk, Annualized Conditional Value at Risk
            3: {"noun": "Risk Analysis"}, # Beta, Alpha, R-Squared, Sharpe Ratio, Sortino Ratio, Treynor Ratio, Jensen's Alpha, Information Ratio, Tracking Error, Value at Risk, Conditional Value at Risk
            4: {"noun": "Correlation Analysis"}, # Correlation Matrix
            5: {"noun": "Portfolio Optimization"}, # Markowitz
            6: {"noun": "Portfolio Backtesting"}, # Sharpe Ratio
            7: {"noun": "Portfolio Simulation"}, # Monte Carlo Simulation
            8: {"noun": "Portfolio Forecasting"}, # ARIMA
            9: {"noun": "Portfolio Stress Testing"} # VaR
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: PortfolioOverview,
            2: PerformanceAnalysis,
            3: RiskAnalysis,
            4: CorrelationAnalysis,
            5: PortfolioOptimization,
            6: PortfolioBacktesting,
            7: PortfolioSimulation,
            8: PortfolioForecasting,
            9: PortfolioStressTesting
        }
        self.menu_logic = {
            1: self.dashboard.portfolio_overview,
            2: self.dashboard.performance_analysis,
            3: self.dashboard.risk_analysis,
            4: self.dashboard.correlation_analysis,
            5: self.dashboard.portfolio_optimization,
            6: self.dashboard.portfolio_backtesting,
            7: self.dashboard.portfolio_simulation,
            8: self.dashboard.portfolio_forecasting,
            9: self.dashboard.portfolio_stress_testing
        }


# PortfolioOverview Menu class for managing the portfolio overview menu
class PortfolioOverview(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO OVERVIEW"
        self.previous_menu = StatisticalAnalysis(dashboard)
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PerformanceAnalysis Menu class for managing the performance analysis menu
class PerformanceAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PERFORMANCE ANALYSIS"
        self.previous_menu = StatisticalAnalysis(dashboard)
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# RiskAnalysis Menu class for managing the risk analysis menu
class RiskAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "RISK ANALYSIS"
        self.previous_menu = StatisticalAnalysis(dashboard)
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# CorrelationAnalysis Menu class for managing the correlation analysis menu
class CorrelationAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CORRELATION ANALYSIS"
        self.previous_menu = StatisticalAnalysis(dashboard)
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioOptimization Menu class for managing the portfolio optimization menu
class PortfolioOptimization(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO OPTIMIZATION"
        self.previous_menu = StatisticalAnalysis(dashboard)
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioBacktesting Menu class for managing the portfolio backtesting menu
class PortfolioBacktesting(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO BACKTESTING"
        self.previous_menu = StatisticalAnalysis(dashboard)
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioSimulation Menu class for managing the portfolio simulation menu
class PortfolioSimulation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO SIMULATION"
        self.previous_menu = StatisticalAnalysis(dashboard)
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioForecasting Menu class for managing the portfolio forecasting menu
class PortfolioForecasting(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO FORECASTING"
        self.previous_menu = StatisticalAnalysis(dashboard)
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioStressTesting Menu class for managing the portfolio stress testing menu
class PortfolioStressTesting(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO STRESS TESTING"
        self.previous_menu = StatisticalAnalysis(dashboard)
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# TradingStrategies Menu class for managing the trading strategies menu
class TradingStrategies(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "TRADING STRATEGIES"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {
            1: {"verb": "View", "noun": "Current Trading Strategies"},
            2: {"verb": "Add", "noun": "Trading Strategy"},
            3: {"verb": "Modify", "noun": "Trading Strategy"},
            4: {"verb": "Remove", "noun": "Trading Strategy"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: CurrentTradingStrategies,
            2: AddTradingStrategy,
            3: ModifyTradingStrategy,
            4: RemoveTradingStrategy
        }
        self.menu_logic = {
            1: self.dashboard.current_trading_strategies,
            2: self.dashboard.add_trading_strategy,
            3: self.dashboard.modify_trading_strategy,
            4: self.dashboard.remove_trading_strategy
        }


# CurrentTradingStrategies Menu class for managing the current trading strategies menu
class CurrentTradingStrategies(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CURRENT TRADING STRATEGIES"
        self.previous_menu = TradingStrategies(dashboard)
        self.options = {} # TODO - Add dynamic list of trading strategies to choose from
        # TODO - finish this menu


# AddTradingStrategy Menu class for managing the add trading strategy menu
class AddTradingStrategy(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD TRADING STRATEGY"
        self.previous_menu = TradingStrategies(dashboard)
        self.options = {} # TODO - Add dynamic list of trading strategies to choose from
        # TODO - finish this menu


# ModifyTradingStrategy Menu class for managing the modify trading strategy menu
class ModifyTradingStrategy(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY TRADING STRATEGY"
        self.previous_menu = TradingStrategies(dashboard)
        self.options = {} # TODO - Add dynamic list of trading strategies to choose from
        # TODO - finish this menu


# RemoveTradingStrategy Menu class for managing the remove trading strategy menu
class RemoveTradingStrategy(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE TRADING STRATEGY"
        self.previous_menu = TradingStrategies(dashboard)
        self.options = {} # TODO - Add dynamic list of trading strategies to choose from
        # TODO - finish this menu


# Reports Menu class for managing the reports menu
class Reports(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REPORTS"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {
            1: {"verb": "View", "noun": "Current Reports"},
            2: {"verb": "Add", "noun": "Report"},
            3: {"verb": "Modify", "noun": "Report"},
            4: {"verb": "Remove", "noun": "Report"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: ViewCurrentReports,
            2: AddReport,
            3: ModifyReport,
            4: RemoveReport
        }
        self.menu_logic = {
            1: self.dashboard.view_current_reports,
            2: self.dashboard.add_report,
            3: self.dashboard.modify_report,
            4: self.dashboard.remove_report
        }


# ViewCurrentReports Menu class for managing the view current reports menu
class ViewCurrentReports(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW CURRENT REPORTS"
        self.previous_menu = Reports(dashboard)
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# AddReport Menu class for managing the add report menu
class AddReport(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD REPORT"
        self.previous_menu = Reports(dashboard)
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ModifyReport Menu class for managing the modify report menu
class ModifyReport(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY REPORT"
        self.previous_menu = Reports(dashboard)
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# RemoveReport Menu class for managing the remove report menu
class RemoveReport(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE REPORT"
        self.previous_menu = Reports(dashboard)
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportData Menu class for managing the export data menu
class ExportData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT DATA"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {
            1: {"verb": "Export", "noun": "Portfolio Data"},
            2: {"verb": "Export", "noun": "Market Data"},
            3: {"verb": "Export", "noun": "Statistical Analysis"},
            4: {"verb": "Export", "noun": "Trading Strategies"},
            5: {"verb": "Export", "noun": "Reports"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: ExportPortfolioData,
            2: ExportMarketData,
            3: ExportStatisticalAnalysis,
            4: ExportTradingStrategies,
            5: ExportReports
        }
        self.menu_logic = {
            1: self.dashboard.export_portfolio_data,
            2: self.dashboard.export_market_data,
            3: self.dashboard.export_statistical_analysis,
            4: self.dashboard.export_trading_strategies,
            5: self.dashboard.export_reports
        }


# ExportPortfolioData Menu class for managing the export portfolio data menu
class ExportPortfolioData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT PORTFOLIO DATA"
        self.previous_menu = ExportData(dashboard)
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportMarketData Menu class for managing the export market data menu
class ExportMarketData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT MARKET DATA"
        self.previous_menu = ExportData(dashboard)
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportStatisticalAnalysis Menu class for managing the export statistical analysis menu
class ExportStatisticalAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT STATISTICAL ANALYSIS"
        self.previous_menu = ExportData(dashboard)
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportTradingStrategies Menu class for managing the export trading strategies menu
class ExportTradingStrategies(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT TRADING STRATEGIES"
        self.previous_menu = ExportData(dashboard)
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportReports Menu class for managing the export reports menu
class ExportReports(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT REPORTS"
        self.previous_menu = ExportData(dashboard)
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# Automation Menu class for managing the automation menu
class Automation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "AUTOMATION"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {
            1: {"verb": "View", "noun": "Current Automations"},
            2: {"verb": "Add", "noun": "Automation"},
            3: {"verb": "Modify", "noun": "Automation"},
            4: {"verb": "Remove", "noun": "Automation"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: ViewAutomations,
            2: AddAutomation,
            3: ModifyAutomation,
            4: RemoveAutomation
        }
        self.menu_logic = {
            1: self.dashboard.view_automations,
            2: self.dashboard.add_automation,
            3: self.dashboard.modify_automation,
            4: self.dashboard.remove_automation
        }


# ViewAutomations Menu class for managing the view automations menu
class ViewAutomations(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW AUTOMATIONS"
        self.previous_menu = Automation(dashboard)
        self.options = {} # TODO - Add dynamic list of automations to choose from
        # TODO - finish this menu


# AddAutomation Menu class for managing the add automation menu
class AddAutomation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD AUTOMATION"
        self.previous_menu = Automation(dashboard)
        self.options = {} # TODO - Add dynamic list of automations to choose from
        # TODO - finish this menu


# ModifyAutomation Menu class for managing the modify automation menu
class ModifyAutomation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY AUTOMATION"
        self.previous_menu = Automation(dashboard)
        self.options = {} # TODO - Add dynamic list of automations to choose from
        # TODO - finish this menu


# RemoveAutomation Menu class for managing the remove automation menu
class RemoveAutomation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE AUTOMATION"
        self.previous_menu = Automation(dashboard)
        self.options = {} # TODO - Add dynamic list of automations to choose from
        # TODO - finish this menu


# Notifications Menu class for managing the notifications menu
class Notifications(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "NOTIFICATIONS"
        self.previous_menu = PortfolioManager(dashboard)
        self.options = {
            1: {"verb": "View", "noun": "Current Notifications"},
            2: {"verb": "Add", "noun": "Notification"},
            3: {"verb": "Modify", "noun": "Notification"},
            4: {"verb": "Remove", "noun": "Notification"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: ViewNotifications,
            2: AddNotification,
            3: ModifyNotification,
            4: RemoveNotification
        }
        self.menu_logic = {
            1: self.dashboard.view_notifications,
            2: self.dashboard.add_notification,
            3: self.dashboard.modify_notification,
            4: self.dashboard.remove_notification
        }


# ViewNotifications Menu class for managing the view notifications menu
class ViewNotifications(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW NOTIFICATIONS"
        self.previous_menu = Notifications(dashboard)
        self.options = {} # TODO - Add dynamic list of notifications to choose from
        # TODO - finish this menu


# AddNotification Menu class for managing the add notification menu
class AddNotification(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD NOTIFICATION"
        self.previous_menu = Notifications(dashboard)
        self.options = {} # TODO - Add dynamic list of notifications to choose from
        # TODO - finish this menu


# ModifyNotification Menu class for managing the modify notification menu
class ModifyNotification(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY NOTIFICATION"
        self.previous_menu = Notifications(dashboard)
        self.options = {} # TODO - Add dynamic list of notifications to choose from
        # TODO - finish this menu


# RemoveNotification Menu class for managing the remove notification menu
class RemoveNotification(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE NOTIFICATION"
        self.previous_menu = Notifications(dashboard)
        self.options = {} # TODO - Add dynamic list of notifications to choose from
        # TODO - finish this menu


# AccountSettings Menu class for managing the account settings menu
class AccountSettings(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ACCOUNT SETTINGS"
        self.previous_menu = Main(dashboard)
        self.options = {
            1: {"verb": "View", "noun": "User Details"},
            2: {"verb": "Manage", "noun": "Email Accounts"},
            3: {"verb": "Change", "noun": "Account Username"},
            4: {"verb": "Change", "noun": "Account Password"},
            5: {"verb": "Delete", "noun": "Account"},
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: ViewUserDetails,
            2: ManageEmailAccounts,
            3: ChangeAccountUsername,
            4: ChangeAccountPassword,
            5: DeleteAccount
        }
        self.menu_logic = {
            1: self.dashboard.view_user_details,
            2: self.dashboard.manage_email_accounts,
            3: self.dashboard.change_account_username,
            4: self.dashboard.change_account_password,
            5: self.dashboard.delete_account
        }


# ViewUserDetails Menu class for managing the view user details menu
class ViewUserDetails(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW USER DETAILS"
        self.previous_menu = AccountSettings(dashboard)
        self.options = {} # TODO - Add dynamic list of user details to choose from
        # TODO - finish this menu


# ViewUserDetails Menu class for managing the user's email accounts
class ManageEmailAccounts(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MANAGE EMAIL ACCOUNTS"
        self.previous_menu = AccountSettings(dashboard)
        self.options = {
            1: {"verb": "View", "noun": "Current Email Accounts"},
            2: {"verb": "Add", "noun": "Email Account"},
            3: {"verb": "Remove", "noun": "Email Account"}
        }
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: CurrentEmailAccounts,
            2: AddEmailAccount,
            3: RemoveEmailAccount
        }
        self.menu_logic = {
            1: self.dashboard.view_current_email_accounts,
            2: self.dashboard.add_email_account,
            3: self.dashboard.remove_email_account
        }


# AddEmailAccount Menu class for managing the add email account menu
class AddEmailAccount(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD EMAIL ACCOUNT"
        self.previous_menu = ManageEmailAccounts(dashboard)
        self.options = {} # TODO - Add dynamic list of email accounts to choose from
        # TODO - finish this menu


# RemoveEmailAccount Menu class for managing the remove email account menu
class RemoveEmailAccount(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE EMAIL ACCOUNT"
        self.previous_menu = ManageEmailAccounts(dashboard)
        self.options = {} # TODO - Add dynamic list of email accounts to choose from
        # TODO - finish this menu


# ChangeAccountUsername Menu class for managing the change account username menu
class ChangeAccountUsername(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CHANGE ACCOUNT USERNAME"
        self.previous_menu = AccountSettings(dashboard)
        self.options = {} # TODO - Add dynamic list of email accounts to choose from
        # TODO - finish this menu


# ChangeAccountPassword Menu class for managing the change account password menu
class ChangeAccountPassword(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CHANGE ACCOUNT PASSWORD"
        self.previous_menu = AccountSettings(dashboard)
        self.options = {} # TODO - Add dynamic list of email accounts to choose from
        # TODO - finish this menu


# DeleteAccount Menu class for managing the delete account menu
class DeleteAccount(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "DELETE ACCOUNT"
        self.previous_menu = AccountSettings(dashboard)
        self.options = {} # TODO - Add dynamic list of email accounts to choose from
        # TODO - finish this menu


# CurrentEmailAccounts Menu class for managing the user's current email accounts
class CurrentEmailAccounts(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CURRENT EMAIL ACCOUNTS"
        self.previous_menu = ManageEmailAccounts(dashboard)
        self.options = {} # TODO - Populate user's current email accounts
        # TODO - finish this menu


# HelpAndInformation Menu class for managing the help and information menu
class HelpAndInformation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "HELP AND INFORMATION"
        self.previous_menu = Main(dashboard)
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
        self.option_count = len(self.options)
        self.next_menu_mapping = {
            1: ViewUserManual,
            2: ViewFAQ,
            3: ViewGlossary,
            4: About,
            5: ContactUs,
            6: ReportBug,
            7: RequestFeature,
            8: ViewLicense
        }
        self.menu_logic = {
            1: self.dashboard.view_user_manual,
            2: self.dashboard.view_faq,
            3: self.dashboard.view_glossary,
            4: self.dashboard.about,
            5: self.dashboard.contact_us,
            6: self.dashboard.report_bug,
            7: self.dashboard.request_feature,
            8: self.dashboard.view_license
        }


# ViewUserManual Menu class for managing the view user manual menu
class ViewUserManual(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW USER MANUAL"
        self.previous_menu = HelpAndInformation(dashboard)
        self.options = {} # TODO - Add dynamic list of user manual pages to choose from
        # TODO - finish this menu


# ViewFAQ Menu class for managing the view FAQ menu
class ViewFAQ(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW FAQ"
        self.previous_menu = HelpAndInformation(dashboard)
        self.options = {} # TODO - Add dynamic list of FAQ pages to choose from
        # TODO - finish this menu


# ViewGlossary Menu class for managing the view glossary menu
class ViewGlossary(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW GLOSSARY"
        self.previous_menu = HelpAndInformation(dashboard)
        self.options = {} # TODO - Add dynamic list of glossary pages to choose from
        # TODO - finish this menu


# About Menu class for managing the about menu
class About(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ABOUT"
        self.previous_menu = HelpAndInformation(dashboard)
        self.options = {} # TODO - Add dynamic list of about pages to choose from
        # TODO - finish this menu


# ContactUs Menu class for managing the contact us menu
class ContactUs(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CONTACT US"
        self.previous_menu = HelpAndInformation(dashboard)
        self.options = {} # TODO - Add dynamic list of contact us pages to choose from
        # TODO - finish this menu


# ReportBug Menu class for managing the report bug menu
class ReportBug(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REPORT A BUG"
        self.previous_menu = HelpAndInformation(dashboard)
        self.options = {} # TODO - Add dynamic list of report bug pages to choose from
        # TODO - finish this menu


# RequestFeature Menu class for managing the request feature menu
class RequestFeature(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REQUEST A FEATURE"
        self.previous_menu = HelpAndInformation(dashboard)
        self.options = {} # TODO - Add dynamic list of request feature pages to choose from
        # TODO - finish this menu


# ViewLicense Menu class for managing the view license menu
class ViewLicense(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW LICENSE"
        self.previous_menu = HelpAndInformation(dashboard)
        self.options = {} # TODO - Add dynamic list of license pages to choose from
        # TODO - finish this menu


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")  