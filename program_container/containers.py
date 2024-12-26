# Purpose: Container module for importing and organizing all necessary local modules

# Standard Libraries

# Third-party Libraries

# Local Modules
from database_management.database import Database
from user_interface.user_input import UserInput
from access_management.login_manager import LoginManager
from user_interface.dashboard import Dashboard

# Configure logging
import logging


# Container class for importing and organizing all necessary local modules
class MainContainer:
	def __init__(self, db_filename: str, db_schema_filename: str) -> None:
		self.__database = Database(db_filename, db_schema_filename)
		self.__login_manager = LoginManager(self.__database)
		self.__dashboard = Dashboard(self.__database, self.__login_manager)
		logging.debug("Program Container created.")

	def start_database(self) -> None:
		self.__database.start()
		logging.debug("Database started.")

	def run_dashboard(self) -> None:
		self.__dashboard.run()
		logging.debug("Dashboard started.")

# TestContainer class for importing and organizing all necessary local modules in a test environment
class TestContainer:
	def __init__(self, db_filename: str, db_schema_filename: str) -> None:
		self.__database = Database(db_filename, db_schema_filename)
		self.__login_manager = LoginManager(self.__database)
		self.__dashboard = Dashboard(self.__database, self.__login_manager)
		logging.debug("Test Container created.")

	def start_database(self) -> None:
		self.__database.start()
		logging.debug("Database started.")

	def run_dashboard(self) -> None:
		self.__dashboard.run()
		logging.debug("Dashboard started.")


if __name__ == "__main__":
	print("This module is not meant to be executed directly.")
