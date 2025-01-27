# Purpose: Menu module for managing menu related functions.

# Standard Libraries

# Third-party Libraries

# Local Modules
from user_interface.dashboard import Dashboard
from user_interface.user_input import UserInput

# Configure logging
import logging


# Menu base class for managing menu related functions
class Menu:
    def __init__(self, dashboard: Dashboard) -> None:
        self.dashboard = dashboard
        self.is_active = False
        self.title = ""
        self.previous_menu = None
        self.menu_mapping = {}
        self.options = {}
        self.option_count = len(self.options)

    def format_return_to_previous_menu_option(self) -> None:
        # Format the return to previous menu option
        if isinstance(self, Login):
            self.options[0] = {"verb": "Exit", "connector": "the", "subject": "Program"}
        elif isinstance(self, Main):
            self.options[0] = {"verb": "Log", "subject": "out"}
        else:
            if self.previous_menu is None:
                self.options[0] = {"verb": "Return", "connector": "to", "subject": "Previous Menu"}
            else:
                self.options[0] = {"verb": "Return", "connector": "to", "subject": f"{self.previous_menu.title.title()} Menu"}

    def print_options(self) -> None:
        # Print the menu title
        print(f"\n{self.title.upper()}")
        print("-" * len(self.title))

        # Collect the options for logging purposes
        debug_options = []
        for key, inner_dict in self.options.items():
            debug_options.append(key)
            value_tmp = ""
            for value in inner_dict.values():
                value_tmp += f"{value} "
            debug_options.append(value_tmp.strip())
        logging.info(f"Options: {debug_options}")

        # Print the sorted options to the console
        for option, option_dict in self.options.items():
            option_text = f"{option}: "

            if "verb" in option_dict:
                option_text += f"{option_dict['verb']} "
            if "connector" in option_dict:
                option_text += f"{option_dict['connector']} "
            if "subject" in option_dict:
                option_text += f"{option_dict['subject']}"

            print(option_text)

    def present_to_participle(self, present_verb: str) -> str:
        # Define irregular verbs found in the program
        irregular_verbs = {
            "exit": "exiting",
            "import": "importing"
        }

        # Check if the verb ends in "e"
        if present_verb.endswith("e"):
            formatted_verb = present_verb[:-1] + "ing"
        # Check if the verb is one syllable and ends in a consonant-vowel-consonant pattern
        elif (len(present_verb) == 3 and
            present_verb[-3] not in "aeiou" and
            present_verb[-2] in "aeiou" and
            present_verb[-1] not in "aeiou"):
            formatted_verb = present_verb + present_verb[-1] + "ing"
        # Check if the verb is one syllable and ends with a single consonant preceded by a single vowel
        elif (len(present_verb) == 2 and
            present_verb[-1] not in "aeiou" and
            present_verb[-2] in "aeiou"):
            formatted_verb = present_verb + present_verb[-1] + "ing"
        # Check if the verb is irregular
        elif present_verb in irregular_verbs:
            formatted_verb = irregular_verbs[present_verb]
        # Otherwise, add "ing" to the end of the verb
        else:
            formatted_verb = present_verb + "ing"

        # Preserve the original case of the verb
        if present_verb.isupper():
            return formatted_verb.upper()
        elif present_verb.istitle():
            return formatted_verb.title()
        else:
            return formatted_verb

    def print_choice_msg(self, option: int | str) -> None:
        if option in self.options:
            verb = self.options[option].get('verb', '')
            formatted_verb = self.present_to_participle(verb) if verb else ''

            connector = self.options[option].get('connector', '')
            subject = self.options[option].get('subject', '')

            choice_parts = []
            if formatted_verb:
                choice_parts.append(formatted_verb.lower())
            if connector:
                choice_parts.append(connector.lower())
            if subject:
                choice_parts.append(subject.lower())

            choice_msg = ' '.join(choice_parts)
            print(f"{choice_msg.capitalize()}...")
        else:
            print(f"Option {option} does not exist.")

    def add_option(self, verb: str | None = None, connector: str | None = None, subject: str | None = None) -> None:
        new_option = {}
        if verb is not None:
            new_option["verb"] = verb
        if connector is not None:
            new_option["connector"] = connector
        if subject is not None:
            new_option["subject"] = subject
        self.option_count += 1
        self.options[self.option_count] = new_option
        logging.debug(f"Option {self.option_count} '{verb + ' ' if verb is not None else ''}{connector + ' ' if connector is not None else ''}{subject if subject is not None else ''}' has been added to {self.title} menu.")

    def update_option(self, option_id: int, **kwargs) -> None:
        option = self.options.get(option_id)
        if option:
            # Remove keys not provided in kwargs
            option_keys = list(option.keys())
            for key in option_keys:
                if key not in kwargs:
                    option.pop(key, None)

            # Update keys provided in kwargs
            for key, value in kwargs.items():
                if value != "":
                    option[key] = value
        else:
            logging.warning(f"Option {option_id} does not exist in {self.title} menu.")

    def remove_option(self, option_id: int) -> None:
        if option_id == 0:
            logging.warning(f"Option {option_id} cannot be removed from {self.title} menu.")
        elif option_id in self.options:
            del self.options[option_id]
            self.option_count -= 1
            logging.debug(f"Option {option_id} has been removed from {self.title} menu.")
        else:
            logging.warning(f"Option {option_id} does not exist in {self.title} menu.")

    def get_valid_menu_choice(self) -> int:
        return UserInput.get_valid_menu_choice(self.option_count)

    def get_next_menu(self, choice: int):
        if self.menu_mapping is None:
            return None
        else:
            next_menu = self.menu_mapping.get(choice)
            if next_menu:
                return next_menu(self.dashboard)
            return None


