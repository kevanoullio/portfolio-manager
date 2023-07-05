# Purpose: Main entry point for the portfolio manager application.

# Standard Libraries
import os
import shutil

# Third-party Libraries

# Local Modules
from database.database import Database
from dashboard.dashboard import Dashboard


def main():
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
        database.initialize_database()
    else:
        # If the database file exists, create a database object
        database = Database(db_filename)

    # Check if the temporary database file exists
    if not os.path.isfile(tmp_db_filename):
        # If the tmp_database file doesn't exist, create a temporary copy
        shutil.copy2(db_filename, tmp_db_filename)

    # Create a temporary database object
    tmp_database = Database(tmp_db_filename)
    # Open the temporary database connection
    tmp_database.open_connection()


    # Open the database connection if it is not already open
    if database.connection is None:
        database.open_connection()

    # Start the dashboard
    dashboard = Dashboard(database)
    dashboard.run()


    # User decides to save the changes
    save_changes = input("Do you want to save the changes? (y/n): ")
    if save_changes.lower() == "y":
        shutil.copy2(tmp_db_filename, db_filename)
        print("Changes saved successfully.")
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
