# Purpose: Session Manager module for managing the current session state.

# Standard Libraries

# Third-party Libraries

# Local Modules
from user_authentication.user import User

# Configure logging
import logging
from config import configure_logging
configure_logging()


# SessionManager class for managing the current user session
class SessionManager:
    def __init__(self):
        self.__login_db_is_running: bool = False
        self.__main_db_is_running: bool = False
        self.current_user: User | None = None
        self.logged_in: bool = False


    def set_login_db_is_running(self, login_db_is_running: bool) -> None:
        self.__login_db_is_running = login_db_is_running
        logging.debug(f"Login DB is running: {self.__login_db_is_running}")

    
    def login_db_is_running(self) -> bool:
        return self.__login_db_is_running
    

    def set_main_db_is_running(self, main_db_is_running: bool) -> None:
        self.__main_db_is_running = main_db_is_running
        logging.debug(f"Main DB is running: {self.__main_db_is_running}")

    
    def main_db_is_running(self) -> bool:
        return self.__main_db_is_running
    

    def get_current_user(self) -> User | None:
        return self.current_user


    def user_logging_in(self, current_user: User) -> None:
        self.current_user = current_user
        self.logged_in = True


    def user_logging_out(self):
        self.current_user = None
        self.logged_in = False
