# Purpose: Login Dashboard module for managing the user interface for the login process.

# Standard Libraries

# Third-party Libraries

# Local Modules
from data_management.database import Database
from session.session_manager import SessionManager
from user_authentication.authentication import UserAuthentication
from user_authentication.login_manager import LoginManager

# Configure logging
import logging
from config import configure_logging
configure_logging()


# LoginDashboard class for managing the login process
class LoginDashboard:
    def __init__(self, session_manager: SessionManager, db_filename: str) -> None:
        self.session_manager = session_manager
        self.db_filename = db_filename
        self.database = Database(self.session_manager, self.db_filename)
        self.user_auth = UserAuthentication(self.session_manager, self.database.query_executor)
        self.login_manager = LoginManager(self.session_manager, self.user_auth)
    

    def valid_input(self, choice: str, min_choice: int, max_choice: int) -> bool:
        if not choice.isdigit() or int(choice) < min_choice or int(choice) > max_choice:
            return False
        return True
    

    def __print_login_menu(self):
        print("\n====================================")
        print("|| Welcome to 'PORTFOLIO MANAGER' ||")
        print("====================================")
        print("\nLOGIN MENU")
        print("-----------")
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")


    def __handle_login_menu(self):
        while self.session_manager.login_db_is_running():
            logging.info("Login Dashboard is running.")
            self.__print_login_menu()
            choice = input("\nPlease enter your choice: ")
            # Check if the input is valid
            while not self.valid_input(choice, 0, 2):
                print("Invalid input. Please try again: ", end="")
                choice = input()

            choice = int(choice)
            if choice == 1:
                self.login_manager.create_account()
                if self.session_manager.current_user is not None:
                    self.session_manager.set_main_db_is_running(True)
            elif choice == 2:
                self.login_manager.login()
                if self.session_manager.current_user is not None:
                    self.session_manager.set_main_db_is_running(True)
            elif choice == 0:
                self.login_manager.logout()
                if self.session_manager.current_user is None:
                    self.session_manager.set_login_db_is_running(False)


    def run(self) -> None:
        self.session_manager.set_login_db_is_running(True)
        self.__handle_login_menu()


    def show_error_message(self) -> None:
        # Logic to display an error message for failed authentication
        pass