# Login Menu class for managing the login menu
class Login(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "LOGIN"
        # Add new menu options
        self.add_option(verb="Create", connector="a", subject="New Account")
        self.add_option(verb="Log", connector="into", subject="Account")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
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
        self.title = "MAIN"
        self.previous_menu = Login(dashboard)
        # Add menu options
        self.add_option(subject="Portfolio Manager")
        self.add_option(subject="Account Settings")
        self.add_option(subject="Help and Information")
        self.add_option(subject="Save Changes")
        self.add_option(subject="Discard Changes")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: PortfolioManager,
            2: AccountSettings,
            3: HelpAndInformation,
            4: None,
            5: None,
            0: Login
        }
        self.menu_logic = {
            1: self.dashboard.portfolio_manager,
            2: self.dashboard.account_settings,
            3: self.dashboard.help_information,
            4: self.dashboard.save_changes,
            5: self.dashboard.discard_changes,
            0: self.dashboard.logout
        }


# PortfolioManager Menu class for managing the portfolio manager menu
class PortfolioManager(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.previous_menu = Main(dashboard)
        self.title = "PORTFOLIO MANAGER"
        # Add menu options
        self.add_option(verb="View", subject="Portfolio")
        self.add_option(verb="Manage", subject="Portfolio")
        self.add_option(verb="View", subject="Market Data")
        self.add_option(verb="Manage", subject="Market Data")
        self.add_option(subject="Statistical Analysis")
        self.add_option(subject="Trading Strategies")
        self.add_option(subject="Reports")
        self.add_option(subject="Export Data")
        self.add_option(subject="Automation")
        self.add_option(subject="Notifications")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ViewPortfolio,
            2: ManagePortfolio,
            3: ViewMarketData,
            4: ManageMarketData,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            0: Main
        }
        self.menu_logic = {
            1: self.dashboard.view_portfolio,
            2: self.dashboard.manage_portfolio,
            3: self.dashboard.view_market_data,
            4: self.dashboard.manage_market_data,
            5: self.dashboard.statistical_analysis,
            6: self.dashboard.trading_strategies,
            7: self.dashboard.reports,
            8: self.dashboard.export_data,
            9: self.dashboard.automation,
            10: self.dashboard.notifications,
            0: self.dashboard.previous_menu
        }


# ViewPortfolio Menu class for managing the view portfolio menu
class ViewPortfolio(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW PORTFOLIO"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="Portfolio Summary")
        self.add_option(verb="View", subject="Current Portfolio")
        self.add_option(verb="View", subject="Entire Portfolio History")
        self.add_option(verb="Search", subject="for Current Investment")
        self.add_option(verb="Search", subject="for Investment in Portfolio History")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ViewPortfolio,
            2: ViewPortfolio,
            3: ViewPortfolio,
            4: ViewPortfolio,
            5: ViewPortfolio,
            0: PortfolioManager
        }
        self.menu_logic = {
            1: self.dashboard.view_portfolio_summary,
            2: self.dashboard.view_current_portfolio,
            3: self.dashboard.view_entire_portfolio_history,
            4: self.dashboard.search_for_current_investment,
            5: self.dashboard.search_for_investment_in_portfolio_history,
            0: self.dashboard.previous_menu
        }


# ManagePortfolio Menu class for managing the manage portfolio menu
class ManagePortfolio(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MANAGE PORTFOLIO"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(verb="Build", subject="Portfolio from Data Set(s)")
        self.add_option(verb="Import", subject="Existing Portfolio Data Set")
        self.add_option(verb="Delete", subject="Existing Portfolio Data Set")
        self.add_option(verb="Manage", subject="Custom Import Scripts")
        self.add_option(verb="Add", subject="Investment Manually")
        self.add_option(verb="Modify", subject="Investment Entry")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: BuildPortfolio,
            2: ImportExistingPortfolio,
            3: None,
            4: None,
            5: None,
            6: None,
            0: PortfolioManager
        }
        self.menu_logic = {
            1: self.dashboard.build_portfolio_from_data_set,
            2: self.dashboard.import_existing_portfolio_data_set,
            3: self.dashboard.delete_existing_portfolio_data_set,
            4: self.dashboard.manage_custom_import_scripts,
            5: self.dashboard.add_investment_manually,
            6: self.dashboard.modify_investment_entry,
            0: self.dashboard.previous_menu
        }


# BuildPortfolio Menu class for managing the build portfolio menu
class BuildPortfolio(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "BUILD PORTFOLIO"
        self.previous_menu = ManagePortfolio(dashboard)
        # Add menu options
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
        # Add menu options
        self.add_option(verb="Import", subject="Existing Portfolio from Brokerage Account")
        self.add_option(verb="Import", subject="Existing Portfolio from CSV File")
        self.add_option(verb="Import", subject="Existing Portfolio from Excel File")
        self.add_option(verb="Import", subject="Existing Portfolio from PDF file")
        self.add_option(verb="Import", subject="Existing Portfolio from Database file")
        self.add_option(verb="Import", subject="Existing Portfolio from Email Account")
        self.add_option(verb="Import", subject="Existing Portfolio from Outlook Desktop App")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ImportExistingPortfolio,
            2: ImportExistingPortfolio,
            3: ImportExistingPortfolio,
            4: ImportExistingPortfolio,
            5: ImportExistingPortfolio,
            6: ImportExistingPortfolio,
            7: ImportExistingPortfolio,
            0: ManagePortfolio
        }
        self.menu_logic = {
            1: self.dashboard.import_existing_portfolio_from_brokerage_account,
            2: self.dashboard.import_existing_portfolio_from_csv_file,
            3: self.dashboard.import_existing_portfolio_from_excel_file,
            4: self.dashboard.import_existing_portfolio_from_pdf_file,
            5: self.dashboard.import_existing_portfolio_from_database_file,
            6: self.dashboard.import_existing_portfolio_from_email_account,
            7: self.dashboard.import_existing_portfolio_from_outlook_desktop_app,
            0: self.dashboard.previous_menu
        }


