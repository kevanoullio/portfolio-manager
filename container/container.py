# Purpose: Container module for importing and organizing all necessary local modules

# Standard Libraries

# Third-party Libraries

# Local Modules
from data_management.database import Database
from access_management.login_manager import LoginManager
from session_management.session_manager import SessionManager
from user_interface.dashboard import Dashboard

# Configure logging
import logging


# Container class for importing and organizing all necessary local modules
class Container:
    def __init__(self, db_filename: str) -> None:
        self.database = Database(db_filename)
        self.login_manager = LoginManager(self.database)
        self.session_manager = SessionManager(self.login_manager)
        self.dashboard = Dashboard(self.session_manager, self.database)


# TestContainer class for importing and organizing all necessary local modules
class TestContainer:
    def __init__(self, db_filename: str) -> None:
        self.database = Database(db_filename)
        self.login_manager = LoginManager(self.database)
        self.session_manager = SessionManager(self.login_manager)
        self.dashboard = Dashboard(self.session_manager, self.database)