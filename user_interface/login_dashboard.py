# Purpose: Login Dashboard module for managing the user interface for the login process.

# Standard Libraries

# Third-party Libraries

# Local Modules
from session.session_manager import SessionManager
from user_authentication.authentication import UserAuthentication
from user_authentication.login_manager import LoginManager
from user_interface.main_dashboard import MainDashboard

# Configure logging
import logging


# LoginDashboard class for managing the login process
class LoginDashboard:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager
        self.database = self.session_manager.database
        self.user_authentication = UserAuthentication(self.session_manager, self.database.query_executor)
        self.login_manager = LoginManager(self.session_manager, self.user_authentication)
        self.main_dashboard = MainDashboard(self.session_manager, self.login_manager)
    

    def __valid_input(self, choice: str, min_choice: int, max_choice: int) -> bool:
        if not choice.isdigit() or int(choice) < min_choice or int(choice) > max_choice:
            return False
        return True


    def run(self) -> None:
        self.session_manager.login_db_is_running = True
        logging.info("Login Dashboard has started running.")
        self.__handle_login_menu()


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
        while self.session_manager.login_db_is_running:
            if not self.session_manager.main_db_is_running:
                self.__print_login_menu()
                choice = input("\nPlease enter your choice: ")
                # Check if the input is valid
                while not self.__valid_input(choice, 0, 2):
                    print("Invalid input. Please try again: ", end="")
                    choice = input()

                choice = int(choice)
                if choice == 1:
                    self.login_manager.create_account()
                    if self.session_manager.current_user is not None:
                        logging.debug(f"User created and logged in: {self.session_manager.current_user.username}")
                        self.main_dashboard.run()
                elif choice == 2:
                    self.login_manager.login()
                    if self.session_manager.current_user is not None:
                        logging.debug(f"User login: {self.session_manager.current_user.username}")
                        self.main_dashboard.run()
                elif choice == 0:
                    self.session_manager.exit_program()

                    


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
