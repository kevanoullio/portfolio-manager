# Purpose: Container module for importing and organizing all necessary local modules

# Standard Libraries

# Third-party Libraries

# Local Modules
from database_management.database import Database
from access_management.login_manager import LoginManager
from user_interface.dashboard import Dashboard

# # Configure logging
# import logging


# Container class for importing and organizing all necessary local modules
class MainContainer:
    def __init__(self, db_filename: str, db_schema_filename: str) -> None:
        self.database = Database(db_filename, db_schema_filename)
        self.login_manager = LoginManager(self.database)
        self.dashboard = Dashboard(self.database, self.login_manager)


# TestContainer class for importing and organizing all necessary local modules
class TestContainer:
    def __init__(self, db_filename: str, db_schema_filename: str) -> None:
        self.database = Database(db_filename, db_schema_filename)
        self.login_manager = LoginManager(self.database)
        self.dashboard = Dashboard(self.database, self.login_manager)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
