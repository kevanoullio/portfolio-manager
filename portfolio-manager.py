# Purpose: Main entry point for the portfolio manager application.

# Standard Libraries
import os

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
    # Check if the database file exists
    db_file = "./user_data/database.db"
    if not os.path.isfile(db_file):
        # If the database file doesn't exist, create a database object
        database = Database(db_file)
        # Open the database connection
        database.open_connection()
        # Initialize the database
        database.initialize_database()
    else:
        # If the database file exists, create a database object
        database = Database(db_file)
    
    # Check if the database connection is already open
    if database.connection is None:
        # If not, open the database connection
        database.open_connection()
    
    # Start the dashboard
    dashboard = Dashboard(database)
    dashboard.run()

    # Close the database connection
    database.close_connection()

if __name__ == "__main__":
    main()
