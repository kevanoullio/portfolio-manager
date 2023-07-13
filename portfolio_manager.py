# Purpose: Main entry point for the portfolio manager application.

# Standard Libraries
import os
import shutil

# Third-party Libraries

# Local Modules
from data_management.database import Database
from session.session_manager import SessionManager
from user_interface.login_dashboard import LoginDashboard

# Configure logging
import logging
from config import configure_logging
configure_logging()


# Main entry point for the portfolio manager application
def main():
    logging.info("Starting the portfolio manager application.")
    # Create the data folder if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Set the database filename
    db_filename = "./data/database.db"
    # # Set the temporary database filename
    # tmp_db_filename = "./data/tmp_database.db"

    # Check if the database file exists
    if os.path.isfile(db_filename):
        # If the database file exists, create a database object
        database = Database(db_filename)
        # Open the database connection
        database.db_connection.open_connection()
    else:
        # If the database file doesn't exist, create a database object
        database = Database(db_filename)
        # Open the database connection
        database.db_connection.open_connection()
        # Initialize the database
        database.db_schema.initialize_database("./database/schema.sql")
        # # Close the database connection
        # database.db_connection.close_connection()


    # Create the session manager
    session_manager = SessionManager(database)
    # Create the login dashboard object
    login_dashboard = LoginDashboard(session_manager)
    user_id = session_manager.current_user.user_id if session_manager.current_user is not None else None
    logging.debug(f"User ID check prior to dashboard running: {user_id}")
    # Run the login dashboard
    login_dashboard.run()
    logging.debug("Checkpoint 1: login_dashboard.run() finished")


    # # Check if the temporary database file exists
    # if os.path.isfile(tmp_db_filename):
    #     # If the tmp_database file exists, ask the user if they want to load the tmp_database file
    #     print("Unexpected shutdown detected in your last session.")
    #     load_tmp_database = input("Do you want to recover the data from your last session? (y/n): ")
    #     if load_tmp_database.lower() == "y":
    #         shutil.copy2(tmp_db_filename, db_filename)
    #         print("Temporary database file loaded successfully.")
    #     else:
    #         discard_changes = input("Do you want to discard the data from your last session? (y/n): ")
    #         if discard_changes.lower() == "y":
    #             os.remove(tmp_db_filename)
    #             print("Temporary database file discarded.")
    #             # After discarding the temporary database, create a new one
    #             shutil.copy2(db_filename, tmp_db_filename)
    # else:
    #     # If the tmp_database file doesn't exist, create a tmp_database file
    #     shutil.copy2(db_filename, tmp_db_filename)

    # # Create a tmp_database object
    # tmp_database = Database(tmp_db_filename)
    # # Open the tmp_database connection
    # tmp_database.db_connection.open_connection()
    # logging.debug("Checkpoint 2: tmp_database created and opened")


    # # Check if the login database is running
    # while session_manager.login_db_is_running:
    #     # Get the current user id
    #     user_id = session_manager.current_user.user_id if session_manager.current_user is not None else None
    #     # If user is authenticated, instantiate the MainDashboard object
    #     logging.debug(f"User ID check after dashboard running: {user_id}")
    #     if user_id is not None:
    #         main_dashboard = MainDashboard(session_manager, login_dashboard.login_manager)
    #         main_dashboard.run()


    # # User decides to save the changes
    # # TODO - Make sure if program quits unexpectedly, the tmp_database file is opened and the user is prompted to save the changes
    # save_changes = input("Do you want to save the changes? (y/n): ")
    # if save_changes.lower() == "y":
    #     shutil.copy2(tmp_db_filename, db_filename)
    #     print("Changes saved successfully.")
    #     os.remove(tmp_db_filename)
    # else:
    #     discard_changes = input("Do you want to discard the changes? (y/n): ")
    #     if discard_changes.lower() == "y":
    #         os.remove(tmp_db_filename)
    #         print("Changes discarded.")


    # Close the database connections
    database.db_connection.close_connection()
    # tmp_database.db_connection.close_connection()


if __name__ == "__main__":
    main()
