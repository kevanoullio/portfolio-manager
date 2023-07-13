# Purpose: Login Dashboard module for managing the user interface for the login process.

# Standard Libraries

# Third-party Libraries

# Local Modules
from session.session_manager import SessionManager
from user_authentication.authentication import UserAuthentication
from user_authentication.login_manager import LoginManager

# Configure logging
import logging
from config import configure_logging
configure_logging()


# LoginDashboard class for managing the login process
class LoginDashboard:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager
        self.database = self.session_manager.database
        self.user_auth = UserAuthentication(self.session_manager, self.database.query_executor)
        self.login_manager = LoginManager(self.session_manager, self.user_auth)
    

    def __valid_input(self, choice: str, min_choice: int, max_choice: int) -> bool:
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
        while self.session_manager.login_db_is_running:
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
                    self.session_manager.main_db_is_running = True
            elif choice == 2:
                self.login_manager.login()
                if self.session_manager.current_user is not None:
                    self.session_manager.main_db_is_running = True
            elif choice == 0:
                self.session_manager.login_db_is_running = False
                logging.info("Login Dashboard has stopped running.")


    def run(self) -> None:
        self.session_manager.login_db_is_running = True
        logging.info("Login Dashboard has started running.")
        self.__handle_login_menu()


if __name__ == "__main__":
    pass