# # ImportFromBrokerageAccount Menu class for managing the import from brokerage account menu
# class ImportFromBrokerageAccount(Menu):
#     def __init__(self, dashboard: Dashboard) -> None:
#         super().__init__(dashboard)
#         self.title = "IMPORT FROM BROKERAGE ACCOUNT"
#         self.previous_menu = ImportExistingPortfolio(dashboard)
#         # Add menu options
#         self.options = {} # TODO - Add dynamic list of brokerage accounts to choose from
#         # TODO - finish this menu


# # ImportFromCSVFile Menu class for managing the import from CSV file menu
# class ImportFromCSVFile(Menu):
#     def __init__(self, dashboard: Dashboard) -> None:
#         super().__init__(dashboard)
#         self.title = "IMPORT FROM CSV FILE"
#         self.previous_menu = ImportExistingPortfolio(dashboard)
#         # Add menu options
#         self.options = {} # TODO - Add dynamic list of CSV files to choose from
#         # TODO - finish this menu


# # ImportFromExcelFile Menu class for managing the import from Excel file menu
# class ImportFromExcelFile(Menu):
#     def __init__(self, dashboard: Dashboard) -> None:
#         super().__init__(dashboard)
#         self.title = "IMPORT FROM EXCEL FILE"
#         self.previous_menu = ImportExistingPortfolio(dashboard)
#         # Add menu options
#         self.options = {} # TODO - Add dynamic list of Excel files to choose from
#         # TODO - finish this menu


# # ImportFromPDFFile Menu class for managing the import from PDF file menu
# class ImportFromPDFFile(Menu):
#     def __init__(self, dashboard: Dashboard) -> None:
#         super().__init__(dashboard)
#         self.title = "IMPORT FROM PDF FILE"
#         self.previous_menu = ImportExistingPortfolio(dashboard)
#         # Add menu options
#         self.options = {} # TODO - Add dynamic list of PDF files to choose from
#         # TODO - finish this menu


# # ImportFromDatabaseFile Menu class for managing the import from database file menu
# class ImportFromDatabaseFile(Menu):
#     def __init__(self, dashboard: Dashboard) -> None:
#         super().__init__(dashboard)
#         self.title = "IMPORT FROM DATABASE FILE"
#         self.previous_menu = ImportExistingPortfolio(dashboard)
#         # Add menu options
#         self.options = {} # TODO - Add dynamic list of database files to choose from
#         # TODO - finish this menu


# # ImportFromEmail Menu class for managing the import from email menu
# class ImportFromEmail(Menu):
#     def __init__(self, dashboard: Dashboard) -> None:
#         super().__init__(dashboard)
#         self.title = "IMPORT FROM EMAIL ACCOUNT"
#         self.previous_menu = ImportExistingPortfolio(dashboard)
#         self.menu_options = {}
#         # Get available email accounts
#         email_accounts = dashboard.get_available_email_accounts()
#         if email_accounts is None or len(email_accounts) == 0:
#             print("No available email accounts for importing.")
#             print("Please add an email account in the account settings.")
#             self.menu_mapping = {}
#             self.menu_logic = {}
#         else:
#             # Add menu options
#             for _, email_account in enumerate(email_accounts):
#                 self.add_option(subject=email_account.address)
#             # Format option 0
#             self.format_return_to_previous_menu_option()
#             self.menu_mapping = {
#                 0: ImportExistingPortfolio
#             }
#             self.menu_logic = {
#                 0: self.dashboard.import_existing_portfolio_from_email_account
#             }
#         self.format_return_to_previous_menu_option()


# class AvailableEmailAccounts(Menu): # TODO - finish this menu
#     def __init__(self, dashboard: Dashboard):
#         super().__init__(dashboard)
#         self.menu_title = "AVAILABLE EMAIL ACCOUNTS"
#         self.previous_menu = ImportFromEmail(dashboard)
#         self.menu_options = {}
#         email_accounts = dashboard.get_available_email_accounts()
#         if email_accounts is None or len(email_accounts) == 0:
#             self.menu_options[1] = "No Available Email Accounts"
#             self.menu_mapping = {
#                 0: ImportExistingPortfolio
#             }
#             self.menu_logic = {
#             0: self.dashboard.previous_menu
#             }
#         else:
#             for _, email_account in enumerate(email_accounts):
#                 self.add_option(subject=email_account.address)
#         self.format_return_to_previous_menu_option()
#         self.menu_mapping = {}
#         self.menu_logic = {}


# class AvailableEmailFolders(Menu): # TODO - finish this menu
#     def __init__(self, dashboard: Dashboard):
#         super().__init__(dashboard)
#         self.menu_title = "AVAILABLE EMAIL ACCOUNTS"
#         self.previous_menu = ImportFromEmail(dashboard)
#         self.menu_options = {}
#         email_folders = dashboard.get_available_email_folders()
#         for i in range(len(email_accounts)):
#             self.menu_options[i] = email_accounts[i].address
#         self.format_return_to_previous_menu_option()
#         self.menu_mapping = {}
#         self.menu_logic = {}
#         # for i in enumerate(email_accounts):
#         #     self.menu_options[i[0]] = i[1].address


# ManageCustomImportScripts Menu class for managing the manage custom import scripts menu
class ManageCustomImportScripts(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MANAGE CUSTOM IMPORT SCRIPTS"
        self.previous_menu = ManagePortfolio(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="Custom Import Scripts")
        self.add_option(verb="Add", subject="Custom Import Script")
        self.add_option(verb="Remove", subject="Custom Import Script")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: CustomImportScripts,
            2: AddCustomImportScript,
            3: RemoveCustomImportScript,
            0: ManagePortfolio
        }
        self.menu_logic = {
            1: self.dashboard.view_custom_import_scripts,
            2: self.dashboard.add_custom_import_script,
            3: self.dashboard.remove_custom_import_script,
            0: self.dashboard.previous_menu
        }


