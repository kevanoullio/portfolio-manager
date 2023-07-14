# Purpose: Dashboard module for managing the user interface and all menu navigation.

# Standard Libraries

# Third-party Libraries

# Local Modules
from session.session_manager import SessionManager
from user_authentication.authentication import UserAuthentication
from user_authentication.login_manager import LoginManager
from user_interface import menu

# Configure logging
import logging


# Dashboard class for managing the user interface and all menu navigation
class Dashboard:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager
        self.database = self.session_manager.database
        self.user_authentication = UserAuthentication(self.session_manager, self.database.query_executor)
        self.login_manager = LoginManager(self.session_manager, self.user_authentication)
        self.login_menu = menu.Login()
    
    def run(self) -> None:
        self.session_manager.login_db_is_running = True
        logging.info("Login Dashboard has started running.")
        self.handle_menu(self.login_menu)


    def __print_welcome_screen(self):
        print("\n====================================")
        print("|| Welcome to 'PORTFOLIO MANAGER' ||")
        print("====================================")


    def handle_menu(self, menu):
        while self.session_manager.login_db_is_running:
            if not self.session_manager.main_db_is_running:
                self.__print_welcome_screen()
                menu.print_options()
                choice = input("\nPlease enter your choice: ")

                # Check if the input is valid
                while not choice.isdigit() or choice.isdigit() < 0 or choice.isdigit() > len(menu.option_count):
                    print("Invalid input. Please try again: ", end="")
                    choice = input()

                choice = int(choice)
                if choice == 0:
                    self.session_manager.exit_program()
                else:
                    selected_option = menu.options[choice - 1]
                    if selected_option["action"] == "create_account":
                        self.login_manager.create_account()
                        if self.session_manager.current_user is not None:
                            logging.info(f"User created and logged in: {self.session_manager.current_user.username}")
                            self.main_dashboard.run()
                    elif selected_option["action"] == "login":
                        self.login_manager.login()
                        if self.session_manager.current_user is not None:
                            logging.info(f"User login: {self.session_manager.current_user.username}")
                            self.main_dashboard.run()



