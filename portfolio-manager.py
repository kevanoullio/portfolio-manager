# Purpose: Main entry point for the portfolio manager application.

# Standard Libraries
import logging
import os
import shutil

# Third-party Libraries

# Local Modules
from database.database import Database
from dashboard.dashboard import Dashboard


def print_vs_logging():
    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")
    logging.error("error")


def main():
    # Configure logging
    level = logging.DEBUG
    format = "[%(levelname)s] %(asctime)s - %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    filename = "portfolio-manager.log"
    logging.basicConfig(level=level, format=format, datefmt=datefmt, filename=filename)

    # Create the user_data folder if it doesn't exist
    if not os.path.exists("user_data"):
        os.makedirs("user_data")
    
    # Declare database as None initially
    database = None
    db_filename = "./user_data/database.db"

    # Declare tmp_database as None initially
    tmp_database = None
    tmp_db_filename = "./user_data/tmp_database.db"

    # Check if the database file exists
    if not os.path.isfile(db_filename):
        # If the database file doesn't exist, create a database object
        database = Database(db_filename)
        # Open the database connection
        database.open_connection()
        # Initialize the database
        database.initialize_database("./database/schema.sql")
    else:
        # If the database file exists, create a database object
        database = Database(db_filename)
        # Open the database connection
        database.open_connection()

    # Check if the temporary database file exists
    if os.path.isfile(tmp_db_filename):
        # If the tmp_database file exists, ask the user if they want to load the tmp_database file
        print("Unexpected shutdown detected in your last session.")
        load_tmp_database = input("Do you want to recover the data from your last session? (y/n): ")
        if load_tmp_database.lower() == "y":
            shutil.copy2(tmp_db_filename, db_filename)
            print("Temporary database file loaded successfully.")
        else:
            discard_changes = input("Do you want to discard the data from your last session? (y/n): ")
            if discard_changes.lower() == "y":
                os.remove(tmp_db_filename)
                print("Temporary database file discarded.")
                # After discarding the temporary database, create a new one
                shutil.copy2(db_filename, tmp_db_filename)
    else:
        # If the tmp_database file doesn't exist, create a temporary copy
        shutil.copy2(db_filename, tmp_db_filename)

    # Create a temporary database object
    tmp_database = Database(tmp_db_filename)
    # Open the temporary database connection
    tmp_database.open_connection()

    # Open the database connection if it is not already open
    if tmp_database.connection is None:
        tmp_database.open_connection()

    # Start the dashboard
    dashboard = Dashboard(tmp_database)
    dashboard.run()

    # User decides to save the changes
    # TODO - Make sure if program quits unexpectedly, the tmp_database file is opened and the user is prompted to save the changes
    save_changes = input("Do you want to save the changes? (y/n): ")
    if save_changes.lower() == "y":
        shutil.copy2(tmp_db_filename, db_filename)
        print("Changes saved successfully.")
        os.remove(tmp_db_filename)
    else:
        discard_changes = input("Do you want to discard the changes? (y/n): ")
        if discard_changes.lower() == "y":
            os.remove(tmp_db_filename)
            print("Changes discarded.")


    # Close the database connections
    database.close_connection()
    tmp_database.close_connection()


if __name__ == "__main__":
    main()