# AddCustomImportScript Menu class for managing the add custom import script menu
class AddCustomImportScript(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD CUSTOM IMPORT SCRIPT"
        self.previous_menu = ManageCustomImportScripts(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of scripts to choose from
        # TODO - finish this menu


# RemoveCustomImportScript Menu class for managing the remove custom import script menu
class RemoveCustomImportScript(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE CUSTOM IMPORT SCRIPT"
        self.previous_menu = ManageCustomImportScripts(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of scripts to choose from
        # TODO - finish this menu


# CustomImportScripts Menu class for managing the custom import scripts menu
class CustomImportScripts(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CUSTOM IMPORT SCRIPTS"
        self.options = {} # TODO - Add dynamic list of scripts to choose from


# ViewMarketData Menu class for managing the view market data menu
class ViewMarketData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW MARKET DATA"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="Macro Data")
        self.add_option(verb="View", subject="Default Market Data")
        self.add_option(verb="View", subject="Custom Market Data")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: PortfolioManager, # TODO - add macro data menu
            2: PortfolioManager, # TODO - add default market data menu
            3: PortfolioManager, # TODO - add custom market data menu
            0: PortfolioManager
        }
        self.menu_logic = {
            1: self.dashboard.previous_menu,
            2: self.dashboard.previous_menu,
            3: self.dashboard.previous_menu,
            0: self.dashboard.previous_menu
        }


# ManageMarketData Menu class for managing the manage market data menu
class ManageMarketData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MANAGE MARKET DATA"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(verb="Initialize", subject="Market Data")
        self.add_option(verb="Import", subject="Custom Market Data")
        self.add_option(verb="Modify", subject="Market Data")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: InitializeMarketData,
            2: ImportCustomMarketData,
            3: ModifyMarketData,
            0: PortfolioManager
        }
        self.menu_logic = {
            1: self.dashboard.initialize_market_data,
            2: self.dashboard.import_custom_market_data,
            3: self.dashboard.modify_market_data,
            0: self.dashboard.previous_menu
        }


# InitializeMarketData Menu class for managing the initialize market data menu
class InitializeMarketData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "INITIALIZE MARKET DATA"
        self.previous_menu = ManageMarketData(dashboard)
        # Add menu options
        # self.add_option(verb="Initialize", subject="Exchange Listings Data")
        self.add_option(verb="Initialize", subject="Asset Information Data")
        self.add_option(verb="Initialize", subject="Index Holdings Data")
        self.add_option(verb="Initialize", subject="Macro Data")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            # 1: InitializeExchangeListingsData,
            1: InitializeAssetInformationData,
            2: InitializeIndexHoldingsData,
            3: InitializeMacroData,
            0: ManageMarketData
        }
        self.menu_logic = {
            # 1: self.dashboard.menu_without_logic,
            1: self.dashboard.menu_without_logic,
            2: self.dashboard.initialize_index_holdings_data,
            3: self.dashboard.initialize_macro_data,
            0: self.dashboard.previous_menu
        }


# # InitializeExchangeListingsData Menu class for managing the initialize exchange listings data menu
# class InitializeExchangeListingsData(Menu):
#     def __init__(self, dashboard: Dashboard) -> None:
#         super().__init__(dashboard)
#         self.title = "INITIALIZE EXCHANGE LISTINGS DATA"
#         self.previous_menu = InitializeMarketData(dashboard)
#         # Add menu options
#         self.add_option(verb="Initialize", subject="All Default Exchange Listings Data")
#         self.add_option(verb="Initialize", subject="NASDAQ Listings Data")
#         self.add_option(verb="Initialize", subject="NYSE Listings Data")
#         self.add_option(verb="Initialize", subject="NYSE MKT Listings Data")
#         self.add_option(verb="Initialize", subject="NYSE ARCA Listings Data")
#         self.add_option(verb="Initialize", subject="BATS Listings Data")
#         self.add_option(verb="Initialize", subject="TSX Listings Data")
#         self.add_option(verb="Initialize", subject="TSXV Listings Data")
#         self.add_option(verb="Initialize", subject="CSE Listings Data")
#         self.add_option(verb="Initialize", subject="Cboe CA Listings Data")
#         # Format option 0
#         self.format_return_to_previous_menu_option()
#         self.menu_mapping = {
#             1: InitializeExchangeListingsData,
#             2: InitializeExchangeListingsData,
#             3: InitializeExchangeListingsData,
#             4: InitializeExchangeListingsData,
#             5: InitializeExchangeListingsData,
#             6: InitializeExchangeListingsData,
#             7: InitializeExchangeListingsData,
#             8: InitializeExchangeListingsData,
#             9: InitializeExchangeListingsData,
#             10: InitializeExchangeListingsData,
#             0: InitializeMarketData
#         }
#         self.menu_logic = { # TODO - add logic
#             1: self.dashboard.initialize_all_exchange_listings_data,
#             2: self.dashboard.initialize_nasdaq_listings_data,
#             3: self.dashboard.initialize_nyse_listings_data,
#             4: self.dashboard.initialize_nyse_mkt_listings_data,
#             5: self.dashboard.initialize_nyse_arca_listings_data,
#             6: self.dashboard.initialize_bats_listings_data,
#             7: self.dashboard.initialize_tsx_listings_data,
#             8: self.dashboard.initialize_tsxv_listings_data,
#             9: self.dashboard.initialize_cse_listings_data,
#             10: self.dashboard.initialize_cboe_canada_listings_data,
#             0: self.dashboard.previous_menu
#         }


# InitializeMarketData Menu class for managing the initialize market data menu
class InitializeAssetInformationData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "INITIALIZE ASSET INFORMATION DATA"
        self.previous_menu = InitializeMarketData(dashboard)
        # Add menu options
        self.add_option(verb="Initialize", subject="All Default Asset Information Data")
        self.add_option(verb="Initialize", subject="NASDAQ Asset Information Data")
        self.add_option(verb="Initialize", subject="NYSE Asset Information Data")
        self.add_option(verb="Initialize", subject="NYSE MKT Asset Information Data")
        self.add_option(verb="Initialize", subject="NYSE ARCA Asset Information Data")
        self.add_option(verb="Initialize", subject="BATS Asset Information Data")
        self.add_option(verb="Initialize", subject="TSX Asset Information Data")
        self.add_option(verb="Initialize", subject="TSXV Asset Information Data")
        self.add_option(verb="Initialize", subject="CSE Asset Information Data")
        self.add_option(verb="Initialize", subject="Cboe CA Asset Information Data")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: InitializeAssetInformationData,
            2: InitializeAssetInformationData,
            3: InitializeAssetInformationData,
            4: InitializeAssetInformationData,
            5: InitializeAssetInformationData,
            6: InitializeAssetInformationData,
            7: InitializeAssetInformationData,
            8: InitializeAssetInformationData,
            9: InitializeAssetInformationData,
            10: InitializeAssetInformationData,
            0: InitializeMarketData
        }
        self.menu_logic = { # TODO - add logic
            1: self.dashboard.initialize_all_asset_information_data,
            2: self.dashboard.initialize_nasdaq_asset_information_data,
            3: self.dashboard.initialize_nyse_asset_information_data,
            4: self.dashboard.initialize_nyse_mkt_asset_information_data,
            5: self.dashboard.initialize_nyse_arca_asset_information_data,
            6: self.dashboard.initialize_bats_asset_information_data,
            7: self.dashboard.initialize_tsx_asset_information_data,
            8: self.dashboard.initialize_tsxv_asset_information_data,
            9: self.dashboard.initialize_cse_asset_information_data,
            10: self.dashboard.initialize_cboe_canada_asset_information_data,
            0: self.dashboard.previous_menu
        }


# InitializeIndexHoldingsData Menu class for managing the initialize index holdings data menu
class InitializeIndexHoldingsData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "INITIALIZE INDEX HOLDINGS DATA"
        self.previous_menu = InitializeMarketData(dashboard)
        # Add menu options # TODO - add options
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = { # TODO - add mapping
            0: ManageMarketData
        }
        self.menu_logic = { # TODO - add logic
            0: self.dashboard.previous_menu
        }


# InitializeMacroData Menu class for managing the initialize macro data menu
class InitializeMacroData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "INITIALIZE MACRO DATA"
        self.previous_menu = InitializeMarketData(dashboard)
        # Add menu options # TODO - add options
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = { # TODO - add mapping
            0: ManageMarketData
        }
        self.menu_logic = { # TODO - add logic
            0: self.dashboard.previous_menu
        }


# ManageMarketData Menu class for managing the manage market data menu
class ImportCustomMarketData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT CUSTOM MARKET DATA"
        self.previous_menu = ManageMarketData(dashboard)
        # Add menu options
        self.add_option(verb="Import", subject="Market Data from CSV")
        self.add_option(verb="Import", subject="Market Data from Excel")
        self.add_option(verb="Import", subject="Market Data from Database")
        self.add_option(verb="Import", subject="Market Data from an API")
        self.add_option(verb="Import", subject="Market Data from Online Source")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ImportMarketDataFromCSV,
            2: ImportMarketDataFromExcel,
            3: ImportMarketDataFromDatabase,
            4: ImportMarketDataFromAPI,
            5: ImportMarketDataFromOnlineSource,
            0: ManageMarketData
        }
        self.menu_logic = {
            1: self.dashboard.import_market_data_from_csv,
            2: self.dashboard.import_market_data_from_excel,
            3: self.dashboard.import_market_data_from_database,
            4: self.dashboard.import_market_data_from_api,
            5: self.dashboard.import_market_data_from_online_source,
            0: self.dashboard.previous_menu
        }


# ImportMarketDataFromCSV Menu class for managing the import market data from CSV menu
class ImportMarketDataFromCSV(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT MARKET DATA FROM CSV"
        self.previous_menu = ImportCustomMarketData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of CSV files to choose from
        # TODO - finish this menu


# ImportMarketDataFromExcel Menu class for managing the import market data from Excel menu
class ImportMarketDataFromExcel(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT MARKET DATA FROM EXCEL"
        self.previous_menu = ImportCustomMarketData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of Excel files to choose from
        # TODO - finish this menu


# ImportMarketDataFromDatabase Menu class for managing the import market data from Excel menu
class ImportMarketDataFromDatabase(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT MARKET DATA FROM DATABASE"
        self.previous_menu = ImportCustomMarketData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of Database files to choose from
        # TODO - finish this menu


# ImportMarketDataFromAPI Menu class for managing the import market data from API menu
class ImportMarketDataFromAPI(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT MARKET DATA FROM API"
        self.previous_menu = ImportCustomMarketData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of APIs to choose from
        # TODO - finish this menu


# ImportMarketDataFromOnlineSource Menu class for managing the import market data from online source menu
class ImportMarketDataFromOnlineSource(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "IMPORT MARKET DATA FROM ONLINE SOURCE"
        self.previous_menu = ImportCustomMarketData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of online sources to choose from
        # TODO - finish this menu


# ModifyMarketData Menu class for managing the import market data from online source menu
class ModifyMarketData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY MARKET DATA"
        self.previous_menu = ManageMarketData(dashboard)
        # Add menu options
        self.add_option(verb="Modify", subject="Single Market Data Entry")
        self.add_option(verb="Modify", subject="Entire Market Data Column")
        self.add_option(verb="Modify", subject="Entire Market Data Table")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ModifySingleMarketDataEntry,
            2: ModifyEntireMarketDataColumn,
            3: ModifyEntireMarketDataTable,
            0: ManageMarketData
        }
        self.menu_logic = {
            1: self.dashboard.modify_single_market_data_entry,
            2: self.dashboard.modify_entire_market_data_column,
            3: self.dashboard.modify_entire_market_data_table,
            0: self.dashboard.previous_menu
        }


# ModifySingleMarketDataEntry Menu class for managing the modify single market data entry menu
class ModifySingleMarketDataEntry(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY SINGLE MARKET DATA ENTRY"
        self.previous_menu = ModifyMarketData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of online sources to choose from
        # TODO - finish this menu


# ModifyEntireMarketDataColumn Menu class for managing the modify entire market data column menu
class ModifyEntireMarketDataColumn(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY ENTIRE MARKET DATA COLUMN"
        self.previous_menu = ModifyMarketData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of online sources to choose from
        # TODO - finish this menu


# ModifyEntireMarketDataTable Menu class for managing the modify entire market data table menu
class ModifyEntireMarketDataTable(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY ENTIRE MARKET DATA TABLE"
        self.previous_menu = ModifyMarketData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of online sources to choose from
        # TODO - finish this menu


# StatisticalAnalysis Menu class for managing the statistical analysis menu
class StatisticalAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "STATISTICAL ANALYSIS"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(subject="Portfolio Overview")
        self.add_option(subject="Performance Analysis")
        self.add_option(subject="Risk Analysis")
        self.add_option(subject="Correlation Analysis")
        self.add_option(subject="Portfolio Optimization")
        self.add_option(subject="Portfolio Backtesting")
        self.add_option(subject="Portfolio Simulation")
        self.add_option(subject="Portfolio Forecasting")
        self.add_option(subject="Portfolio Stress Testing")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: PortfolioOverview,
            2: PerformanceAnalysis,
            3: RiskAnalysis,
            4: CorrelationAnalysis,
            5: PortfolioOptimization,
            6: PortfolioBacktesting,
            7: PortfolioSimulation,
            8: PortfolioForecasting,
            9: PortfolioStressTesting,
            0: PortfolioManager
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
            9: self.dashboard.portfolio_stress_testing,
            0: self.dashboard.previous_menu
        }


# PortfolioOverview Menu class for managing the portfolio overview menu
class PortfolioOverview(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO OVERVIEW"
        self.previous_menu = StatisticalAnalysis(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PerformanceAnalysis Menu class for managing the performance analysis menu
class PerformanceAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PERFORMANCE ANALYSIS"
        self.previous_menu = StatisticalAnalysis(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# RiskAnalysis Menu class for managing the risk analysis menu
class RiskAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "RISK ANALYSIS"
        self.previous_menu = StatisticalAnalysis(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# CorrelationAnalysis Menu class for managing the correlation analysis menu
class CorrelationAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CORRELATION ANALYSIS"
        self.previous_menu = StatisticalAnalysis(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioOptimization Menu class for managing the portfolio optimization menu
class PortfolioOptimization(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO OPTIMIZATION"
        self.previous_menu = StatisticalAnalysis(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioBacktesting Menu class for managing the portfolio backtesting menu
class PortfolioBacktesting(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO BACKTESTING"
        self.previous_menu = StatisticalAnalysis(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioSimulation Menu class for managing the portfolio simulation menu
class PortfolioSimulation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO SIMULATION"
        self.previous_menu = StatisticalAnalysis(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioForecasting Menu class for managing the portfolio forecasting menu
class PortfolioForecasting(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO FORECASTING"
        self.previous_menu = StatisticalAnalysis(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# PortfolioStressTesting Menu class for managing the portfolio stress testing menu
class PortfolioStressTesting(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "PORTFOLIO STRESS TESTING"
        self.previous_menu = StatisticalAnalysis(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of investments to choose from
        # TODO - finish this menu


# TradingStrategies Menu class for managing the trading strategies menu
class TradingStrategies(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "TRADING STRATEGIES"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="Current Trading Strategies")
        self.add_option(verb="Add", subject="Trading Strategy")
        self.add_option(verb="Modify", subject="Trading Strategy")
        self.add_option(verb="Remove", subject="Trading Strategy")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: CurrentTradingStrategies,
            2: AddTradingStrategy,
            3: ModifyTradingStrategy,
            4: RemoveTradingStrategy,
            0: PortfolioManager
        }
        self.menu_logic = {
            1: self.dashboard.current_trading_strategies,
            2: self.dashboard.add_trading_strategy,
            3: self.dashboard.modify_trading_strategy,
            4: self.dashboard.remove_trading_strategy,
            0: self.dashboard.previous_menu
        }


# CurrentTradingStrategies Menu class for managing the current trading strategies menu
class CurrentTradingStrategies(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CURRENT TRADING STRATEGIES"
        self.previous_menu = TradingStrategies(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of trading strategies to choose from
        # TODO - finish this menu


# AddTradingStrategy Menu class for managing the add trading strategy menu
class AddTradingStrategy(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD TRADING STRATEGY"
        self.previous_menu = TradingStrategies(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of trading strategies to choose from
        # TODO - finish this menu


# ModifyTradingStrategy Menu class for managing the modify trading strategy menu
class ModifyTradingStrategy(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY TRADING STRATEGY"
        self.previous_menu = TradingStrategies(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of trading strategies to choose from
        # TODO - finish this menu


# RemoveTradingStrategy Menu class for managing the remove trading strategy menu
class RemoveTradingStrategy(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE TRADING STRATEGY"
        self.previous_menu = TradingStrategies(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of trading strategies to choose from
        # TODO - finish this menu


# Reports Menu class for managing the reports menu
class Reports(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REPORTS"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="Current Reports")
        self.add_option(verb="Add", subject="Report")
        self.add_option(verb="Modify", subject="Report")
        self.add_option(verb="Remove", subject="Report")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ViewCurrentReports,
            2: AddReport,
            3: ModifyReport,
            4: RemoveReport,
            0: PortfolioManager
        }
        self.menu_logic = {
            1: self.dashboard.view_current_reports,
            2: self.dashboard.add_report,
            3: self.dashboard.modify_report,
            4: self.dashboard.remove_report,
            0: self.dashboard.previous_menu
        }


# ViewCurrentReports Menu class for managing the view current reports menu
class ViewCurrentReports(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW CURRENT REPORTS"
        self.previous_menu = Reports(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# AddReport Menu class for managing the add report menu
class AddReport(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD REPORT"
        self.previous_menu = Reports(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ModifyReport Menu class for managing the modify report menu
class ModifyReport(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY REPORT"
        self.previous_menu = Reports(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# RemoveReport Menu class for managing the remove report menu
class RemoveReport(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE REPORT"
        self.previous_menu = Reports(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportData Menu class for managing the export data menu
class ExportData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT DATA"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(verb="Export", subject="Portfolio Data")
        self.add_option(verb="Export", subject="Market Data")
        self.add_option(verb="Export", subject="Statistical Analysis")
        self.add_option(verb="Export", subject="Trading Strategies")
        self.add_option(verb="Export", subject="Reports")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ExportPortfolioData,
            2: ExportMarketData,
            3: ExportStatisticalAnalysis,
            4: ExportTradingStrategies,
            5: ExportReports,
            0: PortfolioManager
        }
        self.menu_logic = {
            1: self.dashboard.export_portfolio_data,
            2: self.dashboard.export_market_data,
            3: self.dashboard.export_statistical_analysis,
            4: self.dashboard.export_trading_strategies,
            5: self.dashboard.export_reports,
            0: self.dashboard.previous_menu
        }


# ExportPortfolioData Menu class for managing the export portfolio data menu
class ExportPortfolioData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT PORTFOLIO DATA"
        self.previous_menu = ExportData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportMarketData Menu class for managing the export market data menu
class ExportMarketData(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT MARKET DATA"
        self.previous_menu = ExportData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportStatisticalAnalysis Menu class for managing the export statistical analysis menu
class ExportStatisticalAnalysis(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT STATISTICAL ANALYSIS"
        self.previous_menu = ExportData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportTradingStrategies Menu class for managing the export trading strategies menu
class ExportTradingStrategies(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT TRADING STRATEGIES"
        self.previous_menu = ExportData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# ExportReports Menu class for managing the export reports menu
class ExportReports(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "EXPORT REPORTS"
        self.previous_menu = ExportData(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of reports to choose from
        # TODO - finish this menu


# Automation Menu class for managing the automation menu
class Automation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "AUTOMATION"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="Current Automations")
        self.add_option(verb="Add", subject="Automation")
        self.add_option(verb="Modify", subject="Automation")
        self.add_option(verb="Remove", subject="Automation")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ViewAutomations,
            2: AddAutomation,
            3: ModifyAutomation,
            4: RemoveAutomation,
            0: PortfolioManager
        }
        self.menu_logic = {
            1: self.dashboard.view_automations,
            2: self.dashboard.add_automation,
            3: self.dashboard.modify_automation,
            4: self.dashboard.remove_automation,
            0: self.dashboard.previous_menu
        }


# ViewAutomations Menu class for managing the view automations menu
class ViewAutomations(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW AUTOMATIONS"
        self.previous_menu = Automation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of automations to choose from
        # TODO - finish this menu


# AddAutomation Menu class for managing the add automation menu
class AddAutomation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD AUTOMATION"
        self.previous_menu = Automation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of automations to choose from
        # TODO - finish this menu


# ModifyAutomation Menu class for managing the modify automation menu
class ModifyAutomation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY AUTOMATION"
        self.previous_menu = Automation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of automations to choose from
        # TODO - finish this menu


# RemoveAutomation Menu class for managing the remove automation menu
class RemoveAutomation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE AUTOMATION"
        self.previous_menu = Automation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of automations to choose from
        # TODO - finish this menu


# Notifications Menu class for managing the notifications menu
class Notifications(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "NOTIFICATIONS"
        self.previous_menu = PortfolioManager(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="Current Notifications")
        self.add_option(verb="Add", subject="Notification")
        self.add_option(verb="Modify", subject="Notification")
        self.add_option(verb="Remove", subject="Notification")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ViewNotifications,
            2: AddNotification,
            3: ModifyNotification,
            4: RemoveNotification,
            0: PortfolioManager
        }
        self.menu_logic = {
            1: self.dashboard.view_notifications,
            2: self.dashboard.add_notification,
            3: self.dashboard.modify_notification,
            4: self.dashboard.remove_notification,
            0: self.dashboard.previous_menu
        }


# ViewNotifications Menu class for managing the view notifications menu
class ViewNotifications(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW NOTIFICATIONS"
        self.previous_menu = Notifications(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of notifications to choose from
        # TODO - finish this menu


# AddNotification Menu class for managing the add notification menu
class AddNotification(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ADD NOTIFICATION"
        self.previous_menu = Notifications(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of notifications to choose from
        # TODO - finish this menu


# ModifyNotification Menu class for managing the modify notification menu
class ModifyNotification(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MODIFY NOTIFICATION"
        self.previous_menu = Notifications(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of notifications to choose from
        # TODO - finish this menu


# RemoveNotification Menu class for managing the remove notification menu
class RemoveNotification(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REMOVE NOTIFICATION"
        self.previous_menu = Notifications(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of notifications to choose from
        # TODO - finish this menu


# AccountSettings Menu class for managing the account settings menu
class AccountSettings(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ACCOUNT SETTINGS"
        self.previous_menu = Main(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="User Details")
        self.add_option(verb="Manage", subject="Email Accounts")
        self.add_option(verb="Change", subject="Account Username")
        self.add_option(verb="Change", subject="Account Password")
        self.add_option(verb="Delete", subject="Account")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: AccountSettings,
            2: ManageEmailAccounts,
            3: ChangeAccountUsername,
            4: ChangeAccountPassword,
            5: DeleteAccount,
            0: Main
        }
        self.menu_logic = {
            1: self.dashboard.view_user_details,
            2: self.dashboard.manage_email_accounts,
            3: self.dashboard.change_account_username,
            4: self.dashboard.change_account_password,
            5: self.dashboard.delete_account,
            0: self.dashboard.previous_menu
        }


# ViewUserDetails Menu class for managing the user's email accounts
class ManageEmailAccounts(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "MANAGE EMAIL ACCOUNTS"
        self.previous_menu = AccountSettings(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="Current Email Accounts")
        self.add_option(verb="Add", subject="Email Account")
        self.add_option(verb="Remove", subject="Email Account")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ManageEmailAccounts,
            2: ManageEmailAccounts,
            3: ManageEmailAccounts,
            0: AccountSettings
        }
        self.menu_logic = {
            1: self.dashboard.view_current_email_accounts,
            2: self.dashboard.add_email_account,
            3: self.dashboard.remove_email_account,
            0: self.dashboard.previous_menu
        }


# # AddEmailAccount Menu class for managing the add email account menu
# class AddEmailAccount(Menu):
#     def __init__(self, dashboard: Dashboard) -> None:
#         super().__init__(dashboard)
#         self.title = "ADD EMAIL ACCOUNT"
#         self.previous_menu = ManageEmailAccounts(dashboard)
#         # Add menu options
#         self.options = {} # TODO - Add dynamic list of email accounts to choose from
#         # TODO - finish this menu


# # RemoveEmailAccount Menu class for managing the remove email account menu
# class RemoveEmailAccount(Menu):
#     def __init__(self, dashboard: Dashboard) -> None:
#         super().__init__(dashboard)
#         self.title = "REMOVE EMAIL ACCOUNT"
#         self.previous_menu = ManageEmailAccounts(dashboard)
#         # Add menu options
#         self.options = {} # TODO - Add dynamic list of email accounts to choose from
#         # TODO - finish this menu


# ChangeAccountUsername Menu class for managing the change account username menu
class ChangeAccountUsername(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CHANGE ACCOUNT USERNAME"
        self.previous_menu = AccountSettings(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of email accounts to choose from
        # TODO - finish this menu


# ChangeAccountPassword Menu class for managing the change account password menu
class ChangeAccountPassword(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CHANGE ACCOUNT PASSWORD"
        self.previous_menu = AccountSettings(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of email accounts to choose from
        # TODO - finish this menu


# DeleteAccount Menu class for managing the delete account menu
class DeleteAccount(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "DELETE ACCOUNT"
        self.previous_menu = AccountSettings(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of email accounts to choose from
        # TODO - finish this menu


# HelpAndInformation Menu class for managing the help and information menu
class HelpAndInformation(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "HELP AND INFORMATION"
        self.previous_menu = Main(dashboard)
        # Add menu options
        self.add_option(verb="View", subject="User Manual")
        self.add_option(verb="View", subject="FAQ")
        self.add_option(verb="View", subject="Glossary")
        self.add_option(subject="About")
        self.add_option(subject="Contact Us")
        self.add_option(verb="Report", subject="a Bug")
        self.add_option(verb="Request", subject="a Feature")
        self.add_option(verb="View", subject="the License")
        # Format option 0
        self.format_return_to_previous_menu_option()
        self.menu_mapping = {
            1: ViewUserManual,
            2: ViewFAQ,
            3: ViewGlossary,
            4: About,
            5: ContactUs,
            6: ReportBug,
            7: RequestFeature,
            8: ViewLicense,
            0: Main
        }
        self.menu_logic = {
            1: self.dashboard.view_user_manual,
            2: self.dashboard.view_faq,
            3: self.dashboard.view_glossary,
            4: self.dashboard.about,
            5: self.dashboard.contact_us,
            6: self.dashboard.report_bug,
            7: self.dashboard.request_feature,
            8: self.dashboard.view_license,
            0: self.dashboard.previous_menu
        }


# ViewUserManual Menu class for managing the view user manual menu
class ViewUserManual(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW USER MANUAL"
        self.previous_menu = HelpAndInformation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of user manual pages to choose from
        # TODO - finish this menu


# ViewFAQ Menu class for managing the view FAQ menu
class ViewFAQ(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW FAQ"
        self.previous_menu = HelpAndInformation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of FAQ pages to choose from
        # TODO - finish this menu


# ViewGlossary Menu class for managing the view glossary menu
class ViewGlossary(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW GLOSSARY"
        self.previous_menu = HelpAndInformation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of glossary pages to choose from
        # TODO - finish this menu


# About Menu class for managing the about menu
class About(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "ABOUT"
        self.previous_menu = HelpAndInformation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of about pages to choose from
        # TODO - finish this menu


# ContactUs Menu class for managing the contact us menu
class ContactUs(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "CONTACT US"
        self.previous_menu = HelpAndInformation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of contact us pages to choose from
        # TODO - finish this menu


# ReportBug Menu class for managing the report bug menu
class ReportBug(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REPORT A BUG"
        self.previous_menu = HelpAndInformation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of report bug pages to choose from
        # TODO - finish this menu


# RequestFeature Menu class for managing the request feature menu
class RequestFeature(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "REQUEST A FEATURE"
        self.previous_menu = HelpAndInformation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of request feature pages to choose from
        # TODO - finish this menu


# ViewLicense Menu class for managing the view license menu
class ViewLicense(Menu):
    def __init__(self, dashboard: Dashboard) -> None:
        super().__init__(dashboard)
        self.title = "VIEW LICENSE"
        self.previous_menu = HelpAndInformation(dashboard)
        # Add menu options
        self.options = {} # TODO - Add dynamic list of license pages to choose from
        # TODO - finish this menu


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
